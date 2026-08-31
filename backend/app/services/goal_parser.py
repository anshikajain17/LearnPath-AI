import re
from ..data.catalog import ROLE_SKILLS

ROLE_ALIASES = {
    "ai engineer": "AI Engineer",
    "artificial intelligence engineer": "AI Engineer",
    "ml engineer": "ML Engineer",
    "machine learning engineer": "ML Engineer",
    "data scientist": "Data Scientist",
    "mern": "MERN Developer",
    "mern stack developer": "MERN Developer",
    "full stack": "Full Stack Developer",
    "full stack developer": "Full Stack Developer",
    "backend": "Backend Engineer",
    "backend engineer": "Backend Engineer",
    "software engineer": "Software Engineer",
}

def parse_goal(goal: str):
    text = goal.lower()
    role = "Software Engineer"
    for alias, canonical in ROLE_ALIASES.items():
        if alias in text:
            role = canonical
            break

    months = 6
    m = re.search(r"(\d+)\s*(?:month|months|mo)", text)
    if m:
        months = max(1, min(24, int(m.group(1))))

    hours = 2.0
    h = re.search(r"(\d+(?:\.\d+)?)\s*(?:hours?|hrs?)\s*(?:a|per)?\s*day", text)
    if h:
        hours = max(0.25, min(12, float(h.group(1))))

    known = {}
    skill_patterns = {
        "Python": r"\bpython\b",
        "JavaScript": r"\b(?:javascript|js)\b",
        "React": r"\breact\b",
        "SQL": r"\bsql\b",
        "Machine Learning": r"\b(?:machine learning|ml)\b",
        "HTML/CSS": r"\b(?:html|css)\b",
        "Git/GitHub": r"\b(?:git|github)\b",
    }
    for skill, pattern in skill_patterns.items():
        if re.search(pattern, text):
            known[skill] = 55.0

    return role, months, hours, known, ROLE_SKILLS[role]
