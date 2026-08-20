import { useState } from "react";

// ─── Brand Tokens ─────────────────────────────────────────────────────────────
const B = {
  bg:        "#0B0C0E",
  surface:   "#111214",
  surfaceHi: "#161719",
  line:      "#161719",
  lineHi:    "#22252A",
  primary:   "#0062FF",
  secondary: "#8F7AFF",
  gradStart: "#0062FF",
  gradEnd:   "#8F7AFF",
  textPrime: "#FFFFFF",
  textMid:   "#8A8F99",
  textMute:  "#3A3F48",
  success:   "#005F3E",
  error:     "#B6002D",
  info:      "#005FCB",
};

// REEMPLAZAR con el email del usuario autenticado
const CURRENT_USER_EMAIL = "usuario@procontacto.com.mx";
const CLOUD_ID = "d041f87a-4f5e-40d1-b719-578536318f6a";

// REEMPLAZAR con los tickets reales del usuario
const INITIAL_TICKETS = [];

// ─── API: calls Anthropic with Atlassian MCP to log work directly ────────────
async function logWorkToJira({ ticketKey, timeSpent, comment, started }) {
  const prompt = comment
    ? `Use the addWorklogToJiraIssue tool to log time. Parameters: cloudId="${CLOUD_ID}", issueIdOrKey="${ticketKey}", timeSpent="${timeSpent}", started="${started}", commentBody="${comment}", contentFormat="markdown". Just call the tool, nothing else.`
    : `Use the addWorklogToJiraIssue tool to log time. Parameters: cloudId="${CLOUD_ID}", issueIdOrKey="${ticketKey}", timeSpent="${timeSpent}", started="${started}". Just call the tool, nothing else.`;

  const resp = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: "claude-sonnet-4-20250514",
      max_tokens: 1024,
      messages: [{ role: "user", content: prompt }],
      mcp_servers: [{ type: "url", url: "https://mcp.atlassian.com/v1/mcp", name: "atlassian" }],
    }),
  });

  if (!resp.ok) throw new Error(`API ${resp.status}`);
  const data = await resp.json();

  // Check for errors in tool results
  const toolResults = (data.content || []).filter(b => b.type === "mcp_tool_result");
  for (const tr of toolResults) {
    const txt = tr.content?.[0]?.text || "";
    if (tr.is_error || txt.toLowerCase().includes('"errorMessages"')) throw new Error(txt.slice(0, 200));
  }

  // If there's a tool_use, it means the API called the MCP tool
  const toolUse = (data.content || []).filter(b => b.type === "mcp_tool_use");
  if (toolUse.length > 0 || toolResults.length > 0) return true;

  throw new Error("La API no ejecutó la herramienta de Jira");
}

// ─── Helpers ──────────────────────────────────────────────────────────────────
function secsToLabel(s) {
  if (!s || s === 0) return null;
  const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60);
  if (h > 0 && m > 0) return `${h}h ${m}m`;
  return h > 0 ? `${h}h` : `${m}m`;
}
function groupByProject(tickets) {
  const map = {};
  tickets.forEach((t, gi) => { if (!map[t.project]) map[t.project] = []; map[t.project].push({ ...t, globalIndex: gi }); });
  return Object.entries(map);
}
const PA = ["#0062FF","#8F7AFF","#2ECC8A","#FF6B35","#00B4D8"];
function projectAccent(p, all) { return PA[all.indexOf(p) % PA.length]; }
const SC = { done:{bg:"#001A10",color:"#C1E7D5",dot:"#005F3E"}, progress:{bg:"#1A0D00",color:"#FDCCB9",dot:"#D14600"}, waiting:{bg:"#00143A",color:"#B9DCFF",dot:"#005FCB"}, default:{bg:B.surfaceHi,color:B.textMid,dot:B.textMute} };
const SL = { done:"Resuelto", progress:"En curso", waiting:"Esperando respuesta", default:"—" };

// ─── Small Components ────────────────────────────────────────────────────────
const GradientText = ({children}) => <span style={{background:`linear-gradient(90deg,${B.gradStart},${B.gradEnd})`,WebkitBackgroundClip:"text",WebkitTextFillColor:"transparent"}}>{children}</span>;
const StatusBadge = ({type}) => { const c=SC[type]||SC.default; return <span style={{background:c.bg,color:c.color,fontSize:11,fontWeight:600,padding:"3px 10px",borderRadius:20,whiteSpace:"nowrap",display:"inline-flex",alignItems:"center",gap:5}}><span style={{width:5,height:5,borderRadius:"50%",background:c.dot,flexShrink:0}}/>{SL[type]||"—"}</span>; };
const KeyBadge = ({ticketKey}) => <a href={`https://procontacto.atlassian.net/browse/${ticketKey}`} target="_blank" rel="noreferrer" style={{fontSize:11,fontWeight:700,color:B.primary,background:"#00163A",padding:"3px 9px",borderRadius:6,textDecoration:"none",fontFamily:"monospace",border:"1px solid #003380",whiteSpace:"nowrap"}}>{ticketKey}</a>;
const QuickBtn = ({label,onClick}) => { const [h,setH]=useState(false); return <button onClick={onClick} onMouseEnter={()=>setH(true)} onMouseLeave={()=>setH(false)} style={{background:h?"#001533":B.surfaceHi,border:`1px solid ${h?B.primary+"60":B.lineHi}`,borderRadius:5,color:h?B.primary:B.textMute,fontSize:10,padding:"2px 6px",cursor:"pointer",fontFamily:"inherit",transition:"all 0.15s"}}>{label}</button>; };
const ProgressBar = ({value,max=8}) => <div style={{width:"100%",height:3,background:B.lineHi,borderRadius:10,overflow:"hidden",marginTop:5}}><div style={{width:`${Math.min(100,(value/max)*100)}%`,height:"100%",background:`linear-gradient(90deg,${B.gradStart},${B.gradEnd})`,borderRadius:10,transition:"width 0.4s"}}/></div>;
const Spinner = () => <span style={{display:"inline-block",width:14,height:14,border:`2px solid ${B.lineHi}`,borderTop:`2px solid ${B.primary}`,borderRadius:"50%",animation:"spin 0.8s linear infinite"}}/>;

function Toast({msg,onClose}) { const isErr=msg.toLowerCase().includes("error"); return <div style={{position:"fixed",bottom:24,right:24,background:B.surface,color:B.textPrime,padding:"12px 20px",borderRadius:12,fontSize:13,fontWeight:500,border:`1px solid ${isErr?B.error+"60":B.success+"60"}`,display:"flex",alignItems:"center",gap:10,zIndex:1100,maxWidth:420}}><span style={{color:isErr?"#FB4D6B":"#2ECC8A",flexShrink:0}}>{isErr?"✕":"✓"}</span><span style={{overflow:"hidden",textOverflow:"ellipsis"}}>{msg}</span><button onClick={onClose} style={{background:"none",border:"none",color:B.textMute,cursor:"pointer",marginLeft:4,fontSize:18,lineHeight:1,flexShrink:0}}>×</button></div>; }

function ConfirmModal({ticket,hours,comment,loading,onConfirm,onCancel}) {
  return <div style={{position:"fixed",inset:0,background:"rgba(0,0,0,0.82)",display:"flex",alignItems:"center",justifyContent:"center",zIndex:1000}}>
    <div style={{background:B.surface,border:`1px solid ${B.lineHi}`,borderRadius:16,padding:28,width:360}}>
      <p style={{fontSize:16,fontWeight:700,color:B.textPrime,marginBottom:6}}>Confirmar carga</p>
      <p style={{fontSize:13,color:B.textMid,marginBottom:20}}>¿Registrar estas horas en Jira?</p>
      <div style={{background:B.surfaceHi,borderRadius:10,padding:"14px 16px",marginBottom:20,border:`1px solid ${B.lineHi}`}}>
        <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:8}}><span style={{fontSize:12,color:B.textMute}}>Ticket</span><KeyBadge ticketKey={ticket.key}/></div>
        <div style={{display:"flex",justifyContent:"space-between",alignItems:"center"}}><span style={{fontSize:12,color:B.textMute}}>Horas</span><span style={{fontSize:14,fontWeight:700,color:B.textPrime}}>{hours}h</span></div>
        {comment && <div style={{marginTop:10,paddingTop:10,borderTop:`1px solid ${B.lineHi}`}}><span style={{fontSize:11,color:B.textMute,display:"block",marginBottom:4}}>Comentario</span><span style={{fontSize:12,color:B.textMid}}>{comment}</span></div>}
      </div>
      <div style={{display:"flex",gap:10}}>
        <button onClick={onCancel} disabled={loading} style={{flex:1,background:"none",border:`1px solid ${B.lineHi}`,borderRadius:8,color:B.textMid,fontSize:13,padding:"9px 0",cursor:loading?"not-allowed":"pointer",fontFamily:"inherit",opacity:loading?0.5:1}}>Cancelar</button>
        <button onClick={onConfirm} disabled={loading} style={{flex:1,background:`linear-gradient(90deg,${B.gradStart},${B.gradEnd})`,border:"none",borderRadius:8,color:"#fff",fontSize:13,fontWeight:700,padding:"9px 0",cursor:loading?"not-allowed":"pointer",fontFamily:"inherit",display:"flex",alignItems:"center",justifyContent:"center",gap:8,opacity:loading?0.7:1}}>
          {loading ? <><Spinner/> Cargando...</> : "Cargar ↗"}
        </button>
      </div>
    </div>
  </div>;
}

function ProjectHeader({project,tickets,accent,collapsed,onToggle}) {
  const total=tickets.reduce((a,t)=>a+(t.timespent||0),0), label=secsToLabel(total);
  return <tr style={{background:B.surfaceHi,cursor:"pointer"}} onClick={onToggle}><td colSpan={8} style={{padding:"10px 16px"}}><div style={{display:"flex",alignItems:"center",gap:12}}>
    <div style={{width:8,height:8,borderRadius:"50%",background:accent,flexShrink:0}}/>
    <span style={{fontSize:12,fontWeight:700,color:B.textPrime,letterSpacing:"0.03em"}}>{project}</span>
    <span style={{fontSize:10,color:accent,background:accent+"18",padding:"2px 8px",borderRadius:10,fontWeight:600,border:`1px solid ${accent}30`}}>{tickets.length} ticket{tickets.length!==1?"s":""}</span>
    {label && <span style={{fontSize:11,color:B.textMid}}><span style={{color:B.textMute}}>Total: </span><span style={{color:"#2ECC8A",fontWeight:600}}>{label}</span></span>}
    <span style={{marginLeft:"auto",fontSize:11,color:B.textMute,userSelect:"none"}}>{collapsed?"▶ mostrar":"▼ ocultar"}</span>
  </div></td></tr>;
}

// ─── Main App ─────────────────────────────────────────────────────────────────
export default function App() {
  const [tickets,setTickets]=useState(INITIAL_TICKETS);
  const [rows,setRows]=useState(INITIAL_TICKETS.map(t=>({hours:"",comment:t.suggestedComment||""})));
  const [confirm,setConfirm]=useState(null);
  const [toast,setToast]=useState(null);
  const [errors,setErrors]=useState({});
  const [hovered,setHovered]=useState(null);
  const [sessionLog,setSessionLog]=useState([]);
  const [showLog,setShowLog]=useState(false);
  const [loading,setLoading]=useState(false);
  const [collapsed,setCollapsed]=useState({});

  const allProjects=[...new Set(tickets.map(t=>t.project))];
  const groups=groupByProject(tickets);

  const update=(i,f,v)=>{setRows(r=>r.map((row,idx)=>idx===i?{...row,[f]:v}:row));setErrors(e=>({...e,[i]:{...e[i],[f]:false}}));};
  const addHours=(i,a)=>{const c=parseFloat(rows[i]?.hours)||0;update(i,"hours",String(Math.min(24,Math.round((c+a)*10)/10)));};
  const showToastMsg=m=>{setToast(m);setTimeout(()=>setToast(null),5000);};

  const handleCargar=i=>{const raw=parseFloat(rows[i].hours);if(!raw||raw<=0){setErrors(e=>({...e,[i]:{...e[i],hours:true}}));return;}setConfirm({index:i});};

  const confirmLog=async()=>{
    const i=confirm.index, raw=parseFloat(rows[i].hours), comment=rows[i].comment.trim();
    const h=Math.floor(raw), m=Math.round((raw-h)*60);
    const timeSpent=m>0?(h>0?`${h}h ${m}m`:`${m}m`):`${h}h`;
    const now=new Date(), started=now.toISOString().split(".")[0]+".000+0000";
    setLoading(true);
    try {
      await logWorkToJira({ticketKey:tickets[i].key,timeSpent,comment,started});
      const addedSecs=Math.round(raw*3600);
      setTickets(ts=>ts.map((t,idx)=>idx===i?{...t,timespent:(t.timespent||0)+addedSecs}:t));
      setSessionLog(l=>[{key:tickets[i].key,time:timeSpent,comment,ts:now.toLocaleTimeString("es",{hour:"2-digit",minute:"2-digit"})},...l]);
      setRows(r=>r.map((row,idx)=>idx===i?{hours:"",comment:""}:row));
      showToastMsg(`${timeSpent} cargadas en ${tickets[i].key}`);
    } catch(err) { showToastMsg(`Error: ${err.message}`); }
    finally { setLoading(false); setConfirm(null); }
  };

  const totalSessionH=sessionLog.reduce((a,l)=>{const hm=l.time.match(/(\d+)h/),mm=l.time.match(/(\d+)m/);return a+(hm?parseInt(hm[1]):0)+(mm?parseInt(mm[1])/60:0);},0);
  const thStyle={padding:"11px 14px",textAlign:"left",fontSize:10,fontWeight:600,color:B.textMute,letterSpacing:"0.08em",textTransform:"uppercase",whiteSpace:"nowrap",background:B.surface};
  const inputBase=hasErr=>({background:B.surfaceHi,border:`1px solid ${hasErr?B.error:B.lineHi}`,borderRadius:8,color:B.textPrime,fontFamily:"inherit",outline:"none"});

  return <div style={{minHeight:"100vh",background:B.bg,fontFamily:"'Inter','DM Sans',sans-serif",padding:"28px 32px",color:B.textPrime}}>
    <style>{`@keyframes spin{to{transform:rotate(360deg)}}`}</style>

    {/* Header */}
    <div style={{display:"flex",alignItems:"center",justifyContent:"space-between",marginBottom:20}}>
      <div style={{display:"flex",alignItems:"center",gap:14}}>
        <svg width="38" height="38" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg" style={{flexShrink:0,borderRadius:8}}>
          <rect width="28" height="28" rx="6" fill="#1a1a2e"/><path d="M16.4705 3.84314H8.78418L12.7646 0L16.4705 3.84314Z" fill="#4fc3f7"/><path d="M24.1569 16.4707L24.1569 8.78442L28 12.7648L24.1569 16.4707Z" fill="#4fc3f7"/><path d="M11.5295 24.1569L19.2158 24.1569L15.2354 28L11.5295 24.1569Z" fill="#4fc3f7"/><path d="M3.84314 11.5293L3.84314 19.2156L-1.73989e-07 15.2352L3.84314 11.5293Z" fill="#4fc3f7"/><path fillRule="evenodd" clipRule="evenodd" d="M14.1381 3.84326C14.1381 8.31568 10.5125 11.9413 6.04004 11.9413V8.92169C8.84478 8.92169 11.1185 6.648 11.1185 3.84326H14.1381Z" fill="#4fc3f7"/><path fillRule="evenodd" clipRule="evenodd" d="M24.1562 14.1372C19.6838 14.1372 16.0582 10.5116 16.0582 6.03918L19.0778 6.03918C19.0778 8.84392 21.3515 11.1176 24.1562 11.1176L24.1562 14.1372Z" fill="#4fc3f7"/><path fillRule="evenodd" clipRule="evenodd" d="M13.8629 24.1567C13.8629 19.6843 17.4885 16.0587 21.9609 16.0587L21.9609 19.0783C19.1562 19.0783 16.8825 21.352 16.8825 24.1567L13.8629 24.1567Z" fill="#4fc3f7"/><path fillRule="evenodd" clipRule="evenodd" d="M3.84375 13.8628C8.31617 13.8628 11.9418 17.4884 11.9418 21.9608L8.92218 21.9608C8.92218 19.1561 6.64849 16.8824 3.84375 16.8824L3.84375 13.8628Z" fill="#4fc3f7"/>
        </svg>
        <div>
          <h1 style={{fontSize:18,fontWeight:700,margin:0,letterSpacing:"-0.03em"}}><GradientText>Pro</GradientText><span style={{color:B.textPrime}}>Contacto</span><span style={{color:B.textMute,fontWeight:400,fontSize:14}}> · Registro de horas</span></h1>
          <p style={{fontSize:11,color:B.textMute,margin:0}}>procontacto.atlassian.net · {CURRENT_USER_EMAIL} · <span style={{color:B.secondary}}>{allProjects.length} proyectos</span> · <span style={{color:"#2ECC8A"}}>API directa</span></p>
        </div>
      </div>
      <div style={{display:"flex",alignItems:"center",gap:12}}>
        {sessionLog.length>0 && <>
          <button onClick={()=>setShowLog(v=>!v)} style={{background:B.surfaceHi,border:`1px solid ${B.lineHi}`,borderRadius:8,color:B.textPrime,fontSize:12,padding:"7px 14px",cursor:"pointer",fontFamily:"inherit",display:"flex",alignItems:"center",gap:8}}>
            <span style={{color:B.secondary,fontWeight:700}}>{Math.round(totalSessionH*10)/10}h</span><span style={{color:B.textMute}}>hoy</span><span style={{color:B.textMute,fontSize:9}}>{showLog?"▲":"▼"}</span>
          </button>
          <div style={{display:"flex",alignItems:"center",gap:6}}>
            <div style={{width:80,height:4,background:B.lineHi,borderRadius:10,overflow:"hidden"}}><div style={{width:`${Math.min(100,(totalSessionH/8)*100)}%`,height:"100%",background:`linear-gradient(90deg,${B.gradStart},${B.gradEnd})`,borderRadius:10,transition:"width 0.4s"}}/></div>
            <span style={{fontSize:10,color:B.textMute}}>/ 8h</span>
          </div>
        </>}
      </div>
    </div>

    <div style={{height:1,background:`linear-gradient(90deg,${B.gradStart},${B.gradEnd},transparent)`,marginBottom:20}}/>

    {showLog && sessionLog.length>0 && <div style={{background:B.surface,border:`1px solid ${B.lineHi}`,borderRadius:12,padding:"14px 18px",marginBottom:20}}>
      <p style={{fontSize:10,color:B.textMute,textTransform:"uppercase",letterSpacing:"0.08em",marginBottom:12}}>Cargas de esta sesión</p>
      {sessionLog.map((l,i)=><div key={i} style={{display:"flex",alignItems:"center",gap:12,padding:"7px 0",borderBottom:i<sessionLog.length-1?`1px solid ${B.line}`:"none"}}>
        <KeyBadge ticketKey={l.key}/><span style={{fontSize:13,fontWeight:700,color:B.secondary}}>{l.time}</span>
        {l.comment&&<span style={{fontSize:12,color:B.textMute,flex:1,overflow:"hidden",textOverflow:"ellipsis",whiteSpace:"nowrap"}}>{l.comment}</span>}
        <span style={{fontSize:11,color:B.textMute,marginLeft:"auto",flexShrink:0}}>{l.ts}</span>
      </div>)}
    </div>}

    {/* Table */}
    <div style={{background:B.surface,borderRadius:14,border:`1px solid ${B.lineHi}`,overflow:"hidden"}}>
      <table style={{width:"100%",borderCollapse:"collapse"}}>
        <thead><tr style={{borderBottom:`1px solid ${B.lineHi}`}}>{["Ticket","Título","Estado","Ya cargado","Actualizado","Horas","Comentario",""].map((h,i)=><th key={i} style={thStyle}>{h}</th>)}</tr></thead>
        <tbody>{groups.map(([project,pts],gi)=>{
          const accent=projectAccent(project,allProjects), isColl=collapsed[project], isLast=gi===groups.length-1;
          return [
            <ProjectHeader key={`h-${project}`} project={project} tickets={pts} accent={accent} collapsed={isColl} onToggle={()=>setCollapsed(c=>({...c,[project]:!c[project]}))}/>,
            ...(!isColl?pts.map((t,li)=>{
              const i=t.globalIndex, isLastIn=li===pts.length-1, logged=secsToLabel(t.timespent), loggedH=t.timespent?t.timespent/3600:0;
              return <tr key={t.key} style={{borderBottom:(!isLastIn||!isLast)?`1px solid ${B.line}`:"none"}} onMouseEnter={()=>setHovered(i)} onMouseLeave={()=>setHovered(null)}>
                <td style={{padding:"13px 14px",whiteSpace:"nowrap",background:hovered===i?B.surfaceHi:"transparent",borderLeft:`2px solid ${accent}40`}}><KeyBadge ticketKey={t.key}/></td>
                <td style={{padding:"13px 14px",maxWidth:240,background:hovered===i?B.surfaceHi:"transparent"}}><span style={{fontSize:13,color:"#D0D4DC",display:"block",overflow:"hidden",textOverflow:"ellipsis",whiteSpace:"nowrap"}} title={t.title}>{t.title}</span></td>
                <td style={{padding:"13px 14px",whiteSpace:"nowrap",background:hovered===i?B.surfaceHi:"transparent"}}><StatusBadge type={t.statusType}/></td>
                <td style={{padding:"13px 14px",whiteSpace:"nowrap",background:hovered===i?B.surfaceHi:"transparent"}}>{logged?<div style={{minWidth:64}}><span style={{fontSize:13,fontWeight:700,color:"#2ECC8A"}}>{logged}</span><ProgressBar value={loggedH}/></div>:<span style={{fontSize:11,color:B.textMute}}>—</span>}</td>
                <td style={{padding:"13px 14px",background:hovered===i?B.surfaceHi:"transparent"}}><span style={{fontSize:11,color:B.textMute,whiteSpace:"nowrap"}}>{t.updated}</span></td>
                <td style={{padding:"13px 10px",background:hovered===i?B.surfaceHi:"transparent"}}>
                  <div style={{display:"flex",alignItems:"center",gap:5}}>
                    <input type="number" min="0.5" max="24" step="0.5" value={rows[i]?.hours||""} onChange={e=>update(i,"hours",e.target.value)} placeholder="0" style={{...inputBase(errors[i]?.hours),width:52,padding:"7px 6px",fontSize:13,textAlign:"center"}} onFocus={e=>e.target.style.borderColor=accent} onBlur={e=>e.target.style.borderColor=errors[i]?.hours?B.error:B.lineHi}/>
                    <span style={{fontSize:11,color:B.textMute}}>h</span>
                  </div>
                  <div style={{display:"flex",gap:3,marginTop:6}}>{[0.5,1,2].map(a=><QuickBtn key={a} label={`+${a}h`} onClick={()=>addHours(i,a)}/>)}</div>
                  {errors[i]?.hours&&<span style={{fontSize:10,color:"#FB4D6B",display:"block",marginTop:3}}>Requerido</span>}
                </td>
                <td style={{padding:"13px 10px",minWidth:200,background:hovered===i?B.surfaceHi:"transparent"}}>
                  <textarea value={rows[i]?.comment||""} onChange={e=>update(i,"comment",e.target.value)} placeholder="Describí el trabajo..." rows={2} style={{...inputBase(false),width:"100%",padding:"7px 10px",fontSize:12,resize:"vertical",lineHeight:1.5}} onFocus={e=>e.target.style.borderColor=accent} onBlur={e=>e.target.style.borderColor=B.lineHi}/>
                </td>
                <td style={{padding:"13px 14px",background:hovered===i?B.surfaceHi:"transparent"}}>
                  <button onClick={()=>handleCargar(i)} style={{background:`linear-gradient(90deg,${B.gradStart},${B.gradEnd})`,border:"none",borderRadius:8,color:"#fff",padding:"8px 16px",fontSize:12,fontWeight:700,cursor:"pointer",whiteSpace:"nowrap",fontFamily:"inherit",transition:"opacity 0.15s"}} onMouseEnter={e=>e.currentTarget.style.opacity="0.8"} onMouseLeave={e=>e.currentTarget.style.opacity="1"}>Cargar</button>
                </td>
              </tr>;
            }):[])
          ];
        })}</tbody>
      </table>
    </div>

    <p style={{fontSize:10,color:B.textMute,marginTop:14,textAlign:"right"}}>Hacé clic en el nombre del proyecto para colapsar</p>

    {confirm && <ConfirmModal ticket={tickets[confirm.index]} hours={rows[confirm.index].hours} comment={rows[confirm.index].comment} loading={loading} onConfirm={confirmLog} onCancel={()=>!loading&&setConfirm(null)}/>}
    {toast && <Toast msg={toast} onClose={()=>setToast(null)}/>}
  </div>;
}
