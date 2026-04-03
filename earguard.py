import streamlit as st
import time
from datetime import datetime
import math

st.set_page_config(
    page_title="EarGuard",
    page_icon="🎧",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #1a1a1a;
    color: #e0e0e0;
}
.stApp { background-color: #1a1a1a; }
section[data-testid="stSidebar"] { display: none; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 0 80px 0 !important; max-width: 480px; margin: 0 auto; }

.eg-card {
    background: #2a2a2a; border-radius: 14px;
    padding: 18px 20px; margin-bottom: 12px; border: 1px solid #333;
}
.eg-card-title {
    font-size: 11px; font-weight: 600; letter-spacing: 0.12em;
    color: #666; text-transform: uppercase; margin-bottom: 14px;
}
.eg-header {
    background: #2a2a2a; padding: 16px 20px;
    display: flex; justify-content: space-between; align-items: center;
    border-bottom: 1px solid #333; margin-bottom: 12px;
}
.eg-logo { font-size: 18px; font-weight: 600; color: #f0f0f0; }
.badge-safe    { background:#1a3a2a; color:#4ade80; padding:3px 12px; border-radius:99px; font-size:12px; font-weight:500; }
.badge-caution { background:#3a2e1a; color:#EF9F27; padding:3px 12px; border-radius:99px; font-size:12px; font-weight:500; }
.badge-danger  { background:#3a1a1a; color:#f87171; padding:3px 12px; border-radius:99px; font-size:12px; font-weight:500; }
.badge-speaker { background:#1a2535; color:#60a5fa; padding:3px 12px; border-radius:99px; font-size:12px; font-weight:500; }

.metric-grid { display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:12px; }
.metric-box  { background:#2a2a2a; border-radius:12px; padding:14px 16px; border:1px solid #333; }
.metric-lbl  { font-size:12px; color:#666; margin-bottom:4px; }
.metric-val  { font-size:22px; font-weight:500; color:#f0f0f0; }

.vol-track { background:#3a3a3a; border-radius:99px; height:6px; overflow:hidden; margin:8px 0 4px; }
.vol-fill  { height:100%; border-radius:99px; }

.prog-track { background:#3a3a3a; border-radius:99px; height:10px; overflow:hidden; margin:10px 0 4px; }
.prog-fill  { height:100%; border-radius:99px; }

.alert-warn   { background:#2e2510; border-left:3px solid #EF9F27; border-radius:8px; padding:10px 14px; margin:8px 0; font-size:13px; color:#EF9F27; }
.alert-danger { background:#2e1010; border-left:3px solid #f87171; border-radius:8px; padding:10px 14px; margin:8px 0; font-size:13px; color:#f87171; }
.alert-safe   { background:#102e1a; border-left:3px solid #4ade80; border-radius:8px; padding:10px 14px; margin:8px 0; font-size:13px; color:#4ade80; }
.alert-info   { background:#1a2535; border-left:3px solid #60a5fa; border-radius:8px; padding:10px 14px; margin:8px 0; font-size:13px; color:#60a5fa; }

.timer-big { font-family:'DM Mono',monospace; font-size:52px; font-weight:500;
             color:#EF9F27; text-align:center; letter-spacing:0.05em; }
.timer-sub { font-size:12px; color:#555; text-align:center; margin-top:-4px; margin-bottom:8px; }
.dose-label { font-size:11px; color:#555; text-align:right; margin-top:2px; }

.log-entry { display:flex; justify-content:space-between; align-items:center;
             padding:10px 0; border-bottom:1px solid #2e2e2e; font-size:13px; }
.log-entry:last-child { border-bottom:none; }
.log-dot-safe   { width:8px; height:8px; border-radius:50%; background:#4ade80; flex-shrink:0; }
.log-dot-danger { width:8px; height:8px; border-radius:50%; background:#f87171; flex-shrink:0; }
.log-dot-warn   { width:8px; height:8px; border-radius:50%; background:#EF9F27; flex-shrink:0; }

.chart-wrap { display:flex; align-items:flex-end; gap:7px; height:70px; margin-bottom:6px; }
.bar-col    { display:flex; flex-direction:column; align-items:center; gap:3px; flex:1; }
.bar-rect   { width:100%; border-radius:3px 3px 0 0; }
.bar-lbl    { font-size:10px; color:#666; }
.bar-val    { font-size:9px; color:#888; }

.score-big  { font-size:52px; font-weight:600; line-height:1; }
.score-desc { font-size:14px; color:#ccc; margin-top:2px; }
.score-sub  { font-size:12px; color:#555; margin-top:2px; }

.toggle-lbl { font-size:14px; color:#e0e0e0; }
.toggle-sub { font-size:11px; color:#555; margin-top:2px; }

.stButton>button {
    width:100%; background:#EF9F27 !important; color:#1a1a1a !important;
    border:none !important; border-radius:12px !important; height:48px !important;
    font-size:15px !important; font-weight:600 !important; font-family:'DM Sans',sans-serif !important;
}
.stop-btn .stButton>button { background:#3a3a3a !important; color:#e0e0e0 !important; }
div[data-testid="stSelectbox"]>div>div {
    background:#333 !important; border:1px solid #444 !important;
    border-radius:8px !important; color:#e0e0e0 !important;
}
div[data-testid="metric-container"] { display:none; }
.stSlider label   { display:none !important; }
.stSelectbox label { display:none !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state defaults ───────────────────────────────────────────────────
defaults = {
    "session_active":   False,
    "start_time":       None,
    "last_tick":        None,
    "dose":             0.0,      # cumulative 0.0 → 1.0+
    "elapsed_seconds":  0.0,
    "session_log":      [],
    "enforce_breaks":   True,
    "gradual_warnings": True,
    "hard_cutoff":      False,
    "break_duration":   "10 min",
    "daily_limit":      "3 hr",
    "rule_preset":      "60/60",
    "volume":           72,
    "output_type":      "In-ear headphones",
    "warned_75":        False,
    "warned_90":        False,
    "warned_100":       False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Core functions ───────────────────────────────────────────────────────────
def safe_minutes(volume, output_type, preset="60/60"):
    if output_type == "Speaker":
        return 9999
    bv = 0.6 if preset == "60/60" else 0.8
    bm = 60  if preset == "60/60" else 80
    ratio = max(volume, 1) / 100
    return min(round(bm * (bv / ratio) ** 2), 120)

def get_status(volume, output_type):
    if output_type == "Speaker": return "speaker",  "Speaker"
    if volume <  60:             return "safe",      "Safe"
    if volume < 80:              return "caution",   "Caution"
    return "danger", "Loud"

def dose_color(dose):
    """Smooth green → amber → red interpolation."""
    d = min(dose, 1.0)
    if d < 0.6:
        t = d / 0.6
        r = int(0x4a + (0xEF - 0x4a) * t)
        g = int(0xde + (0x9F - 0xde) * t)
        b = int(0x80 + (0x27 - 0x80) * t)
    else:
        t = (d - 0.6) / 0.4
        r = int(0xEF + (0xf8 - 0xEF) * t)
        g = int(0x9F + (0x71 - 0x9F) * t)
        b = int(0x27 + (0x71 - 0x27) * t)
    return f"#{min(r,255):02x}{min(g,255):02x}{min(b,255):02x}"

def fmt_duration(seconds):
    m, s = int(seconds // 60), int(seconds % 60)
    return f"{m:02d}:{s:02d}"

def fmt_mins(mins):
    if mins >= 9999: return "∞"
    if mins >= 60:
        h, m = mins // 60, mins % 60
        return f"{h}h {m}m" if m else f"{h}h"
    return f"{mins}m"

def ring_svg(dose, centre, sub, color):
    r    = 62
    circ = 2 * math.pi * r
    rem  = max(0.0, 1.0 - dose)
    dash = circ * rem
    gap  = circ - dash
    return f"""
    <div style="display:flex;flex-direction:column;align-items:center;padding:8px 0 4px;">
      <svg width="170" height="170" viewBox="0 0 160 160">
        <circle cx="80" cy="80" r="{r}" fill="none" stroke="#3a3a3a" stroke-width="11"/>
        <circle cx="80" cy="80" r="{r}" fill="none" stroke="{color}" stroke-width="11"
          stroke-dasharray="{dash:.2f} {gap:.2f}" stroke-linecap="round"
          transform="rotate(-90 80 80)"/>
        <text x="80" y="72" text-anchor="middle" fill="#f0f0f0"
          font-family="DM Sans,sans-serif" font-size="26" font-weight="500">{centre}</text>
        <text x="80" y="94" text-anchor="middle" fill="#666"
          font-family="DM Sans,sans-serif" font-size="12">{sub}</text>
      </svg>
      <div style="font-size:13px;color:#555;margin-top:2px;">Cumulative ear exposure</div>
    </div>"""

def tick_dose():
    """
    Advance cumulative dose.
    dose += delta_seconds / safe_limit_seconds_at_current_volume
    Changing volume mid-session changes the RATE, not the accumulated dose.
    This closes the 'lower volume to reset' loophole entirely.
    """
    now = time.time()
    if st.session_state.last_tick is None:
        st.session_state.last_tick = now
        return
    delta = now - st.session_state.last_tick
    st.session_state.last_tick       = now
    st.session_state.elapsed_seconds += delta
    limit_s = safe_minutes(
        st.session_state.volume,
        st.session_state.output_type,
        st.session_state.rule_preset
    ) * 60
    st.session_state.dose = min(st.session_state.dose + delta / limit_s, 1.05)

def end_session():
    st.session_state.session_log.append({
        "time":       datetime.now().strftime("%H:%M"),
        "device":     st.session_state.output_type,
        "volume":     st.session_state.volume,
        "duration":   round(st.session_state.elapsed_seconds / 60, 1),
        "dose":       round(min(st.session_state.dose, 1.0) * 100),
        "over_limit": st.session_state.dose >= 1.0,
    })
    for k in ["session_active","start_time","last_tick","dose","elapsed_seconds",
              "warned_75","warned_90","warned_100"]:
        st.session_state[k] = defaults[k]

# ── Tick if session running ──────────────────────────────────────────────────
if st.session_state.session_active:
    tick_dose()

# ── Derived values ───────────────────────────────────────────────────────────
dose      = st.session_state.dose
cur_safe  = safe_minutes(st.session_state.volume, st.session_state.output_type, st.session_state.rule_preset)
status_k, status_l = get_status(st.session_state.volume, st.session_state.output_type)
arc_col   = dose_color(dose) if st.session_state.session_active else "#EF9F27"

if st.session_state.session_active:
    rem_mins    = math.ceil(max(0.0, 1.0 - dose) * cur_safe)
    ring_centre = fmt_mins(rem_mins)
    ring_sub    = "remaining"
else:
    ring_centre = fmt_mins(cur_safe)
    ring_sub    = "at this volume"
    dose        = 0.0

# ── Header ───────────────────────────────────────────────────────────────────
badge_map = {"safe":"badge-safe","caution":"badge-caution","danger":"badge-danger","speaker":"badge-speaker"}
st.markdown(f"""
<div class="eg-header">
  <span class="eg-logo">🎧 EarGuard</span>
  <span class="{badge_map[status_k]}">{status_l}</span>
</div>""", unsafe_allow_html=True)

tab_home, tab_stats, tab_settings = st.tabs(["◎  Home", "▦  Stats", "⚙  Settings"])

# ═════════════════════════════════════════════════════════════════════════════
# HOME
# ═════════════════════════════════════════════════════════════════════════════
with tab_home:

    # Ring
    st.markdown(f'<div class="eg-card">{ring_svg(dose, ring_centre, ring_sub, arc_col)}</div>',
                unsafe_allow_html=True)

    # Output device
    out_opts = ["In-ear headphones","Over-ear headphones","Bluetooth headphones","Speaker"]
    st.markdown('<div class="eg-card"><div class="eg-card-title">Output device</div>', unsafe_allow_html=True)
    sel = st.selectbox("out", out_opts,
                       index=out_opts.index(st.session_state.output_type),
                       key="out_sel", label_visibility="collapsed")
    if sel != st.session_state.output_type:
        st.session_state.output_type = sel
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Volume
    vc = "#4ade80" if st.session_state.volume <= 60 else "#EF9F27" if st.session_state.volume <= 80 else "#f87171"
    st.markdown(f"""
    <div class="eg-card">
      <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
        <span style="font-size:14px;font-weight:500;">Volume</span>
        <span style="font-size:14px;font-weight:500;color:{vc};">{st.session_state.volume}%</span>
      </div>
      <div class="vol-track"><div class="vol-fill" style="width:{st.session_state.volume}%;background:{vc};"></div></div>""",
        unsafe_allow_html=True)
    new_vol = st.slider("vol", 0, 100, st.session_state.volume, key="vol_sl", label_visibility="collapsed")
    st.markdown('<p style="font-size:12px;color:#444;margin-top:4px;">Drag to set volume level</p></div>',
                unsafe_allow_html=True)
    if new_vol != st.session_state.volume:
        st.session_state.volume = new_vol
        # dose intentionally NOT reset — only the accumulation rate changes
        st.rerun()

    # Status banner
    banners = {
        "speaker": ('<div class="alert-info">📢 Speaker mode — no ear tracking needed.</div>', ),
        "safe":    ('<div class="alert-safe">✓ Within safe listening range.</div>', ),
        "caution": ('<div class="alert-warn">⚠ Caution — consider lowering volume.</div>', ),
        "danger":  ('<div class="alert-danger">⬤ Loud — dose accumulating fast.</div>', ),
    }
    st.markdown(banners[status_k][0], unsafe_allow_html=True)

    # Quick stats
    total_today = sum(s["duration"] for s in st.session_state.session_log)
    sessions_n  = len(st.session_state.session_log)
    st.markdown(f"""
    <div class="metric-grid">
      <div class="metric-box"><div class="metric-lbl">Today</div>
        <div class="metric-val">{fmt_mins(round(total_today))}</div></div>
      <div class="metric-box"><div class="metric-lbl">Sessions</div>
        <div class="metric-val">{sessions_n}</div></div>
    </div>""", unsafe_allow_html=True)

    # Session tracker
    st.markdown('<div class="eg-card"><div class="eg-card-title">Session tracker</div>', unsafe_allow_html=True)

    if status_k == "speaker":
        st.markdown('<p style="color:#555;font-size:13px;">Tracking paused — speaker in use.</p>', unsafe_allow_html=True)

    elif not st.session_state.session_active:
        if st.button("▶  Start listening session"):
            st.session_state.session_active  = True
            st.session_state.start_time      = time.time()
            st.session_state.last_tick       = time.time()
            st.session_state.dose            = 0.0
            st.session_state.elapsed_seconds = 0.0
            st.session_state.warned_75       = False
            st.session_state.warned_90       = False
            st.session_state.warned_100      = False
            st.rerun()
    else:
        d        = st.session_state.dose
        prog_col = dose_color(d)

        st.markdown(f'<div class="timer-big">{fmt_duration(st.session_state.elapsed_seconds)}</div>', unsafe_allow_html=True)
        st.markdown('<div class="timer-sub">session duration</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="prog-track">
          <div class="prog-fill" style="width:{min(d,1)*100:.1f}%;background:{prog_col};"></div>
        </div>
        <div class="dose-label">
          Ear dose: {min(d*100,100):.0f}% &nbsp;·&nbsp; rate: {fmt_mins(cur_safe)} limit at {st.session_state.volume}% vol
        </div>""", unsafe_allow_html=True)

        # Progressive warnings
        if d >= 1.0:
            if not st.session_state.warned_100:
                st.session_state.warned_100 = True
            st.markdown('<div class="alert-danger">🔴 Ear dose full — take a break now!</div>', unsafe_allow_html=True)
        elif d >= 0.9:
            if not st.session_state.warned_90:
                st.session_state.warned_90 = True
            st.markdown('<div class="alert-danger">⚠ 90% dose reached — finish up soon.</div>', unsafe_allow_html=True)
        elif d >= 0.75:
            if not st.session_state.warned_75:
                st.session_state.warned_75 = True
            st.markdown('<div class="alert-warn">⚠ 75% dose reached — consider a break.</div>', unsafe_allow_html=True)

        if d >= 1.0 and st.session_state.hard_cutoff:
            end_session()
            st.rerun()

        st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="stop-btn">', unsafe_allow_html=True)
        if st.button("⏹  End session"):
            end_session()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        time.sleep(0.5)   # 0.5s = snappy but not hammering the CPU
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Today's log
    st.markdown('<div class="eg-card"><div class="eg-card-title">Today\'s log</div>', unsafe_allow_html=True)
    if st.session_state.session_log:
        for s in reversed(st.session_state.session_log):
            dot = "log-dot-danger" if s["over_limit"] else "log-dot-warn" if s["dose"] >= 75 else "log-dot-safe"
            st.markdown(f"""
            <div class="log-entry">
              <div style="display:flex;align-items:center;gap:10px;">
                <div class="{dot}"></div>
                <div>
                  <div style="color:#e0e0e0;">{s['time']} · {s['device']}</div>
                  <div style="font-size:11px;color:#555;">{s['volume']}% vol · dose: {s['dose']}%</div>
                </div>
              </div>
              <div style="color:#888;font-size:13px;">{s['duration']} min</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:#555;font-size:13px;">No sessions yet today.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# STATS
# ═════════════════════════════════════════════════════════════════════════════
with tab_stats:

    days   = ['M','T','W','T','F','S','S']
    hours  = [1.2, 2.8, 1.0, 3.4, 0.8, 2.1, 1.4]
    colors = ['#4ade80','#f87171','#4ade80','#f87171','#4ade80','#EF9F27','#4ade80']
    today_h = sum(s["duration"] for s in st.session_state.session_log) / 60
    hours[6]  = round(today_h, 1)
    colors[6] = '#f87171' if today_h > 3 else '#EF9F27' if today_h > 2 else '#4ade80'
    max_h = max(hours) if max(hours) > 0 else 1

    bars = "".join(
        f'<div class="bar-col"><div class="bar-val">{h}h</div>'
        f'<div class="bar-rect" style="height:{max(4,int(h/max_h*52))}px;background:{c};"></div>'
        f'<div class="bar-lbl">{d}</div></div>'
        for d, h, c in zip(days, hours, colors)
    )
    legend = """<div style="display:flex;gap:12px;margin-top:10px;flex-wrap:wrap;">
      <span style="font-size:11px;color:#555;display:flex;align-items:center;gap:4px;">
        <span style="width:8px;height:8px;border-radius:2px;background:#4ade80;display:inline-block"></span>Safe</span>
      <span style="font-size:11px;color:#555;display:flex;align-items:center;gap:4px;">
        <span style="width:8px;height:8px;border-radius:2px;background:#EF9F27;display:inline-block"></span>Warning</span>
      <span style="font-size:11px;color:#555;display:flex;align-items:center;gap:4px;">
        <span style="width:8px;height:8px;border-radius:2px;background:#f87171;display:inline-block"></span>Over limit</span>
    </div>"""

    st.markdown(f'<div class="eg-card"><div class="eg-card-title">This week</div>'
                f'<div class="chart-wrap">{bars}</div>{legend}</div>', unsafe_allow_html=True)

    avg_vol = round(sum(s["volume"] for s in st.session_state.session_log) /
                    len(st.session_state.session_log)) if st.session_state.session_log else 68
    over_n  = sum(1 for s in st.session_state.session_log if s["over_limit"])

    st.markdown(f"""
    <div class="metric-grid">
      <div class="metric-box"><div class="metric-lbl">Weekly avg</div><div class="metric-val">1h 41m</div></div>
      <div class="metric-box"><div class="metric-lbl">Safe days</div><div class="metric-val">{max(0,7-over_n)} / 7</div></div>
      <div class="metric-box"><div class="metric-lbl">Avg volume</div><div class="metric-val">{avg_vol}%</div></div>
      <div class="metric-box"><div class="metric-lbl">Breaks taken</div><div class="metric-val">{sessions_n}</div></div>
    </div>""", unsafe_allow_html=True)

    score  = max(30, min(100, 100 - over_n * 8 - max(0, avg_vol - 60) // 5))
    sc_col = "#4ade80" if score >= 70 else "#EF9F27" if score >= 50 else "#f87171"
    sc_msg = "Good — keep it up" if score >= 70 else "Fair — try lower volumes" if score >= 50 else "Poor — take more breaks"

    st.markdown(f"""
    <div class="eg-card">
      <div class="eg-card-title">Ear health score</div>
      <div style="display:flex;align-items:center;gap:16px;">
        <div class="score-big" style="color:{sc_col};">{score}</div>
        <div><div class="score-desc">{sc_msg}</div>
          <div class="score-sub">Based on volume + duration habits</div></div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="eg-card">
      <div class="eg-card-title">About the dose model</div>
      <p style="font-size:13px;color:#666;line-height:1.7;">
        EarGuard tracks <span style="color:#EF9F27;">cumulative ear dose</span>, not a simple countdown timer.
        Lowering your volume mid-session slows how fast dose accumulates —
        but <span style="color:#f87171;">never resets it</span>.
        This is based on the ISO 1999 noise exposure standard used by audiologists.
      </p>
      <p style="font-size:13px;color:#555;line-height:1.8;margin-top:8px;">
        60% volume → full dose in 60 min<br>
        80% volume → full dose in ~34 min<br>
        100% volume → full dose in ~22 min
      </p>
    </div>""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# SETTINGS
# ═════════════════════════════════════════════════════════════════════════════
with tab_settings:

    st.markdown('<div class="eg-card"><div class="eg-card-title">Limiter mode</div>', unsafe_allow_html=True)
    for key, lbl, sub in [
        ("enforce_breaks",   "Enforce breaks",   "Remind when limit reached"),
        ("gradual_warnings", "Gradual warnings", "Notify at 75%, 90%, 100%"),
        ("hard_cutoff",      "Hard cutoff",      "Force end session at limit"),
    ]:
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f'<div class="toggle-lbl">{lbl}</div><div class="toggle-sub">{sub}</div>', unsafe_allow_html=True)
        with c2:
            st.session_state[key] = st.toggle(key, value=st.session_state[key], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="eg-card"><div class="eg-card-title">Breaks</div>', unsafe_allow_html=True)
    for key, lbl, opts in [
        ("break_duration", "Break duration", ["5 min","10 min","15 min","20 min"]),
        ("daily_limit",    "Daily limit",    ["1 hr","2 hr","3 hr","No limit"]),
    ]:
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown(f'<div class="toggle-lbl">{lbl}</div>', unsafe_allow_html=True)
        with c2:
            st.session_state[key] = st.selectbox(key, opts,
                index=opts.index(st.session_state[key]), label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="eg-card"><div class="eg-card-title">Rule preset</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown('<div class="toggle-lbl">Base rule</div><div class="toggle-sub">WHO 60/60 guideline</div>', unsafe_allow_html=True)
    with c2:
        presets = ["60/60","80/80","Custom"]
        st.session_state.rule_preset = st.selectbox(
            "rp", presets, index=presets.index(st.session_state.rule_preset),
            label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)
    if st.button("🗑  Clear today's data"):
        for k in ["session_log","session_active","start_time","last_tick",
                  "dose","elapsed_seconds","warned_75","warned_90","warned_100"]:
            st.session_state[k] = defaults[k]
        st.rerun()

    st.markdown("""
    <div style="text-align:center;color:#333;font-size:11px;margin-top:20px;">
      EarGuard · WHO 60/60 · ISO 1999 dose model · v1.1
    </div>""", unsafe_allow_html=True)


#python -m streamlit run "c:/Users/kavya/Journey/Self Projects/earguard.py"