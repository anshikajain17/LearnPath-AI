const API = import.meta.env.VITE_API_URL || "http://localhost:8000";
async function request(path, options={}) {
  const r = await fetch(`${API}${path}`, {headers: {"Content-Type":"application/json", ...(options.headers||{})}, ...options});
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}
export const api = {
  health:()=>request("/api/health"),
  personalize:(profile)=>request("/api/personalize",{method:"POST",body:JSON.stringify(profile)}),
  assessment:(x)=>request("/api/assessment",{method:"POST",body:JSON.stringify(x)}),
  coach:(x)=>request("/api/coach",{method:"POST",body:JSON.stringify(x)}),
  resume:async(file)=>{
    const fd=new FormData(); fd.append("file",file);
    const r=await fetch(`${API}/api/resume`,{method:"POST",body:fd});
    if(!r.ok) throw new Error(await r.text()); return r.json();
  }
};
