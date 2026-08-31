import os, io
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .db import init_db, save_profile, load_profile, save_assessment
from .schemas import Profile, Assessment, CoachRequest
from .services.goal_parser import parse_goal
from .services.recommender import readiness, gaps, build_plan, make_graph
from .services.adaptive import apply_assessment
from .services.ai_service import coach_answer

app = FastAPI(title="LearnPath AI Next", version="2.0.0")

origins = [x.strip() for x in os.getenv("CORS_ORIGINS","http://localhost:5173").split(",")]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def startup():
    init_db()

def generate(profile: Profile):
    role, months, hours, inferred, target = parse_goal(profile.goal)
    skills = dict(profile.skills)
    for k,v in inferred.items():
        skills.setdefault(k, v)
    profile.role, profile.months, profile.hours_per_day, profile.skills = role, months, hours, skills
    roadmap, projects = build_plan(role, profile.goal, skills, hours, months)
    gap_rows = gaps(role, skills)
    ready = readiness(role, skills)
    next_action = roadmap[0] if roadmap else {"title":"You're ready for the target role.","skill":role}
    schedule = make_schedule(roadmap, hours)
    save_profile(profile.model_dump())
    return {
        "profile": profile.model_dump(),
        "readiness": ready,
        "skill_gaps": gap_rows,
        "roadmap": roadmap,
        "graph": make_graph(role, skills),
        "next_action": next_action,
        "schedule": schedule,
        "projects": projects,
        "explanation": f"Recommendations combine skill-gap priority, prerequisite readiness, goal similarity and difficulty fit for {role}."
    }

def make_schedule(roadmap, hours):
    slots = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    out=[]
    for i, item in enumerate(roadmap[:7]):
        out.append({"day":slots[i], "focus":item["skill"], "minutes":min(180,max(30,int(hours*60))), "action":item["title"]})
    return out

@app.get("/api/health")
def health():
    return {"status":"ok","service":"learnpath-ai-next"}

@app.post("/api/personalize")
def personalize(profile: Profile):
    return generate(profile)

@app.get("/api/profile")
def profile():
    p = load_profile()
    return p or Profile().model_dump()

@app.post("/api/assessment")
def assessment(item: Assessment):
    p = load_profile() or Profile().model_dump()
    skills, old, new = apply_assessment(p.get("skills",{}), item.skill, item.score)
    p["skills"] = skills
    save_assessment(item.skill,item.score)
    save_profile(p)
    result = generate(Profile(**p))
    result["assessment_update"] = {"skill":item.skill,"old":old,"new":new}
    return result

@app.post("/api/coach")
async def coach(req: CoachRequest):
    return {"answer": await coach_answer(req.question, req.profile.model_dump(), req.roadmap)}

@app.post("/api/resume")
async def resume(file: UploadFile = File(...)):
    data = await file.read()
    text = ""
    if file.filename and file.filename.lower().endswith(".pdf"):
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(data))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as e:
            raise HTTPException(400, f"Could not parse PDF: {e}")
    else:
        text = data.decode("utf-8", errors="ignore")

    from ..app.data.catalog import SKILLS
    lower = text.lower()
    found = []
    for skill in SKILLS:
        aliases = [skill.lower()]
        if skill == "JavaScript": aliases += ["js"]
        if skill == "Git/GitHub": aliases += ["git","github"]
        if skill == "HTML/CSS": aliases += ["html","css"]
        if any(a in lower for a in aliases):
            found.append({"skill":skill,"evidence":"Detected in resume"})
    return {"filename":file.filename,"skills":found,"text_preview":text[:1000]}
