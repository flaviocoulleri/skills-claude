import { useState } from "react";

// ─── Design Tokens (OKLCH — tinted toward ProContacto blue h264) ──────────────
const B = {
  bg:           "oklch(0.09 0.008 264)",
  surface:      "oklch(0.115 0.009 264)",
  surfaceHi:    "oklch(0.135 0.009 264)",
  surfaceMd:    "oklch(0.155 0.010 264)",
  line:         "oklch(0.165 0.008 264)",
  lineHi:       "oklch(0.205 0.009 264)",
  primary:      "oklch(0.52 0.24 264)",
  primaryDim:   "oklch(0.17 0.08 264)",
  primaryFaint: "oklch(0.13 0.04 264)",
  secondary:    "oklch(0.68 0.18 281)",
  textPrime:    "oklch(0.97 0.005 264)",
  textMid:      "oklch(0.62 0.010 264)",
  textMute:     "oklch(0.38 0.008 264)",
  success:      "oklch(0.55 0.15 155)",
  warning:      "oklch(0.65 0.18 50)",
  error:        "oklch(0.55 0.20 22)",
};

// Antonio (condensed, departure-board feel) + Figtree (clean, legible at 11px)
const F = {
  display: "'Antonio', 'Barlow Condensed', sans-serif",
  body:    "'Figtree', 'Barlow', sans-serif",
};

// REEMPLAZAR con los datos del briefing generados por la skill
const BRIEFING_DATA = {};

// ─── Primitives ───────────────────────────────────────────────────────────────

// Animated chevron (rotates on open)
function Chevron({ open }) {
  return (
    <span style={{
      fontSize: 10, color: B.textMute, flexShrink: 0, userSelect: "none",
      display: "inline-block", lineHeight: 1,
      transition: "transform 0.2s cubic-bezier(0.4,0,0.2,1), color 0.15s",
      transform: open ? "rotate(90deg)" : "rotate(0deg)",
    }}>▶</span>
  );
}

// grid-template-rows expand — no height animation, no layout thrashing
function Expand({ open, children }) {
  return (
    <div style={{
      display: "grid",
      gridTemplateRows: open ? "1fr" : "0fr",
      transition: "grid-template-rows 0.22s cubic-bezier(0.4,0,0.2,1)",
    }}>
      <div style={{ overflow: "hidden" }}>{children}</div>
    </div>
  );
}

// Section label with extending rule — supports collapsible behavior
function SectionLabel({ icon, title, right, collapsible, collapsed, onToggle }) {
  return (
    <div
      onClick={collapsible ? onToggle : undefined}
      style={{
        display: "flex", alignItems: "center", gap: 8,
        marginBottom: 12,
        cursor: collapsible ? "pointer" : "default",
        userSelect: "none",
      }}
    >
      <span style={{ fontSize: 11, lineHeight: 1, flexShrink: 0 }}>{icon}</span>
      <span style={{
        fontFamily: F.body, fontSize: 10, fontWeight: 600,
        color: B.textMute, letterSpacing: "0.1em", textTransform: "uppercase",
        flexShrink: 0,
      }}>{title}</span>
      <div style={{ flex: 1, height: 1, background: B.line }} />
      {right && (
        <span style={{
          fontFamily: F.body, fontSize: 10, color: B.textMute,
          background: B.surfaceMd, padding: "2px 8px", borderRadius: 20, flexShrink: 0,
        }}>{right}</span>
      )}
      {collapsible && <Chevron open={!collapsed} />}
    </div>
  );
}

// Status badge — pill shape
const STATUS = {
  done:     { bg: "oklch(0.16 0.05 155)", fg: "oklch(0.80 0.12 155)", dot: "oklch(0.55 0.15 155)", label: "Resuelto" },
  progress: { bg: "oklch(0.17 0.06 50)",  fg: "oklch(0.82 0.14 50)",  dot: "oklch(0.65 0.18 50)",  label: "En curso" },
  waiting:  { bg: "oklch(0.15 0.05 264)", fg: "oklch(0.78 0.14 264)", dot: "oklch(0.58 0.18 264)", label: "En espera" },
  default:  { bg: B.surfaceHi,            fg: B.textMid,              dot: B.textMute,             label: "—" },
};
function StatusBadge({ type }) {
  const s = STATUS[type] || STATUS.default;
  return (
    <span style={{
      background: s.bg, color: s.fg, fontSize: 10, fontWeight: 500,
      fontFamily: F.body, padding: "2px 9px", borderRadius: 20,
      whiteSpace: "nowrap", display: "inline-flex", alignItems: "center", gap: 4,
    }}>
      <span style={{ width: 4, height: 4, borderRadius: "50%", background: s.dot, flexShrink: 0 }} />
      {s.label}
    </span>
  );
}

// Urgency pill
function UrgentPill() {
  return (
    <span style={{
      fontSize: 9, color: B.warning, fontFamily: F.body, fontWeight: 600,
      background: "oklch(0.17 0.06 50 / 0.85)", padding: "2px 7px", borderRadius: 20,
      letterSpacing: "0.06em", textTransform: "uppercase", flexShrink: 0,
      border: "1px solid oklch(0.65 0.18 50 / 0.3)", display: "inline-block",
    }}>urgente</span>
  );
}

// Toast
function Toast({ msg, onClose }) {
  const isErr = msg.toLowerCase().includes("error");
  return (
    <div style={{
      position: "fixed", bottom: 24, right: 24, background: B.surface,
      color: B.textPrime, padding: "12px 18px", borderRadius: 10, fontSize: 13,
      fontFamily: F.body, fontWeight: 500,
      border: `1px solid ${isErr ? B.error : B.success}`,
      display: "flex", alignItems: "center", gap: 10, zIndex: 1100, maxWidth: 400,
      boxShadow: "0 8px 24px oklch(0 0 0 / 0.5)",
    }}>
      <span style={{ color: isErr ? B.error : B.success }}>{isErr ? "✕" : "✓"}</span>
      <span style={{ flex: 1 }}>{msg}</span>
      <button onClick={onClose} style={{
        background: "none", border: "none", color: B.textMute,
        cursor: "pointer", fontSize: 16, lineHeight: 1, padding: 0,
      }}>×</button>
    </div>
  );
}

// ─── Header ───────────────────────────────────────────────────────────────────
function Header({ date, focus }) {
  const m = date.match(/(\w+), (\d+) de (\w+) de (\d+)/);
  const dayNum  = m?.[2] || "";
  const dayName = (m?.[1] || "").toUpperCase();
  const month   = (m?.[3] || "").toUpperCase();
  const year    = m?.[4] || "";

  return (
    <div style={{ padding: "24px 20px 20px", borderBottom: `1px solid ${B.line}` }}>
      {/* Date lockup */}
      <div style={{ display: "flex", alignItems: "flex-end", gap: 16, marginBottom: 18 }}>
        <span style={{
          fontFamily: F.display, fontSize: 88, fontWeight: 400, lineHeight: 0.82,
          color: B.primary, letterSpacing: "-0.02em", userSelect: "none",
        }}>{dayNum}</span>
        <div style={{ paddingBottom: 6, display: "flex", flexDirection: "column", gap: 4 }}>
          <span style={{
            fontFamily: F.display, fontSize: 22, fontWeight: 400,
            color: B.textPrime, letterSpacing: "0.05em", lineHeight: 1,
          }}>{dayName}</span>
          <span style={{
            fontFamily: F.body, fontSize: 11, color: B.textMute, letterSpacing: "0.03em",
          }}>{month} · {year}</span>
        </div>
      </div>

      {/* Focus strip — no card, just tinted area */}
      <div style={{
        background: B.primaryFaint,
        border: `1px solid oklch(0.52 0.24 264 / 0.18)`,
        borderRadius: 7, padding: "10px 14px",
        display: "flex", gap: 10, alignItems: "flex-start",
      }}>
        <span style={{ fontSize: 15, flexShrink: 0, lineHeight: 1.5 }}>🔥</span>
        <span style={{ fontSize: 12, color: B.textMid, fontFamily: F.body, lineHeight: 1.6 }}>
          {focus}
        </span>
      </div>
    </div>
  );
}

// ─── Summary ──────────────────────────────────────────────────────────────────
function SummarySection({ items }) {
  const [collapsed, setCollapsed] = useState(false);
  if (!items?.length) return null;
  return (
    <section style={{ padding: "20px 20px 0" }}>
      <SectionLabel icon="⚡" title="Resumen ejecutivo" collapsible collapsed={collapsed} onToggle={() => setCollapsed(c => !c)} />
      <Expand open={!collapsed}>
        <div style={{ display: "flex", flexDirection: "column", gap: 8, paddingBottom: 4 }}>
          {items.map((item, i) => (
            <div key={i} style={{ display: "flex", gap: 12, alignItems: "flex-start" }}>
              <span style={{
                fontFamily: F.display, fontSize: 16, fontWeight: 400,
                color: B.primary, flexShrink: 0, lineHeight: 1.4, minWidth: 20,
              }}>{String(i + 1).padStart(2, "0")}</span>
              <span style={{
                fontSize: 12, color: B.textMid, fontFamily: F.body, lineHeight: 1.65,
              }}>{item}</span>
            </div>
          ))}
        </div>
      </Expand>
    </section>
  );
}

// ─── Tasks ────────────────────────────────────────────────────────────────────
function TaskRow({ task, index, onToggle }) {
  const [open, setOpen] = useState(false);
  const hasWhy = !!task.why;
  const isUrgent = task.urgent && !task.done;

  return (
    <div style={{
      opacity: task.done ? 0.42 : 1,
      transition: "opacity 0.2s",
    }}>
      <div
        className="row-hover"
        onClick={() => hasWhy && setOpen(o => !o)}
        style={{
          display: "flex", alignItems: "flex-start", gap: 10,
          padding: "7px 8px 7px 4px", borderRadius: 5, cursor: hasWhy ? "pointer" : "default",
          background: isUrgent ? "oklch(0.65 0.18 50 / 0.04)" : "transparent",
        }}
      >
        {/* Sequence number in Antonio */}
        <span style={{
          fontFamily: F.display, fontSize: 18, fontWeight: 400,
          color: isUrgent ? B.warning : B.textMute,
          width: 26, flexShrink: 0, lineHeight: 1.1, textAlign: "right",
          paddingTop: 1,
        }}>{String(index + 1).padStart(2, "0")}</span>

        {/* Checkbox */}
        <span
          onClick={e => { e.stopPropagation(); onToggle(); }}
          style={{
            width: 15, height: 15, borderRadius: 3, flexShrink: 0, marginTop: 2,
            border: `1.5px solid ${task.done ? B.success : isUrgent ? B.warning : B.lineHi}`,
            background: task.done ? B.success : "transparent",
            display: "flex", alignItems: "center", justifyContent: "center",
            cursor: "pointer", transition: "all 0.15s", fontSize: 9, color: B.bg,
            fontFamily: F.display,
          }}
        >{task.done ? "✓" : ""}</span>

        {/* Task text */}
        <span style={{ flex: 1, minWidth: 0 }}>
          <span style={{
            fontSize: 12, color: task.done ? B.textMute : B.textPrime,
            fontFamily: F.body, lineHeight: 1.5,
            textDecoration: task.done ? "line-through" : "none",
          }}>
            {isUrgent && <><UrgentPill />{" "}</>}
            {task.text}
          </span>
          <span style={{
            fontSize: 9, color: B.textMute, background: B.surfaceMd,
            padding: "1px 6px", borderRadius: 20, marginLeft: 6,
            fontFamily: F.body, display: "inline-block",
          }}>{task.origin}</span>
        </span>

        {hasWhy && <Chevron open={open} />}
      </div>

      <Expand open={open}>
        <div style={{
          margin: "0 8px 6px 40px",
          padding: "8px 10px",
          fontSize: 11, color: B.textMute, fontFamily: F.body, lineHeight: 1.6,
          background: B.surface, borderRadius: 5,
        }}>
          {task.why}
        </div>
      </Expand>
    </div>
  );
}

function TasksSection({ tasks, onToggleTask }) {
  const [collapsed, setCollapsed] = useState(false);
  const active = tasks.filter(t => !t.done);
  const done   = tasks.filter(t => t.done);
  const ordered = [...active, ...done];

  return (
    <section style={{ padding: "20px 20px 0" }}>
      <SectionLabel icon="✅" title="Tareas" right={`${active.length} pendientes`} collapsible collapsed={collapsed} onToggle={() => setCollapsed(c => !c)} />
      <Expand open={!collapsed}>
        <div>
          <div style={{ display: "flex", flexDirection: "column", gap: 2 }}>
            {ordered.map((t, i) => (
              <TaskRow key={t.id} task={t} index={i} onToggle={() => onToggleTask(t.id)} />
            ))}
          </div>
          {done.length > 0 && active.length > 0 && (
            <div style={{ height: 1, background: B.line, margin: "6px 0", opacity: 0.5 }} />
          )}
        </div>
      </Expand>
    </section>
  );
}

// ─── Calendar (groups conflicts by time) ──────────────────────────────────────
function CalEventRow({ ev, isConflict }) {
  const [open, setOpen] = useState(false);
  return (
    <div>
      <div
        className="row-hover"
        onClick={() => ev.brief && setOpen(o => !o)}
        style={{
          display: "flex", alignItems: "flex-start", gap: 10,
          padding: "5px 8px 5px 4px", borderRadius: 5,
          cursor: ev.brief ? "pointer" : "default",
        }}
      >
        {/* Indent marker for conflict events */}
        {isConflict && (
          <div style={{
            width: 2, alignSelf: "stretch", background: B.lineHi,
            borderRadius: 2, flexShrink: 0, marginTop: 3, marginBottom: 3,
          }} />
        )}

        {/* Title */}
        <div style={{ flex: 1, minWidth: 0 }}>
          {ev.link
            ? <a href={ev.link} target="_blank" rel="noreferrer"
                onClick={e => e.stopPropagation()}
                style={{ fontSize: 13, color: B.textPrime, fontWeight: 600, textDecoration: "none", fontFamily: F.body, lineHeight: 1.4 }}>
                {ev.title}
              </a>
            : <span style={{ fontSize: 13, color: B.textPrime, fontWeight: 600, fontFamily: F.body, lineHeight: 1.4 }}>
                {ev.title}
              </span>
          }
        </div>

        {ev.brief && <Chevron open={open} />}
      </div>

      <Expand open={open}>
        <div style={{
          margin: `0 8px 6px ${isConflict ? 16 : 4}px`,
          padding: "8px 10px",
          fontSize: 11, color: B.textMid, fontFamily: F.body, lineHeight: 1.6,
          background: B.surface, borderRadius: 5,
        }}>
          {ev.brief}
        </div>
      </Expand>
    </div>
  );
}

function CalSection({ events }) {
  const [collapsed, setCollapsed] = useState(false);
  if (!events?.length) return null;

  // Group by time
  const groups = [];
  const seen = {};
  events.forEach(ev => {
    if (!seen[ev.time]) { seen[ev.time] = []; groups.push({ time: ev.time, evs: seen[ev.time] }); }
    seen[ev.time].push(ev);
  });

  return (
    <section style={{ padding: "20px 20px 0" }}>
      <SectionLabel icon="📅" title="Calendario" right={`${events.length} reuniones`} collapsible collapsed={collapsed} onToggle={() => setCollapsed(c => !c)} />
      <Expand open={!collapsed}>
        <div style={{ display: "flex", flexDirection: "column", gap: 14, paddingBottom: 4 }}>
          {groups.map(({ time, evs }) => {
            const isMulti = evs.length > 1;
            return (
              <div key={time} style={{ display: "flex", gap: 0, alignItems: "flex-start" }}>
                {/* Time in Antonio — the visual anchor */}
                <div style={{
                  fontFamily: F.display, fontSize: 26, fontWeight: 400,
                  color: isMulti ? B.warning : B.primary,
                  width: 62, flexShrink: 0, lineHeight: 1,
                  letterSpacing: "-0.02em", paddingTop: 4,
                }}>{time}</div>

                {/* Events */}
                <div style={{ flex: 1, minWidth: 0 }}>
                  {isMulti && (
                    <div style={{
                      fontSize: 9, color: B.warning, fontFamily: F.body, fontWeight: 600,
                      letterSpacing: "0.08em", textTransform: "uppercase",
                      marginBottom: 4, display: "flex", alignItems: "center", gap: 5,
                    }}>
                      <span style={{ width: 4, height: 4, borderRadius: "50%", background: B.warning, display: "inline-block" }} />
                      conflicto · {evs.length} reuniones simultáneas
                    </div>
                  )}
                  <div style={{ display: "flex", flexDirection: "column", gap: 2 }}>
                    {evs.map((ev, i) => (
                      <CalEventRow key={i} ev={ev} isConflict={isMulti} />
                    ))}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </Expand>
    </section>
  );
}

// ─── Emails ───────────────────────────────────────────────────────────────────
function EmailRow({ email, last }) {
  const [open, setOpen] = useState(false);
  const isHigh = email.urgency === "high";
  return (
    <div style={{ borderBottom: last ? "none" : `1px solid ${B.line}` }}>
      <div
        className="row-hover"
        onClick={() => setOpen(o => !o)}
        style={{ display: "flex", alignItems: "center", gap: 8, padding: "8px 6px", borderRadius: 4, cursor: "pointer" }}
      >
        {isHigh && <UrgentPill />}
        <div style={{ flex: 1, minWidth: 0, overflow: "hidden" }}>
          <span style={{ fontSize: 10, color: B.textMute, fontFamily: F.body }}>{email.from}</span>
          {email.subject && (
            <span style={{ fontSize: 11, color: B.textMid, fontFamily: F.body }}>
              {" · "}{email.subject}
            </span>
          )}
        </div>
        <Chevron open={open} />
      </div>
      <Expand open={open}>
        <div style={{
          margin: "0 6px 8px 6px", padding: "8px 10px",
          fontSize: 11, color: isHigh ? B.warning : B.textMid,
          fontFamily: F.body, lineHeight: 1.6,
          background: B.surface, borderRadius: 5,
        }}>
          {email.actionItem}
        </div>
      </Expand>
    </div>
  );
}

function EmailsSection({ emails }) {
  const [collapsed, setCollapsed] = useState(false);
  if (!emails?.length) return null;
  const urgent = emails.filter(e => e.urgency === "high").length;
  return (
    <section style={{ padding: "20px 20px 0" }}>
      <SectionLabel icon="📧" title="Emails" right={urgent > 0 ? `${urgent} urgente${urgent > 1 ? "s" : ""}` : null} collapsible collapsed={collapsed} onToggle={() => setCollapsed(c => !c)} />
      <Expand open={!collapsed}>
        <div>
          {emails.map((e, i) => (
            <EmailRow key={i} email={e} last={i === emails.length - 1} />
          ))}
        </div>
      </Expand>
    </section>
  );
}

// ─── Slack ────────────────────────────────────────────────────────────────────
function SlackRow({ item, last }) {
  const [open, setOpen] = useState(false);
  return (
    <div style={{ borderBottom: last ? "none" : `1px solid ${B.line}` }}>
      <div
        className="row-hover"
        onClick={() => setOpen(o => !o)}
        style={{ display: "flex", alignItems: "center", gap: 8, padding: "8px 6px", borderRadius: 4, cursor: "pointer" }}
      >
        <span style={{
          fontSize: 10, color: B.secondary, fontFamily: F.body, fontWeight: 600, flexShrink: 0,
        }}>
          {item.type === "mention" ? "@mención" : item.type === "dm" ? "DM" : "Thread"}
        </span>
        <span style={{ fontSize: 11, color: B.textMid, fontFamily: F.body, flex: 1, minWidth: 0 }}>
          {item.from}{item.channel && <span style={{ color: B.textMute }}> en {item.channel}</span>}
        </span>
        {item.needsReply && (
          <span style={{ fontSize: 10, color: B.warning, flexShrink: 0 }}>↩</span>
        )}
        <Chevron open={open} />
      </div>
      <Expand open={open}>
        <div style={{
          margin: "0 6px 8px 6px", padding: "8px 10px",
          fontSize: 11, color: B.textMid, fontFamily: F.body, lineHeight: 1.6,
          background: B.surface, borderRadius: 5,
        }}>
          {item.summary}
          {item.needsReply && (
            <div style={{ fontSize: 9, color: B.warning, fontFamily: F.body, fontWeight: 600, marginTop: 4, letterSpacing: "0.04em" }}>
              ↩ necesita respuesta
            </div>
          )}
        </div>
      </Expand>
    </div>
  );
}

function SlackSection({ items }) {
  const [collapsed, setCollapsed] = useState(false);
  if (!items?.length) return null;
  return (
    <section style={{ padding: "20px 20px 0" }}>
      <SectionLabel icon="💬" title="Slack" right={`${items.length} mensajes`} collapsible collapsed={collapsed} onToggle={() => setCollapsed(c => !c)} />
      <Expand open={!collapsed}>
        <div>
          {items.map((s, i) => (
            <SlackRow key={i} item={s} last={i === items.length - 1} />
          ))}
        </div>
      </Expand>
    </section>
  );
}

// ─── Jira ─────────────────────────────────────────────────────────────────────
function JiraSection({ jira }) {
  const [collapsed, setCollapsed] = useState(false);
  if (!jira) return null;
  return (
    <section style={{ padding: "20px 20px 0" }}>
      <SectionLabel icon="🎯" title="Jira" collapsible collapsed={collapsed} onToggle={() => setCollapsed(c => !c)} />

      <Expand open={!collapsed}>
        <div style={{ paddingBottom: 4 }}>
          {/* Stats row — numbers in Antonio */}
          <div style={{ display: "flex", gap: 24, marginBottom: 16 }}>
            <div>
              <span style={{
                fontFamily: F.display, fontSize: 44, fontWeight: 400,
                color: B.textPrime, lineHeight: 1, letterSpacing: "-0.02em",
              }}>{jira.totalActive}</span>
              <div style={{ fontSize: 10, color: B.textMute, fontFamily: F.body, marginTop: 2, letterSpacing: "0.04em", textTransform: "uppercase" }}>
                activos
              </div>
            </div>
            <div style={{ width: 1, background: B.line, alignSelf: "stretch" }} />
            <div>
              <span style={{
                fontFamily: F.display, fontSize: 44, fontWeight: 400,
                color: B.warning, lineHeight: 1, letterSpacing: "-0.02em",
              }}>{jira.highPriority}</span>
              <div style={{ fontSize: 10, color: B.textMute, fontFamily: F.body, marginTop: 2, letterSpacing: "0.04em", textTransform: "uppercase" }}>
                alta prioridad
              </div>
            </div>
          </div>

          {/* Issue list */}
          <div style={{ display: "flex", flexDirection: "column", gap: 7 }}>
            {(jira.updatedYesterday || []).map(issue => (
              <div key={issue.key} style={{
                display: "flex", alignItems: "center", gap: 8,
                padding: "4px 0",
              }}>
                <a
                  href={`https://procontacto.atlassian.net/browse/${issue.key}`}
                  target="_blank" rel="noreferrer"
                  style={{
                    fontSize: 10, fontWeight: 600, color: B.primary,
                    background: B.primaryFaint, padding: "3px 9px", borderRadius: 20,
                    textDecoration: "none", fontFamily: F.body,
                    border: "1px solid oklch(0.52 0.24 264 / 0.25)",
                    whiteSpace: "nowrap", flexShrink: 0,
                  }}
                >{issue.key}</a>
                <span style={{
                  fontSize: 11, color: B.textMid, fontFamily: F.body,
                  flex: 1, minWidth: 0, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap",
                }}>{issue.summary}</span>
                <StatusBadge type={issue.statusType} />
              </div>
            ))}
          </div>
        </div>
      </Expand>
    </section>
  );
}

// ─── App ──────────────────────────────────────────────────────────────────────
export default function App() {
  const [tasks, setTasks] = useState(BRIEFING_DATA.tasks || []);
  const [toast, setToast] = useState(null);

  const toggleTask = id => setTasks(prev => prev.map(t => t.id === id ? { ...t, done: !t.done } : t));
  const hasSlack = (BRIEFING_DATA.slack || []).length > 0;

  return (
    <div style={{ background: B.bg, minHeight: "100vh", color: B.textPrime, fontFamily: F.body }}>
      <div style={{ maxWidth: 1120, margin: "0 auto" }}>
        <Header date={BRIEFING_DATA.date} focus={BRIEFING_DATA.focus} />
        <SummarySection items={BRIEFING_DATA.summary} />

        {/* 2-column grid: calendar left | action panel right */}
        <div style={{
          display: "grid",
          gridTemplateColumns: "1.1fr 0.9fr",
          alignItems: "start",
          borderTop: `1px solid ${B.line}`,
          marginTop: 20,
        }}>
          {/* Left — Calendar */}
          <div style={{ borderRight: `1px solid ${B.line}`, paddingBottom: 40 }}>
            <CalSection events={BRIEFING_DATA.calendar} />
          </div>

          {/* Right — Action panel */}
          <div style={{ paddingBottom: 40 }}>
            <TasksSection tasks={tasks} onToggleTask={toggleTask} />
            <EmailsSection emails={BRIEFING_DATA.emails} />
            {hasSlack && <SlackSection items={BRIEFING_DATA.slack} />}
            <JiraSection jira={BRIEFING_DATA.jira} />
          </div>
        </div>
      </div>

      {toast && <Toast msg={toast} onClose={() => setToast(null)} />}

      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Antonio:wght@400;600&family=Figtree:wght@400;500;600&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        a:hover { opacity: 0.75; transition: opacity 0.15s; }
        .row-hover:hover { background: oklch(0.135 0.009 264) !important; transition: background 0.12s; }
      `}</style>
    </div>
  );
}
