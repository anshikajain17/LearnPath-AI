import React,{useEffect,useMemo,useState} from "react";
import {api} from "./api";
import {
  LayoutDashboard, Route, BrainCircuit, UserRound, Upload, Sparkles,
  Target, Clock3, Flame, ArrowUpRight, CheckCircle2, LockKeyhole,
  Send, RefreshCw, ChevronRight, Zap, FileText
} from "lucide-react";
import {ResponsiveContainer,AreaChart,Area,Tooltip} from "recharts";

const demoProfile={
  name:"Learner",
  goal:"Become an AI Engineer in 6 months. I know Python and basic ML. I can study 2 hours a day.",
  skills:{Python:55,"Machine Learning":35,JavaScript:20,SQL:20},
  interests:["AI","Building projects"], hours_per_day:2, months:6
};

function pct(v){return Math.round(Number(v||0))}
function App(){
  const [profile,setProfile]=useState(demoProfile);
  const [plan,setPlan]=useState(null);
  const [view,setView]=useState("dashboard");
  const [loading,setLoading]=useState(false);
  const [toast,setToast]=useState("");
  const [coachQ,setCoachQ]=useState("");
  const [coachA,setCoachA]=useState("");
  const [assessment,setAssessment]=useState({skill:"Python",score:80});
  const [resume,setResume]=useState(null);

  useEffect(()=>{api.health().catch(()=>{});},[]);
  const generate=async()=>{
    setLoading(true); try{const p=await api.personalize(profile); setPlan(p); setProfile(p.profile); setToast("Your adaptive plan is ready.");}
    catch(e){setToast("Backend is not running. Start FastAPI on port 8000.");} finally{setLoading(false);}
  };
  useEffect(()=>{generate()},[]);

  const submitAssessment=async()=>{
    try{const p=await api.assessment({...assessment,score:Number(assessment.score)});setPlan(p);setProfile(p.profile);setToast(`Updated ${assessment.skill}: ${p.assessment_update.old}% → ${p.assessment_update.new}%`);}
    catch(e){setToast("Could not submit assessment.");}
  };
  const ask=async()=>{
    if(!coachQ.trim())return;
    try{const r=await api.coach({question:coachQ,profile,roadmap:plan?.roadmap||[]});setCoachA(r.answer);}
    catch(e){setCoachA("Start the backend to use the coach.");}
  };
  const upload=async(e)=>{
    const f=e.target.files?.[0]; if(!f)return;
    try{const r=await api.resume(f);setResume(r);setToast(`${r.skills.length} skills detected from resume.`);}
    catch(e){setToast("Resume parsing failed.");}
  };

  const nav=[
    ["dashboard","Overview",LayoutDashboard],["roadmap","Learning Path",Route],
    ["skills","Skill Intelligence",BrainCircuit],["coach","AI Coach",Sparkles],
    ["profile","Learner Profile",UserRound]
  ];
  const readiness=plan?.readiness||0;
  const gapData=useMemo(()=>plan?.skill_gaps?.slice(0,7).map(x=>({name:x.skill,gap:x.gap}))||[],[plan]);

  return <div className="app">
    <aside className="sidebar">
      <div className="brand"><div className="brandmark"><Sparkles size={18}/></div><div><b>LearnPath</b><span>AI Career Intelligence</span></div></div>
      <div className="nav">{nav.map(([id,label,Icon])=><button className={view===id?"active":""} onClick={()=>setView(id)} key={id}><Icon size={18}/>{label}</button>)}</div>
      <div className="sideCard"><div className="tiny">CURRENT TARGET</div><strong>{profile.role||"Career path"}</strong><div className="miniBar"><i style={{width:`${readiness}%`}}/></div><span>{readiness}% ready</span></div>
      <div className="sideFoot">Adaptive engine v2.0<br/>Evidence-driven learning</div>
    </aside>
    <main className="main">
      <header className="topbar"><div className="mobileBrand">LearnPath AI</div><div className="status"><span className="dot"/> Intelligence online</div><button className="ghost" onClick={generate}><RefreshCw size={15}/> Recalculate</button></header>
      {toast&&<div className="toast" onClick={()=>setToast("")}>{toast}</div>}
      {view==="dashboard"&&<Dashboard plan={plan} readiness={readiness} gapData={gapData} onView={setView}/>}
      {view==="roadmap"&&<Roadmap plan={plan}/>}
      {view==="skills"&&<Skills plan={plan} gapData={gapData}/>}
      {view==="coach"&&<Coach q={coachQ} setQ={setCoachQ} a={coachA} ask={ask} plan={plan}/>}
      {view==="profile"&&<ProfileEditor profile={profile} setProfile={setProfile} generate={generate} loading={loading} upload={upload} resume={resume}/>}
    </main>
  </div>
}

function Dashboard({plan,readiness,gapData,onView}){
  if(!plan)return <div className="empty">Preparing your career intelligence…</div>;
  const chart=[{x:"Start",v:Math.max(8,readiness-24)},{x:"Now",v:readiness},{x:"Target",v:100}];
  return <section>
    <div className="hero"><div><div className="eyebrow"><Zap size={14}/> PERSONALIZED CAREER INTELLIGENCE</div><h1>Your next best move,<br/><em>made intelligent.</em></h1><p>LearnPath continuously compares your current evidence with your target role and adapts the path as you learn.</p><div className="heroBtns"><button className="primary" onClick={()=>onView("roadmap")}>Continue learning <ArrowUpRight size={17}/></button><button className="secondary" onClick={()=>onView("skills")}>Explore skill graph</button></div></div>
      <div className="readiness"><div className="ring"><div><b>{pct(readiness)}%</b><span>ready</span></div></div><span>Career readiness</span></div>
    </div>
    <div className="grid4">
      <Metric icon={Target} label="Target role" value={plan.profile.role}/>
      <Metric icon={Clock3} label="Daily budget" value={`${plan.profile.hours_per_day}h / day`}/>
      <Metric icon={Flame} label="Learning streak" value="7 days"/>
      <Metric icon={CheckCircle2} label="Next action" value={plan.next_action.skill}/>
    </div>
    <div className="two">
      <Card title="Readiness trajectory" subtitle="Illustrative progress from your current evidence"><div className="chart"><ResponsiveContainer width="100%" height={220}><AreaChart data={chart}><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopOpacity=".35"/><stop offset="100%" stopOpacity="0"/></linearGradient></defs><Area type="monotone" dataKey="v" stroke="currentColor" fill="url(#g)" strokeWidth={3}/><Tooltip/></AreaChart></ResponsiveContainer></div></Card>
      <Card title="Next best action" subtitle="Chosen from your highest-priority evidence"><div className="next"><div className="nextIcon"><Sparkles/></div><div><b>{plan.next_action.skill}</b><p>{plan.next_action.reasons?.join(" · ")}</p><span>{plan.next_action.duration_days||7} days · {plan.next_action.recommended_hours||4}h guided practice</span></div><button onClick={()=>onView("roadmap")}><ChevronRight/></button></div></Card>
    </div>
    <div className="two">
      <Card title="Top skill gaps" subtitle="Where your target role has the most unmet evidence"><div className="gapList">{gapData.map((x)=><div className="gap" key={x.name}><span>{x.name}</span><div className="track"><i style={{width:`${x.gap}%`}}/></div><b>{pct(x.gap)}%</b></div>)}</div></Card>
      <Card title="Why this path?" subtitle="Transparent recommendation logic"><div className="reasons">{["Skill-gap priority","Prerequisite readiness","Goal similarity","Difficulty fit","Available study time"].map((x,i)=><div key={x}><span>{i+1}</span><b>{x}</b><small>Used by the recommendation engine</small></div>)}</div></Card>
    </div>
  </section>
}

function Metric({icon:Icon,label,value}){return <div className="metric"><div className="metricIcon"><Icon size={17}/></div><div><span>{label}</span><b>{value}</b></div></div>}
function Card({title,subtitle,children}){return <div className="card"><div className="cardHead"><div><h3>{title}</h3><p>{subtitle}</p></div></div>{children}</div>}

function Roadmap({plan}){
  return <section><SectionHead eyebrow="ADAPTIVE ROADMAP" title="Your path to the target role" text="Prerequisites are ordered automatically. Assessment evidence can regenerate this sequence."/>
    <div className="roadmap">{plan?.roadmap?.map((x,i)=><div className={`step ${i===0?"current":""}`} key={x.id}><div className="stepLine"><div className="stepDot">{i+1}</div>{i<plan.roadmap.length-1&&<i/>}</div><div className="stepBody"><div className="stepTop"><div><span className="pill">{x.type}</span><h3>{x.skill}</h3><p>{x.reasons?.join(" · ")}</p></div><button className="check"><CheckCircle2/></button></div><div className="resourceRow">{(x.resources||[]).map(r=><span key={r}><FileText size={14}/>{r}</span>)}</div><div className="stepFoot"><span>{x.duration_days} days</span><span>Score {Math.round(x.score*100)}%</span>{x.prerequisites?.length>0&&<span>Requires {x.prerequisites.join(", ")}</span>}</div></div></div>)}</div>
  </section>
}

function Skills({plan,gapData}){
  return <section><SectionHead eyebrow="SKILL INTELLIGENCE" title="See the gap, not just the goal" text="Your role is represented as an evidence graph: mastered, developing and missing capabilities."/>
    <div className="skillLayout"><Card title={`${plan?.profile?.role||"Career"} skill map`} subtitle="Status is computed from your learner evidence"><div className="skillGraph">{plan?.graph?.map((n,i)=><div className={`node ${n.status}`} style={{"--x":`${12+(i%4)*25}%`,"--y":`${18+Math.floor(i/4)*28}%`}} key={n.skill}><div>{n.status==="mastered"?<CheckCircle2/>:<BrainCircuit/>}</div><b>{n.skill}</b><span>{pct(n.score)}%</span></div>)}</div></Card>
      <Card title="Gap priorities" subtitle="Largest gaps are surfaced first"><div className="gapList">{gapData.map(x=><div className="gap" key={x.name}><span>{x.name}</span><div className="track"><i style={{width:`${x.gap}%`}}/></div><b>{pct(x.gap)}%</b></div>)}</div></Card></div>
  </section>
}

function Coach({q,setQ,a,ask,plan}){
  return <section><SectionHead eyebrow="AI COACH" title="Ask about your path" text="The coach is grounded in your actual profile and roadmap. Add an API key for the optional LLM provider; local mode works without one."/>
    <div className="coach"><div className="coachHeader"><div className="coachOrb"><Sparkles/></div><div><b>LearnPath Intelligence</b><span>Context-aware career coach</span></div></div><div className="chat">{a?<div className="bubble ai">{a}</div>:<div className="suggestions">{["Why is my next step recommended?","Can I skip my current topic?","How can I compress my roadmap?","What should I build for my target role?"].map(x=><button onClick={()=>setQ(x)} key={x}>{x}<ChevronRight/></button>)}</div>}</div><div className="composer"><input value={q} onChange={e=>setQ(e.target.value)} onKeyDown={e=>e.key==="Enter"&&ask()} placeholder="Ask: Why should I learn this next?"/><button onClick={ask}><Send size={17}/></button></div></div>
  </section>
}

function ProfileEditor({profile,setProfile,generate,loading,upload,resume}){
  const [skills,setSkills]=useState(Object.entries(profile.skills||{}));
  const update=(k,v)=>setProfile(p=>({...p,[k]:v}));
  return <section><SectionHead eyebrow="LEARNER PROFILE" title="Give the engine better evidence" text="Natural language is enough. The engine also accepts explicit skill evidence, time and career constraints."/>
    <div className="profileGrid"><Card title="Career intent" subtitle="Tell LearnPath where you want to go"><label>Goal</label><textarea value={profile.goal} onChange={e=>update("goal",e.target.value)}/><div className="formRow"><div><label>Name</label><input value={profile.name} onChange={e=>update("name",e.target.value)}/></div><div><label>Hours/day</label><input type="number" min=".25" max="12" value={profile.hours_per_day} onChange={e=>update("hours_per_day",Number(e.target.value))}/></div></div><button className="primary wide" onClick={generate} disabled={loading}>{loading?<RefreshCw className="spin"/>:<Sparkles/>} Generate adaptive plan</button></Card>
      <Card title="Resume intelligence" subtitle="Upload a PDF or plain-text resume to extract skills"><label className="upload"><Upload/><span>Drop resume here or click to browse<input type="file" accept=".pdf,.txt" onChange={upload}/></span></label>{resume&&<div className="resumeResult"><b>{resume.filename}</b><div>{resume.skills.map(s=><span key={s.skill}>{s.skill}</span>)}</div></div>}<div className="skillEditor"><label>Known skills</label>{skills.map(([k,v])=><div className="skillEdit" key={k}><span>{k}</span><input type="range" min="0" max="100" value={v} onChange={e=>{const n=Number(e.target.value);setSkills(skills.map(x=>x[0]===k?[k,n]:x));setProfile(p=>({...p,skills:{...p.skills,[k]:n}}))}}/><b>{v}%</b></div>)}</div></Card></div>
  </section>
}

function SectionHead({eyebrow,title,text}){return <div className="sectionHead"><div className="eyebrow"><Sparkles size={13}/>{eyebrow}</div><h2>{title}</h2><p>{text}</p></div>}
export default App;
