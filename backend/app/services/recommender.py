from typing import Dict, List

from ..data.catalog import PREREQS, RESOURCES, SKILLS, ROLE_SKILLS

def _similarity(goal, skill):
    goal_words = set(goal.lower().split())
    skill_words = set(skill.lower().split())
    if not goal_words or not skill_words:
        return 0.0
    return len(goal_words & skill_words) / len(goal_words | skill_words)

def readiness(role: str, skills: Dict[str, float]) -> float:
    target = ROLE_SKILLS.get(role, [])
    if not target:
        return 0.0
    return round(sum(float(skills.get(s, 0)) for s in target) / len(target), 1)

def gaps(role: str, skills: Dict[str, float]):
    rows = []
    for skill in ROLE_SKILLS.get(role, []):
        current = float(skills.get(skill, 0))
        gap = max(0, 100-current)
        priority = round(gap * (1.2 if current < 40 else 1.0), 1)
        rows.append({
            "skill": skill, "current": round(current,1), "gap": round(gap,1),
            "priority": priority, "domain": SKILLS.get(skill,{}).get("domain","Core")
        })
    return sorted(rows, key=lambda x: x["priority"], reverse=True)

def build_plan(role: str, goal: str, skills: Dict[str,float], hours: float, months: int):
    target = ROLE_SKILLS.get(role, [])
    gap_rows = gaps(role, skills)
    completed = {s for s,v in skills.items() if v >= 80}

    def prereqs_ready(skill):
        return all((p in completed) or skills.get(p,0) >= 70 for p in PREREQS.get(skill, []))

    candidates = []
    for row in gap_rows:
        skill = row["skill"]
        if row["gap"] <= 5: continue
        sim = _similarity(goal, skill)
        prereq = 1.0 if prereqs_ready(skill) else 0.45
        difficulty_fit = 1.0 if SKILLS.get(skill,{}).get("difficulty",2) <= 4 else 0.8
        score = 0.50*(row["gap"]/100) + 0.20*sim + 0.20*prereq + 0.10*difficulty_fit
        reasons = [
            f"{row['gap']:.0f}% estimated skill gap",
            "matches the target role",
            "fits your current learning evidence"
        ]
        if PREREQS.get(skill):
            reasons.append("prerequisites: " + ", ".join(PREREQS[skill]))
        candidates.append((score, skill, reasons))

    candidates.sort(reverse=True)
    roadmap = []
    seen = set()

    def add_with_prereqs(skill):
        for p in PREREQS.get(skill, []):
            if p not in seen and p not in completed:
                add_with_prereqs(p)
        if skill not in seen and skill not in completed:
            score, _, reasons = next(((s,k,r) for s,k,r in candidates if k==skill), (0.5, skill, ["required foundation"]))
            roadmap.append({
                "id": f"step-{len(roadmap)+1}",
                "skill": skill,
                "title": f"Master {skill}",
                "type": "Skill milestone",
                "duration_days": max(2, int(8 - min(5, skills.get(skill,0)/20))),
                "score": round(score,3),
                "reasons": reasons,
                "prerequisites": PREREQS.get(skill, []),
                "resources": RESOURCES.get(skill, [f"{skill} guided learning path", f"{skill} practice project"]),
                "completed": False
            })
            seen.add(skill)

    for _, skill, _ in candidates[:10]:
        add_with_prereqs(skill)

    total_days = max(14, months * 30)
    capacity = max(1, int(hours * 2))
    for item in roadmap:
        item["recommended_hours"] = round(max(3, item["duration_days"] * 0.9 / capacity), 1)

    # portfolio projects
    projects = []
    if role in ("AI Engineer","ML Engineer","Data Scientist"):
        projects = [
            {"title":"Adaptive ML Project","difficulty":"Intermediate","skills":["Python","Machine Learning","FastAPI"],"days":10},
            {"title":"RAG Career Coach","difficulty":"Advanced","skills":["Python","LLMs","REST APIs"],"days":14},
        ]
    else:
        projects = [
            {"title":"Production Learning Dashboard","difficulty":"Intermediate","skills":["React","REST APIs","Git/GitHub"],"days":10},
            {"title":"Full Stack Portfolio App","difficulty":"Advanced","skills":["React","Node.js","PostgreSQL"],"days":14},
        ]
    return roadmap, projects

def make_graph(role, skills):
    nodes = []
    for skill in ROLE_SKILLS.get(role, []):
        status = "mastered" if skills.get(skill,0)>=80 else "in-progress" if skills.get(skill,0)>=40 else "missing"
        nodes.append({"skill":skill,"status":status,"score":round(skills.get(skill,0),1),"prerequisites":PREREQS.get(skill,[])})
    return nodes
