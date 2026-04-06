import streamlit as st
import os
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
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background-color: #0f0f0f;
    color: #e0e0e0;
}
.stApp { background-color: #0f0f0f; }
section[data-testid="stSidebar"] { display: none; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 0 80px 0 !important; max-width: 480px; margin: 0 auto; }

.eg-card {
    background: linear-gradient(145deg, #1c1c1c, #161616);
    border-radius: 20px;
    padding: 20px 22px;
    margin-bottom: 12px;
    border: 1px solid #2a2a2a;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
}
.eg-card-title {
    font-size: 10px; font-weight: 700; letter-spacing: 0.18em;
    color: #444; text-transform: uppercase; margin-bottom: 14px;
}
.eg-header {
    background: linear-gradient(180deg, #1a1a1a 0%, #141414 100%);
    padding: 18px 22px;
    display: flex; justify-content: space-between; align-items: center;
    border-bottom: 1px solid #222; margin-bottom: 14px;
}
.eg-logo { font-size: 17px; font-weight: 700; color: #f5f5f5; letter-spacing: -0.02em; }
.eg-logo span { color: #EF9F27; }

.badge-safe    { background:rgba(74,222,128,0.12);  color:#4ade80; padding:4px 14px; border-radius:99px; font-size:11px; font-weight:600; border:1px solid rgba(74,222,128,0.2);  letter-spacing:0.06em; }
.badge-caution { background:rgba(239,159,39,0.12);  color:#EF9F27; padding:4px 14px; border-radius:99px; font-size:11px; font-weight:600; border:1px solid rgba(239,159,39,0.2);  letter-spacing:0.06em; }
.badge-danger  { background:rgba(248,113,113,0.12); color:#f87171; padding:4px 14px; border-radius:99px; font-size:11px; font-weight:600; border:1px solid rgba(248,113,113,0.2); letter-spacing:0.06em; }
.badge-speaker { background:rgba(96,165,250,0.12);  color:#60a5fa; padding:4px 14px; border-radius:99px; font-size:11px; font-weight:600; border:1px solid rgba(96,165,250,0.2);  letter-spacing:0.06em; }

.metric-grid { display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:12px; }
.metric-box  { background:linear-gradient(145deg,#1c1c1c,#161616); border-radius:14px; padding:16px 18px; border:1px solid #2a2a2a; }
.metric-lbl  { font-size:11px; color:#444; margin-bottom:6px; font-weight:600; letter-spacing:0.1em; text-transform:uppercase; }
.metric-val  { font-size:24px; font-weight:600; color:#f0f0f0; letter-spacing:-0.02em; }

.vol-track { background:#222; border-radius:99px; height:5px; overflow:hidden; margin:8px 0 4px; }
.vol-fill  { height:100%; border-radius:99px; }
.prog-track { background:#222; border-radius:99px; height:8px; overflow:hidden; margin:12px 0 4px; }
.prog-fill  { height:100%; border-radius:99px; }

.alert-warn   { background:rgba(239,159,39,0.08);  border-left:3px solid #EF9F27; border-radius:10px; padding:12px 16px; margin:8px 0; font-size:13px; color:#EF9F27; }
.alert-danger { background:rgba(248,113,113,0.08); border-left:3px solid #f87171; border-radius:10px; padding:12px 16px; margin:8px 0; font-size:13px; color:#f87171; }
.alert-safe   { background:rgba(74,222,128,0.08);  border-left:3px solid #4ade80; border-radius:10px; padding:12px 16px; margin:8px 0; font-size:13px; color:#4ade80; }
.alert-info   { background:rgba(96,165,250,0.08);  border-left:3px solid #60a5fa; border-radius:10px; padding:12px 16px; margin:8px 0; font-size:13px; color:#60a5fa; }

.timer-big { font-family:'JetBrains Mono',monospace; font-size:54px; font-weight:500; color:#EF9F27; text-align:center; letter-spacing:0.04em; text-shadow:0 0 40px rgba(239,159,39,0.3); }
.timer-sub { font-size:11px; color:#444; text-align:center; margin-top:-4px; margin-bottom:10px; letter-spacing:0.12em; text-transform:uppercase; }
.dose-label { font-size:11px; color:#444; text-align:right; margin-top:4px; }

.log-entry { display:flex; justify-content:space-between; align-items:center; padding:11px 0; border-bottom:1px solid #1e1e1e; font-size:13px; }
.log-entry:last-child { border-bottom:none; }
.log-dot-safe   { width:7px; height:7px; border-radius:50%; background:#4ade80; flex-shrink:0; box-shadow:0 0 6px rgba(74,222,128,0.6); }
.log-dot-danger { width:7px; height:7px; border-radius:50%; background:#f87171; flex-shrink:0; box-shadow:0 0 6px rgba(248,113,113,0.6); }
.log-dot-warn   { width:7px; height:7px; border-radius:50%; background:#EF9F27; flex-shrink:0; box-shadow:0 0 6px rgba(239,159,39,0.6); }

.chart-wrap { display:flex; align-items:flex-end; gap:8px; height:80px; margin-bottom:6px; }
.bar-col    { display:flex; flex-direction:column; align-items:center; gap:4px; flex:1; }
.bar-rect   { width:100%; border-radius:4px 4px 0 0; }
.bar-lbl    { font-size:10px; color:#444; font-weight:600; }
.bar-val    { font-size:9px; color:#555; }

.score-big  { font-size:56px; font-weight:700; line-height:1; letter-spacing:-0.03em; }
.score-desc { font-size:14px; color:#ccc; margin-top:4px; font-weight:500; }
.score-sub  { font-size:11px; color:#444; margin-top:3px; }

.toggle-lbl { font-size:14px; color:#e0e0e0; font-weight:500; }
.toggle-sub { font-size:11px; color:#444; margin-top:2px; }

.stButton>button {
    width:100%;
    background:linear-gradient(135deg,#EF9F27 0%,#d4891a 100%) !important;
    color:#0f0f0f !important; border:none !important; border-radius:14px !important;
    height:50px !important; font-size:14px !important; font-weight:700 !important;
    font-family:'Space Grotesk',sans-serif !important; letter-spacing:0.04em !important;
    box-shadow:0 4px 20px rgba(239,159,39,0.25) !important;
}
.stop-btn .stButton>button {
    background:#1e1e1e !important; color:#888 !important;
    box-shadow:none !important; border:1px solid #2a2a2a !important;
}
div[data-testid="stSelectbox"]>div>div {
    background:#1a1a1a !important; border:1px solid #2a2a2a !important;
    border-radius:10px !important; color:#e0e0e0 !important;
}
div[data-testid="metric-container"] { display:none; }
.stSlider label    { display:none !important; }
.stSelectbox label { display:none !important; }

@keyframes pulse-glow {
    0%   { opacity:0.5; }
    50%  { opacity:1.0; }
    100% { opacity:0.5; }
}
</style>
""", unsafe_allow_html=True)

# ── Session state defaults ───────────────────────────────────────────────────
defaults = {
    "session_active":   False,
    "start_time":       None,
    "last_tick":        None,
    "dose":             0.0,
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
    if output_type == "Speaker": return "speaker", "Speaker"
    if volume < 60:              return "safe",     "Safe"
    if volume < 80:              return "caution",  "Caution"
    return "danger", "Loud"

def dose_color(dose):
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

def build_ring(dose, centre, sub, color, is_active):
    R      = 68
    CX, CY = 90, 90
    circ   = 2 * math.pi * R
    filled = min(dose, 1.0)
    dash   = round(circ * filled, 2)
    gap    = round(circ - dash, 2)
    pct    = int(filled * 100)
    glow_opacity = round(0.12 + filled * 0.28, 2)

    # pulse style
    pulse = ""
    if is_active and filled > 0:
        speed = round(max(1.2, 3.0 - filled * 2.0), 1)
        pulse = "animation:pulse-glow " + str(speed) + "s ease-in-out infinite;"

    # build tick marks as plain string
    ticks = ""
    for i in range(10):
        angle_rad = math.radians(-90 + i * 36)
        ox = round(CX + (R + 10) * math.cos(angle_rad), 1)
        oy = round(CY + (R + 10) * math.sin(angle_rad), 1)
        ix = round(CX + (R + 5)  * math.cos(angle_rad), 1)
        iy = round(CY + (R + 5)  * math.sin(angle_rad), 1)
        tc = color if (i / 10) <= filled else "#2a2a2a"
        ticks += ('<line x1="' + str(ox) + '" y1="' + str(oy) + '" '
                  'x2="' + str(ix) + '" y2="' + str(iy) + '" '
                  'stroke="' + tc + '" stroke-width="2" stroke-linecap="round"/>')

    # leading edge dot
    lead_dot = ""
    if 0.01 < filled < 1.0:
        la = math.radians(-90 + filled * 360)
        dx = round(CX + R * math.cos(la), 1)
        dy = round(CY + R * math.sin(la), 1)
        lead_dot = ('<circle cx="' + str(dx) + '" cy="' + str(dy) + '" r="5.5" '
                    'fill="' + color + '" opacity="0.9"/>')

    # build SVG entirely with string concatenation — no f-string
    svg = (
        '<svg width="210" height="210" viewBox="0 0 180 180" xmlns="http://www.w3.org/2000/svg">'
        '<defs>'
        '<radialGradient id="rglow" cx="50%" cy="50%" r="50%">'
        '<stop offset="0%" stop-color="' + color + '" stop-opacity="' + str(glow_opacity) + '"/>'
        '<stop offset="100%" stop-color="' + color + '" stop-opacity="0"/>'
        '</radialGradient>'
        '</defs>'
        # ambient glow
        '<circle cx="90" cy="90" r="75" fill="url(#rglow)" style="' + pulse + '"/>'
        # track ring
        '<circle cx="90" cy="90" r="' + str(R) + '" fill="none" stroke="#1e1e1e" stroke-width="10"/>'
        # tick marks
        + ticks +
        # filled arc
        '<circle cx="90" cy="90" r="' + str(R) + '" fill="none"'
        ' stroke="' + color + '" stroke-width="10"'
        ' stroke-dasharray="' + str(dash) + ' ' + str(gap) + '"'
        ' stroke-linecap="round"'
        ' transform="rotate(-90 90 90)"/>'
        # leading dot
        + lead_dot +
        # centre percentage
        '<text x="90" y="76" text-anchor="middle"'
        ' fill="#f5f5f5" font-family="JetBrains Mono,monospace"'
        ' font-size="30" font-weight="500">' + str(pct) + '%</text>'
        # time remaining
        '<text x="90" y="100" text-anchor="middle"'
        ' fill="' + color + '" font-family="Space Grotesk,sans-serif"'
        ' font-size="14" font-weight="600">' + str(centre) + '</text>'
        # sub label
        '<text x="90" y="116" text-anchor="middle"'
        ' fill="#383838" font-family="Space Grotesk,sans-serif"'
        ' font-size="9" letter-spacing="1.5">' + sub.upper() + '</text>'
        '</svg>'
    )

    html = (
        '<div style="display:flex;flex-direction:column;align-items:center;padding:10px 0 4px;">'
        + svg
        + '<div style="font-size:10px;color:#2e2e2e;letter-spacing:0.16em;'
          'text-transform:uppercase;margin-top:2px;">Live Device Volume</div>'
        + '</div>'
    )
    return html

def tick_dose():
    now = time.time()
    if st.session_state.last_tick is None:
        st.session_state.last_tick = now
        return
    delta = now - st.session_state.last_tick
    st.session_state.last_tick        = now
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

# ── Tick ─────────────────────────────────────────────────────────────────────
if st.session_state.session_active:
    tick_dose()

# ── Derived values ────────────────────────────────────────────────────────────
dose      = st.session_state.dose
cur_safe  = safe_minutes(st.session_state.volume, st.session_state.output_type, st.session_state.rule_preset)
status_k, status_l = get_status(st.session_state.volume, st.session_state.output_type)
if st.session_state.volume <= 60:
    arc_col = "#4ade80"
elif st.session_state.volume <= 80:
    arc_col = "#EF9F27"
else:
    arc_col = "#f87171"

if st.session_state.session_active:
    rem_mins    = math.ceil(max(0.0, 1.0 - dose) * cur_safe)
    ring_centre = fmt_mins(rem_mins)
    ring_sub    = "remaining"
else:
    ring_centre = fmt_mins(cur_safe)
    ring_sub    = "at this vol"
    dose        = 0.0

# ── Header ────────────────────────────────────────────────────────────────────
badge_map = {
    "safe":    "badge-safe",
    "caution": "badge-caution",
    "danger":  "badge-danger",
    "speaker": "badge-speaker",
}
st.markdown(
    f'<div class="eg-header">'
    f'<span class="eg-logo">Ear<span>Guard</span></span>'
    f'<span class="{badge_map[status_k]}">{status_l}</span>'
    f'</div>',
    unsafe_allow_html=True
)

tab_home, tab_stats, tab_settings = st.tabs(["◎  Home", "▦  Stats", "⚙  Settings"])

# ═══════════════════════════════════════════════════════
# HOME
# ═══════════════════════════════════════════════════════
with tab_home:

    # ── Ring ──
    vol_frac = st.session_state.volume / 100.0
    ring_html = build_ring(vol_frac, ring_centre, ring_sub, arc_col, st.session_state.session_active)
    st.markdown(
        '<div class="eg-card" style="padding:10px 10px 16px;">' + ring_html + '</div>',
        unsafe_allow_html=True
    )

    # ── Output device ──
    out_opts = ["In-ear headphones", "Over-ear headphones", "Bluetooth headphones", "Speaker"]
    st.markdown('<div class="eg-card"><div class="eg-card-title">Output device</div>', unsafe_allow_html=True)
    sel = st.selectbox("out", out_opts,
                       index=out_opts.index(st.session_state.output_type),
                       key="out_sel", label_visibility="collapsed")
    if sel != st.session_state.output_type:
        st.session_state.output_type = sel
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Volume ──
    vc = "#4ade80" if st.session_state.volume <= 60 else "#EF9F27" if st.session_state.volume <= 80 else "#f87171"
    st.markdown(
        f'<div class="eg-card">'
        f'<div style="display:flex;justify-content:space-between;margin-bottom:8px;align-items:center;">'
        f'<span style="font-size:13px;font-weight:600;color:#888;letter-spacing:0.08em;text-transform:uppercase;">Volume</span>'
        f'<span style="font-size:22px;font-weight:700;color:{vc};font-family:\'JetBrains Mono\',monospace;">{st.session_state.volume}%</span>'
        f'</div>'
        f'<div class="vol-track"><div class="vol-fill" style="width:{st.session_state.volume}%;background:{vc};"></div></div>',
        unsafe_allow_html=True
    )

    # Hardware bridge check
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    vol_file   = os.path.join(SCRIPT_DIR, "current_volume.txt")

    if os.path.exists(vol_file):
        try:
            with open(vol_file, "r") as f:
                bridge_vol = int(f.read().strip())
        except Exception:
            bridge_vol = st.session_state.volume
        st.markdown(
            '<p style="font-size:11px;color:#60a5fa;margin-top:6px;letter-spacing:0.06em;">⬤ LIVE · Reading from OS hardware</p></div>',
            unsafe_allow_html=True
        )
        if bridge_vol != st.session_state.volume:
            st.session_state.volume = bridge_vol
            st.rerun()
    else:
        new_vol = st.slider("vol", 0, 100, st.session_state.volume, key="vol_sl", label_visibility="collapsed")
        st.markdown(
            '<p style="font-size:11px;color:#333;margin-top:4px;letter-spacing:0.06em;">Drag to set volume level</p></div>',
            unsafe_allow_html=True
        )
        if new_vol != st.session_state.volume:
            st.session_state.volume = new_vol
            st.rerun()

    # ── Status banner ──
    banners = {
        "speaker": '<div class="alert-info">📢 Speaker mode — no ear tracking needed.</div>',
        "safe":    '<div class="alert-safe">✓ Within safe listening range.</div>',
        "caution": '<div class="alert-warn">⚠ Caution — consider lowering volume.</div>',
        "danger":  '<div class="alert-danger">⬤ Loud — dose accumulating fast.</div>',
    }
    st.markdown(banners[status_k], unsafe_allow_html=True)

    # ── Quick stats ──
    total_today = sum(s["duration"] for s in st.session_state.session_log)
    sessions_n  = len(st.session_state.session_log)
    st.markdown(
        f'<div class="metric-grid">'
        f'<div class="metric-box"><div class="metric-lbl">Today</div><div class="metric-val">{fmt_mins(round(total_today))}</div></div>'
        f'<div class="metric-box"><div class="metric-lbl">Sessions</div><div class="metric-val">{sessions_n}</div></div>'
        f'</div>',
        unsafe_allow_html=True
    )

    # ── Session tracker ──
    st.markdown('<div class="eg-card"><div class="eg-card-title">Session tracker</div>', unsafe_allow_html=True)

    if status_k == "speaker":
        st.markdown('<p style="color:#444;font-size:13px;">Tracking paused — speaker in use.</p>', unsafe_allow_html=True)

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
        st.markdown('<div class="timer-sub">Session duration</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="prog-track">'
            f'<div class="prog-fill" style="width:{min(d,1)*100:.1f}%;background:{prog_col};"></div>'
            f'</div>'
            f'<div class="dose-label">Ear dose: {min(d*100,100):.0f}% &nbsp;·&nbsp; limit at {st.session_state.volume}% vol = {fmt_mins(cur_safe)}</div>',
            unsafe_allow_html=True
        )

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

        st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="stop-btn">', unsafe_allow_html=True)
        if st.button("⏹  End session"):
            end_session()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        time.sleep(0.5)
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Today's log ──
    st.markdown('<div class="eg-card"><div class="eg-card-title">Today\'s log</div>', unsafe_allow_html=True)
    if st.session_state.session_log:
        for s in reversed(st.session_state.session_log):
            dot = "log-dot-danger" if s["over_limit"] else "log-dot-warn" if s["dose"] >= 75 else "log-dot-safe"
            st.markdown(
                f'<div class="log-entry">'
                f'<div style="display:flex;align-items:center;gap:10px;">'
                f'<div class="{dot}"></div>'
                f'<div><div style="color:#ccc;font-weight:500;">{s["time"]} · {s["device"]}</div>'
                f'<div style="font-size:11px;color:#444;margin-top:1px;">{s["volume"]}% vol · dose: {s["dose"]}%</div>'
                f'</div></div>'
                f'<div style="color:#555;font-size:13px;font-family:\'JetBrains Mono\',monospace;">{s["duration"]}m</div>'
                f'</div>',
                unsafe_allow_html=True
            )
    else:
        st.markdown('<p style="color:#333;font-size:13px;">No sessions yet today.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# STATS
# ═══════════════════════════════════════════════════════
with tab_stats:

    days   = ['M','T','W','T','F','S','S']
    hours  = [1.2, 2.8, 1.0, 3.4, 0.8, 2.1, 1.4]
    colors = ['#4ade80','#f87171','#4ade80','#f87171','#4ade80','#EF9F27','#4ade80']
    today_h   = sum(s["duration"] for s in st.session_state.session_log) / 60
    hours[6]  = round(today_h, 1)
    colors[6] = '#f87171' if today_h > 3 else '#EF9F27' if today_h > 2 else '#4ade80'
    max_h     = max(hours) if max(hours) > 0 else 1

    bars = "".join(
        f'<div class="bar-col">'
        f'<div class="bar-val" style="color:{c};">{h}h</div>'
        f'<div class="bar-rect" style="height:{max(4,int(h/max_h*60))}px;background:{c};opacity:0.85;box-shadow:0 0 8px {c}55;"></div>'
        f'<div class="bar-lbl">{d}</div>'
        f'</div>'
        for d, h, c in zip(days, hours, colors)
    )
    legend = (
        '<div style="display:flex;gap:14px;margin-top:12px;flex-wrap:wrap;">'
        '<span style="font-size:10px;color:#444;display:flex;align-items:center;gap:5px;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;">'
        '<span style="width:6px;height:6px;border-radius:2px;background:#4ade80;display:inline-block;"></span>Safe</span>'
        '<span style="font-size:10px;color:#444;display:flex;align-items:center;gap:5px;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;">'
        '<span style="width:6px;height:6px;border-radius:2px;background:#EF9F27;display:inline-block;"></span>Warning</span>'
        '<span style="font-size:10px;color:#444;display:flex;align-items:center;gap:5px;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;">'
        '<span style="width:6px;height:6px;border-radius:2px;background:#f87171;display:inline-block;"></span>Over limit</span>'
        '</div>'
    )
    st.markdown(
        '<div class="eg-card"><div class="eg-card-title">This week</div>'
        + '<div class="chart-wrap">' + bars + '</div>'
        + legend + '</div>',
        unsafe_allow_html=True
    )

    avg_vol = (round(sum(s["volume"] for s in st.session_state.session_log) /
               len(st.session_state.session_log)) if st.session_state.session_log else 68)
    over_n  = sum(1 for s in st.session_state.session_log if s["over_limit"])

    st.markdown(
        f'<div class="metric-grid">'
        f'<div class="metric-box"><div class="metric-lbl">Weekly avg</div><div class="metric-val">1h 41m</div></div>'
        f'<div class="metric-box"><div class="metric-lbl">Safe days</div><div class="metric-val">{max(0,7-over_n)} / 7</div></div>'
        f'<div class="metric-box"><div class="metric-lbl">Avg volume</div><div class="metric-val">{avg_vol}%</div></div>'
        f'<div class="metric-box"><div class="metric-lbl">Breaks taken</div><div class="metric-val">{sessions_n}</div></div>'
        f'</div>',
        unsafe_allow_html=True
    )

    score  = max(30, min(100, 100 - over_n * 8 - max(0, avg_vol - 60) // 5))
    sc_col = "#4ade80" if score >= 70 else "#EF9F27" if score >= 50 else "#f87171"
    sc_msg = "Good — keep it up" if score >= 70 else "Fair — try lower volumes" if score >= 50 else "Poor — take more breaks"

    st.markdown(
        f'<div class="eg-card">'
        f'<div class="eg-card-title">Ear health score</div>'
        f'<div style="display:flex;align-items:center;gap:20px;">'
        f'<div class="score-big" style="color:{sc_col};text-shadow:0 0 30px {sc_col}55;">{score}</div>'
        f'<div><div class="score-desc">{sc_msg}</div>'
        f'<div class="score-sub" style="margin-top:4px;">Based on volume + duration habits</div></div>'
        f'</div></div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="eg-card">
      <div class="eg-card-title">About the dose model</div>
      <p style="font-size:13px;color:#555;line-height:1.8;">
        EarGuard tracks <span style="color:#EF9F27;font-weight:600;">cumulative ear dose</span>,
        not a simple countdown timer. Lowering volume slows accumulation —
        but <span style="color:#f87171;font-weight:600;">never resets it</span>.
        Based on the ISO 1999 noise exposure standard.
      </p>
      <div style="margin-top:12px;display:flex;flex-direction:column;gap:8px;">
        <div style="display:flex;justify-content:space-between;font-size:12px;color:#444;font-family:'JetBrains Mono',monospace;">
          <span>60% vol</span><span style="color:#4ade80;">60 min safe</span></div>
        <div style="display:flex;justify-content:space-between;font-size:12px;color:#444;font-family:'JetBrains Mono',monospace;">
          <span>80% vol</span><span style="color:#EF9F27;">~34 min safe</span></div>
        <div style="display:flex;justify-content:space-between;font-size:12px;color:#444;font-family:'JetBrains Mono',monospace;">
          <span>100% vol</span><span style="color:#f87171;">~22 min safe</span></div>
      </div>
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# SETTINGS
# ═══════════════════════════════════════════════════════
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

    st.markdown(
        '<div style="text-align:center;color:#2a2a2a;font-size:11px;margin-top:24px;'
        'letter-spacing:0.12em;text-transform:uppercase;">'
        'EarGuard · WHO 60/60 · ISO 1999 · v1.2</div>',
        unsafe_allow_html=True
    )

# python -m streamlit run "c:/Users/kavya/Journey/Self Projects/earguard/earguard.py"