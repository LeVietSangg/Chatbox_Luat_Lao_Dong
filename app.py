"""
app.py — Chatbot Pháp luật Lao động
Fixes: sidebar toggle, example-q pipeline, multi-conversation, visual separation
"""
import os, sys, re, time
import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))
from retriever import LegalRetriever
from generator import LegalGenerator

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TOP_K    = 10
MODEL    = "gemini-3.5-flash-lite"

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Chatbot Pháp luật Lao động",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; margin: 0; }
.stApp { background: #F7F2EC !important; }

/* ── Streamlit native elements (Keep them visible and functional) ── */
#MainMenu { visibility: hidden; } /* Only hide the hamburger menu contents if needed, but let's just leave it for now to avoid breaking header */
footer { visibility: hidden; }

/* ── Collapse layout gaps ── */
.block-container { max-width: 100% !important; }
[data-testid="column"]:nth-of-type(1) { padding-left: 20px !important; padding-right: 15px !important; }
[data-testid="column"]:nth-of-type(2) { padding-right: 20px !important; }

/* ════════════════════════════════
   SIDEBAR — đỏ đô
════════════════════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(175deg, #7B1A1A 0%, #5E1111 65%, #4A0D0D 100%) !important;
    border-right: none !important;
    box-shadow: 3px 0 12px rgba(0,0,0,0.22) !important;   /* ← ranh giới sidebar|chat */
    min-width: 220px !important;
    max-width: 240px !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding: 16px 14px 14px !important;
    height: 100vh;
    display: flex; flex-direction: column;
    overflow: hidden;
}

/* Override tất cả text trong sidebar về màu trắng */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div { color: rgba(255,255,255,0.85) !important; }

/* Logo */
.sb-logo {
    display:flex; align-items:center; gap:10px;
    padding-bottom:14px;
    border-bottom:1px solid rgba(255,255,255,0.12);
    margin-bottom:12px; flex-shrink:0;
}
.sb-logo-icon {
    width:40px; height:40px;
    background:rgba(255,255,255,0.13); border-radius:9px;
    display:flex; align-items:center; justify-content:center;
    font-size:1.25rem; flex-shrink:0;
}
.sb-logo-name  { font-size:.88rem; font-weight:700; color:#fff !important; line-height:1.25; margin:0; }
.sb-logo-sub   { font-size:.62rem; color:rgba(255,255,255,.45) !important; line-height:1.4; margin:2px 0 0; }

/* Section label */
.sb-lbl {
    font-size:.62rem; font-weight:700; text-transform:uppercase;
    letter-spacing:.09em; color:rgba(255,255,255,.38) !important;
    margin:10px 0 5px; flex-shrink:0;
}

/* History scroll area */
.sb-scroll { flex:1; overflow-y:auto; min-height:0; }
.sb-scroll::-webkit-scrollbar { width:3px; }
.sb-scroll::-webkit-scrollbar-thumb { background:rgba(255,255,255,.15); border-radius:4px; }

/* History item (plain HTML — styled buttons below for clickable ones) */
.sb-item {
    display:flex; align-items:flex-start; gap:8px;
    padding:7px 8px; border-radius:8px; cursor:pointer;
    transition:background .15s; margin-bottom:2px;
}
.sb-item:hover  { background:rgba(255,255,255,.09); }
.sb-item.active { background:rgba(255,255,255,.15); }
.sb-item-ico    { font-size:.85rem; flex-shrink:0; margin-top:1px; opacity:.65; }
.sb-item-title  { font-size:.79rem; font-weight:500; color:#fff !important;
                  white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:150px; }
.sb-item-time   { font-size:.66rem; color:rgba(255,255,255,.38) !important; margin-top:1px; }

/* Sidebar stButton overrides */
[data-testid="stSidebar"] .stButton > button {
    width:100% !important;
    background:rgba(255,255,255,.11) !important;
    border:1.5px solid rgba(255,255,255,.22) !important;
    border-radius:9px !important;
    color:#fff !important;
    font-size:.83rem !important; font-weight:600 !important;
    padding:8px 12px !important;
    box-shadow:none !important; margin-bottom:4px !important;
    transition:background .18s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background:rgba(255,255,255,.2) !important;
    border-color:rgba(255,255,255,.35) !important;
}
/* History-item styled buttons (no border, left-aligned) */
[data-testid="stSidebar"] .hist-btn button {
    background:transparent !important;
    border:none !important;
    border-radius:8px !important;
    text-align:left !important;
    padding:7px 8px !important;
    font-size:.79rem !important; font-weight:400 !important;
    color:rgba(255,255,255,.85) !important;
}
[data-testid="stSidebar"] .hist-btn button:hover {
    background:rgba(255,255,255,.1) !important;
}

/* Sidebar bottom */
.sb-bottom { flex-shrink:0; margin-top:auto; padding-top:8px; }
.sb-info {
    background:rgba(0,0,0,.18); border-radius:9px;
    padding:9px 11px; font-size:.71rem;
    color:rgba(255,255,255,.6) !important; line-height:1.55;
    margin-bottom:10px;
}
.sb-info a { color:#E8A44A !important; font-weight:600; text-decoration:none; }
.sb-settings { font-size:.77rem; color:rgba(255,255,255,.4) !important; cursor:pointer;
               padding:4px 2px; display:flex; align-items:center; gap:6px; }
.sb-settings:hover { color:rgba(255,255,255,.75) !important; }
.sb-divider  { border:none; border-top:1px solid rgba(255,255,255,.1); margin:8px 0; }

/* ════════════════════════════════
   MAIN — 2 cột: chat | sources
════════════════════════════════ */

/* ── Chat header ── */
.chat-header {
    display:flex; align-items:center; justify-content:space-between;
    background:#fff;
    border-bottom:1px solid #EAE0D5;
    padding:10px 18px; 
    box-shadow:0 1px 4px rgba(0,0,0,.05);
}
.chat-hd-left { display:flex; align-items:center; gap:10px; }
.chat-hd-av {
    width:35px; height:35px;
    background:linear-gradient(135deg,#7B1A1A,#A82C2C);
    border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-size:.95rem; flex-shrink:0;
}
.chat-hd-name   { font-size:.9rem; font-weight:700; color:#1E0A0A; margin:0; }
.chat-hd-status { font-size:.68rem; color:#888; display:flex; align-items:center; gap:4px; margin-top:1px; }
.dot-green      { width:7px; height:7px; background:#3FB950; border-radius:50%; display:inline-block; }
.hd-btn {
    width:30px; height:30px; border-radius:7px;
    border:1px solid #EAE0D5; background:#FAF7F3;
    display:flex; align-items:center; justify-content:center;
    cursor:pointer; font-size:.85rem;
    transition:background .15s; margin-left:6px;
}
.hd-btn:hover { background:#F0E8DF; }

/* ── Messages ── */
.msg-list { padding:20px 18px 8px; display:flex; flex-direction:column; gap:22px; }

/* ── Empty state ── */
.empty-wrap {
    display:flex; flex-direction:column;
    align-items:center; justify-content:center;
    min-height:55vh;
    padding:30px 24px; text-align:center;
}
.empty-icon {
    width:68px; height:68px; border-radius:50%;
    background:linear-gradient(135deg,#7B1A1A,#A82C2C);
    display:flex; align-items:center; justify-content:center;
    font-size:1.85rem; margin:0 auto 16px;
    box-shadow:0 4px 18px rgba(123,26,26,.28);
}
.empty-wrap h3 { font-size:1.05rem; font-weight:700; color:#1E0A0A; margin:0 0 6px; }
.empty-wrap p  { font-size:.82rem; color:#9A8070; line-height:1.6;
                 max-width:360px; margin:0 0 20px; }

/* Example question buttons (main area) */
.stButton > button.eq-btn, div[data-testid="column"] .stButton > button {
    border-radius:20px !important;
    border:1px solid #E0D5C8 !important;
    background:#fff !important;
    color:#5A3A2A !important;
    font-size:.78rem !important;
    padding:7px 14px !important;
    box-shadow:0 1px 3px rgba(0,0,0,.06) !important;
    transition:all .18s !important;
    text-align:left !important;
    margin-bottom:4px !important;
}
.stButton > button.eq-btn:hover,
div[data-testid="column"] .stButton > button:hover {
    background:#7B1A1A !important;
    color:#fff !important;
    border-color:#7B1A1A !important;
}

/* ── User bubble ── */
.msg-user { display:flex; justify-content:flex-end; padding-left:60px; }
.ub {
    background:linear-gradient(135deg,#7B1A1A,#9E2020);
    color:#fff; border-radius:16px 3px 16px 16px;
    padding:12px 17px; font-size:.88rem; line-height:1.65;
    box-shadow:0 2px 10px rgba(123,26,26,.3); max-width:76%;
}
.ub-time { font-size:.62rem; color:rgba(255,255,255,.5);
           text-align:right; margin-top:5px; }

/* ── Bot bubble ── */
.msg-bot { display:flex; gap:10px; align-items:flex-start; padding-right:16px; }
.bot-av {
    width:32px; height:32px; flex-shrink:0;
    background:linear-gradient(135deg,#7B1A1A,#A82C2C);
    border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-size:.85rem; margin-top:3px;
}
.bot-wrap { flex:1; min-width:0; }

/* Main answer */
.msg-ans {
    background:#fff; border:1px solid #E8DDD0;
    border-radius:3px 16px 16px 16px;
    padding:14px 17px; font-size:.88rem;
    line-height:1.7; color:#2C1010;
    box-shadow:0 1px 5px rgba(0,0,0,.07);
    margin-bottom:8px; word-break:break-word;
    white-space: pre-wrap;
}

/* Legal basis card */
.lbc {
    background:#fff; border:1px solid #E8DDD0;
    border-radius:10px; padding:10px 13px; margin-bottom:7px;
    box-shadow:0 1px 3px rgba(0,0,0,.05);
}
.lbc-hd {
    font-size:.67rem; font-weight:700;
    text-transform:uppercase; letter-spacing:.06em;
    color:#7B1A1A; margin-bottom:7px;
    display:flex; align-items:center; gap:5px;
}
details > summary { list-style: none; cursor: pointer; outline: none; }
details > summary::-webkit-details-marker { display: none; }

.lbc-details {
    border-bottom: 1px solid #F2EAE0;
    padding-bottom: 6px;
    margin-bottom: 6px;
}
.lbc-details:last-child { border-bottom: none; padding-bottom: 0; margin-bottom: 0; }
.lbc-row {
    display:flex; align-items:flex-start; gap:9px;
}
.chat-fulltext {
    margin-top: 8px; padding: 12px; background: #FFF;
    border-radius: 6px; font-size: 0.82rem; white-space: pre-wrap;
    color: #2C1010; border: 1px dashed #E8DDD0;
}
.src-fulltext {
    margin-top: 10px; padding: 12px; background: #FAF7F3;
    border-radius: 6px; font-size: 0.8rem; white-space: pre-wrap;
    color: #2C1010; border: 1px solid #EAE0D5;
}
.lbc-n {
    width:19px; height:19px; flex-shrink:0;
    background:#F9EEE8; color:#7B1A1A;
    border-radius:50%; font-size:.66rem; font-weight:700;
    display:flex; align-items:center; justify-content:center;
    margin-top:1px;
}
.lbc-info { flex:1; min-width:0; }
.lbc-doc   { font-size:.8rem; font-weight:600; color:#1E0A0A; margin-bottom:1px; }
.lbc-cls   { font-size:.73rem; color:#7A6050; }
.lbc-id    {
    display:inline-block; background:#FEF0DE;
    border:1px solid #E8A44A; color:#996B00;
    font-size:.61rem; font-family:monospace; font-weight:600;
    padding:1px 6px; border-radius:4px; margin-top:3px;
}
.lbc-link  { font-size:.71rem; font-weight:600; color:#7B1A1A; cursor:pointer; flex-shrink:0; margin-top:2px; }

/* Summary card */
.sum-c {
    background:#FDF8F3; border:1px solid #E8DDD0;
    border-left:3px solid #7B1A1A;
    border-radius:0 10px 10px 0;
    padding:9px 13px; margin-bottom:7px;
    font-size:.81rem; color:#3A2010; line-height:1.6;
}
.sum-lbl { font-size:.66rem; font-weight:700; text-transform:uppercase;
           letter-spacing:.06em; color:#7B1A1A; margin-bottom:3px; }

/* Footer under bot message */
.msg-foot {
    display:flex; align-items:center; justify-content:space-between;
    padding:2px 0; margin-top:2px;
}
.foot-time { font-size:.62rem; color:#C0A898; }
.foot-acts { display:flex; gap:5px; }
.foot-btn  {
    width:24px; height:24px; border-radius:6px;
    border:1px solid #EAE0D5; background:transparent;
    display:flex; align-items:center; justify-content:center;
    cursor:pointer; font-size:.72rem; color:#9A8070;
    transition:all .15s;
}
.foot-btn:hover { background:#F0E8DF; color:#7B1A1A; }

/* Refusal */
.refusal {
    background:#FFF5F4; border:1px solid #F0BABA;
    border-radius:3px 16px 16px 16px;
    padding:12px 15px; font-size:.86rem; color:#8B2020; line-height:1.55;
}

/* Chat input */
[data-testid="stChatInput"] {
    border:1.5px solid #DDD5C8 !important;
    border-radius:12px !important;
    background:#FAF7F3 !important;
    box-shadow:none !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color:#7B1A1A !important;
    box-shadow:0 0 0 3px rgba(123,26,26,.1) !important;
}
.inp-hint { text-align:center; font-size:.66rem; color:#C0A898; margin-top:5px; }

/* ════════════════════════════════
   SOURCE PANEL
════════════════════════════════ */
.src-wrap {
    background:#fff; height:100%;
    border-left:1px solid #EAE0D5;
    padding:14px 12px;
    overflow-y:auto;
}
.src-wrap::-webkit-scrollbar { width:3px; }
.src-wrap::-webkit-scrollbar-thumb { background:#DDD5C8; border-radius:4px; }

.src-hd {
    display:flex; align-items:center; justify-content:space-between;
    margin-bottom:10px; padding-bottom:9px;
    border-bottom:1px solid #EAE0D5;
    position:sticky; top:0; background:#fff; z-index:5;
}
.src-title { font-size:.82rem; font-weight:700; color:#1E0A0A; display:flex; align-items:center; gap:6px; }
.src-badge {
    background:#7B1A1A; color:#fff;
    font-size:.61rem; font-weight:700;
    padding:2px 7px; border-radius:10px;
}
.src-badge-gray { background:#9A8070; }

.src-card {
    border:1px solid #EAE0D5; border-radius:10px;
    padding:11px 12px; margin-bottom:8px;
    box-shadow:0 1px 3px rgba(0,0,0,.04);
    transition:box-shadow .15s;
}
.src-card:hover { box-shadow:0 2px 8px rgba(0,0,0,.09); }

.src-doc-tag {
    display:inline-block;
    background:#FEF0DE; border:1px solid rgba(232,164,74,.4);
    color:#7B3A00; font-size:.64rem; font-weight:700;
    padding:2px 7px; border-radius:4px; margin-bottom:6px;
    text-transform:uppercase; letter-spacing:.04em;
}
.src-cls   { font-size:.84rem; font-weight:700; color:#1E0A0A; margin-bottom:4px; }
.src-prev  {
    font-size:.75rem; color:#7A6050; line-height:1.6;
    margin-bottom:8px; font-style:italic;
    display:-webkit-box; -webkit-line-clamp:3;
    -webkit-box-orient:vertical; overflow:hidden;
}
.src-foot  {
    display:flex; align-items:center; justify-content:space-between;
    padding-top:7px; border-top:1px solid #F2EAE0;
}
.src-id {
    display:inline-block;
    background:#FEF0DE; border:1px solid #E8A44A;
    color:#996B00; font-family:monospace;
    font-size:.6rem; font-weight:600; padding:2px 6px; border-radius:4px;
}
.src-link { font-size:.71rem; font-weight:600; color:#7B1A1A; cursor:pointer; }
.src-link:hover { color:#A82C2C; }

.src-sec-lbl {
    font-size:.67rem; font-weight:700; text-transform:uppercase;
    letter-spacing:.07em; color:#9A8070;
    display:flex; align-items:center; justify-content:space-between;
    padding:9px 0 7px; border-top:1px solid #EAE0D5; margin-top:2px;
}

.src-empty {
    display:flex; flex-direction:column;
    align-items:center; justify-content:center;
    padding:48px 14px; text-align:center; color:#C0A898; gap:10px;
}
.src-empty-icon { font-size:2rem; opacity:.35; }
.src-empty p { font-size:.76rem; line-height:1.55; max-width:170px; margin:0; }
</style>
""", unsafe_allow_html=True)


# ── Load pipeline ─────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Đang khởi động hệ thống...")
def load_pipeline():
    r = LegalRetriever(data_dir=DATA_DIR)
    g = LegalGenerator(model_name=MODEL, temperature=0.0)
    return r, g


# ── Helpers ───────────────────────────────────────────────────────────────────
DOC_NAMES = {
    "45_2019_QH14":  "Bộ luật Lao động 2019",
    "145_2020_NDCP": "Nghị định 145/2020/NĐ-CP",
    "58_VBHN-VPQH":  "Luật BHXH (VBHN)",
    "84_2015_QH13":  "Luật ATVSLĐ 2015",
    "10_2012_QH13":  "Bộ luật Lao động 2012",
    "50_2024_QH15":  "Luật Công đoàn 2024",
}

def doc_name(code: str) -> str:
    for k, v in DOC_NAMES.items():
        if k in code: return v
    return code.replace("_", "/")

def parse_pid(pid: str) -> dict:
    parts = pid.split("__")
    code  = parts[0]
    dieu  = next((p[1:] for p in parts[1:] if p.startswith("D") and p[1:].isdigit()), "")
    khoan = next((p[1:] for p in parts[1:] if p.startswith("K")), "")
    clause = ("Điều " + dieu if dieu else "") + (", Khoản " + khoan if khoan else "")
    return {"doc": doc_name(code), "clause": clause.strip(", ") or pid, "pid": pid}

def strip_cit(text: str) -> str:
    return re.sub(r'\[[^\[\]]+\]', '', text).strip()

def hm() -> str:
    t = time.localtime(); return f"{t.tm_hour:02d}:{t.tm_min:02d}"

def new_conv() -> dict:
    return {"title": "Cuộc trò chuyện mới", "time": hm(), "messages": [], "chunks": None}


# ── Session state — multi-conversation ────────────────────────────────────────
if "convs" not in st.session_state:
    st.session_state.convs = {0: new_conv()}
if "active" not in st.session_state:
    st.session_state.active = 0
if "pending_q" not in st.session_state:
    st.session_state.pending_q = None

def get_conv() -> dict:
    return st.session_state.convs[st.session_state.active]

def switch_conv(cid: int):
    st.session_state.active = cid


# ══════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════
with st.sidebar:
    # Logo
    st.markdown("""
    <div class="sb-logo">
      <div class="sb-logo-icon">⚖️</div>
      <div>
        <p class="sb-logo-name">Chatbot<br>Pháp luật Lao động</p>
        <p class="sb-logo-sub">Tra cứu nhanh – Chính xác – Dễ hiểu</p>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── Nút cuộc trò chuyện mới ──────────────────
    if st.button("＋   Cuộc trò chuyện mới", key="btn_new", use_container_width=True):
        # Đặt title từ câu hỏi đầu tiên nếu có
        conv = get_conv()
        if conv["messages"]:
            first_q = next(
                (m["content"][:40] for m in conv["messages"] if m["role"] == "user"),
                "Cuộc trò chuyện"
            )
            conv["title"] = first_q
        # Tạo conversation mới
        new_id = max(st.session_state.convs.keys()) + 1
        st.session_state.convs[new_id] = new_conv()
        st.session_state.active = new_id
        st.rerun()

    # ── Conversation hiện tại ─────────────────────
    st.markdown('<div class="sb-lbl">Tất cả cuộc trò chuyện</div>', unsafe_allow_html=True)
    conv = get_conv()
    if conv["messages"]:
        first_q = next((m["content"][:36] for m in conv["messages"] if m["role"] == "user"), "Cuộc trò chuyện")
        st.markdown(f"""
        <div class="sb-item active">
          <span class="sb-item-ico">💬</span>
          <div>
            <div class="sb-item-title">{first_q}...</div>
            <div class="sb-item-time">Hôm nay, {conv['time']}</div>
          </div>
        </div>""", unsafe_allow_html=True)

    # ── Lịch sử ──────────────────────────────────
    other_convs = [(cid, c) for cid, c in st.session_state.convs.items()
                   if cid != st.session_state.active and c["messages"]]
    other_convs.sort(key=lambda x: x[0], reverse=True)

    if other_convs:
        st.markdown('<div class="sb-lbl" style="margin-top:12px;">Lịch sử gần đây</div>', unsafe_allow_html=True)
        for cid, c in other_convs[:6]:
            title = c.get("title") or next(
                (m["content"][:36] for m in c["messages"] if m["role"] == "user"),
                "Cuộc trò chuyện"
            )
            # Sử dụng st.button để có thể click chuyển conversation
            col_ico, col_txt = st.columns([1, 5])
            with col_ico:
                st.markdown('<span style="font-size:.85rem;opacity:.6">🕐</span>', unsafe_allow_html=True)
            with col_txt:
                if st.button(f"{title[:34]}...", key=f"hist_{cid}", use_container_width=True):
                    switch_conv(cid)
                    st.rerun()
            st.markdown(f'<div style="font-size:.64rem;color:rgba(255,255,255,.35);padding:0 0 4px 28px;">Hôm nay, {c["time"]}</div>', unsafe_allow_html=True)

    # ── Bottom ────────────────────────────────────
    st.markdown('<hr class="sb-divider">', unsafe_allow_html=True)
    st.markdown("""


    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# LOAD PIPELINE
# ══════════════════════════════════════════════
try:
    retriever, generator = load_pipeline()
except Exception as e:
    st.error(f"❌ Lỗi khởi tạo: {e}"); st.stop()


# ══════════════════════════════════════════════
# MAIN: chat | sources
# ══════════════════════════════════════════════
col_chat, col_src = st.columns([3, 1.1], gap="small")

# ─────────────────────────────────────────────
# CỘT CHAT
# ─────────────────────────────────────────────
with col_chat:

    # Header
    st.markdown("""
    <div class="chat-header">
      <div class="chat-hd-left">
        <div class="chat-hd-av">⚖️</div>
        <div>
          <div class="chat-hd-name">Chatbot hỗ trợ tra cứu một số quy định về pháp luật về lao động</div>
          <div class="chat-hd-status"><span class="dot-green"></span>Đang hoạt động</div>
        </div>
      </div>

    </div>""", unsafe_allow_html=True)

    conv     = get_conv()
    messages = conv["messages"]

    EXAMPLES = [
        "Thời gian thử việc tối đa là bao nhiêu ngày?",
        "Tiền trợ cấp thôi việc tính như thế nào?",
        "Làm thêm giờ tối đa trong một năm là bao nhiêu giờ?",
        "Điều kiện hưởng lương hưu hằng tháng là gì?",
        "Người lao động được nghỉ phép bao nhiêu ngày mỗi năm?",
        "Chế độ thai sản cho lao động nữ như thế nào?",
    ]

    # ── Empty state ─────────────────────────────
    if not messages:
        st.markdown("""
        <div class="empty-wrap">
          <div class="empty-icon">⚖️</div>
          <h3>Xin chào! Tôi có thể giúp gì cho bạn?</h3>
          <p>Đặt câu hỏi về <strong>hợp đồng lao động</strong>, <strong>tiền lương</strong>,
             <strong>BHXH</strong>, <strong>nghỉ phép</strong>, <strong>sa thải</strong>
             và các vấn đề pháp luật lao động khác.</p>
        </div>""", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        for i, q in enumerate(EXAMPLES):
            with (c1 if i % 2 == 0 else c2):
                # KHÔNG gọi st.rerun() ở đây — để Streamlit tự rerun sau button click
                if st.button(q, key=f"eq_{i}", use_container_width=True):
                    st.session_state.pending_q = q
                    # Streamlit tự rerun sau khi button được click

    else:
        # ── Render conversation ──────────────────
        html_content = '<div class="msg-list">'
        for msg in messages:
            if msg["role"] == "user":
                msg_text = msg['content'].strip()
                html_content += f"""<div class="msg-user">
<div class="ub">
{msg_text}
<div class="ub-time">{msg.get('time','')} ✓✓</div>
</div>
</div>"""
            else:
                is_ref  = msg.get("is_refusal", False)
                api_e   = msg.get("api_error", False)
                ans     = strip_cit(msg["content"])
                cits    = msg.get("citations", [])
                chunks  = msg.get("chunks", [])
                t       = msg.get("time", "")

                if api_e:
                    body = '<div class="refusal">Hệ thống AI đang quá tải hoặc gặp lỗi kết nối. Vui lòng thử lại sau.</div>'
                elif is_ref:
                    body = '<div class="refusal">Xin lỗi, tôi không tìm thấy thông tin phù hợp trong cơ sở dữ liệu pháp luật.</div>'
                else:
                    body = f'<div class="msg-ans">{ans}</div>'
                    cited_c = [c for c in chunks if c.get("provision_id") in cits][:3]
                    if cited_c:
                        rows = ""
                        for idx, c in enumerate(cited_c, 1):
                            p = parse_pid(c.get("provision_id",""))
                            noi_dung = c.get("content", {}).get("noi_dung", "Không có nội dung.")
                            hieu_luc = c.get("content", {}).get("hieu_luc", "")
                            
                            hl_badge = ''
                            if hieu_luc == "het_hieu_luc":
                                hl_badge = '<span style="font-size: 0.65rem; padding: 2px 6px; border-radius: 4px; background: #FFEEEE; color: #D32F2F; border: 1px solid #FFCDD2; margin-left: 8px; font-weight: 500;">Hết hiệu lực</span>'
                            elif hieu_luc == "con_hieu_luc":
                                hl_badge = '<span style="font-size: 0.65rem; padding: 2px 6px; border-radius: 4px; background: #E8F5E9; color: #2E7D32; border: 1px solid #C8E6C9; margin-left: 8px; font-weight: 500;">Còn hiệu lực</span>'

                        rows += f"""<details class="lbc-details">
<summary>
<div class="lbc-row">
<div class="lbc-n">{idx}</div>
<div class="lbc-info">
<div class="lbc-doc">{p['doc']}{hl_badge}</div>
<div class="lbc-cls">{p['clause']}</div>
<span class="lbc-id">{p['pid']}</span>
</div>
<span class="lbc-link">Xem ▾</span>
</div>
</summary>
<div class="chat-fulltext">{noi_dung}</div>
</details>"""
                        body += f'<div class="lbc"><div class="lbc-hd">📄 Căn cứ pháp lý</div>{rows}</div>'

                html_content += f"""<div class="msg-bot">
<div class="bot-av">⚖️</div>
<div class="bot-wrap">
{body}
<div class="msg-foot">
<span class="foot-time">{t}</span>
<div class="foot-acts">
</div>
</div>
</div>
</div>"""
        html_content += '</div>'
        st.markdown(html_content, unsafe_allow_html=True)

    # ── Chat input ───────────────────────────────
    st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)
    typed = st.chat_input("Nhập câu hỏi pháp luật lao động của bạn...")

    # Ưu tiên: typed > pending_q
    prompt = typed or st.session_state.pending_q
    if st.session_state.pending_q and not typed:
        st.session_state.pending_q = None  # clear sau khi dùng

    if prompt:
        t = hm()
        conv = get_conv()

        # Thêm user message
        conv["messages"].append({"role": "user", "content": prompt, "time": t})

        # Đặt title nếu là câu đầu tiên
        if len([m for m in conv["messages"] if m["role"] == "user"]) == 1:
            conv["title"] = prompt[:40]
            conv["time"]  = t

        # Pipeline
        with st.spinner("Đang tìm kiếm điều khoản..."):
            chunks = retriever.search_hybrid(prompt, top_k=TOP_K)

        with st.spinner("Đang soạn câu trả lời..."):
            res = generator.generate(prompt, chunks)

        conv["chunks"] = chunks
        conv["messages"].append({
            "role":       "assistant",
            "content":    res["answer"],
            "citations":  res.get("citations", []),
            "is_refusal": res.get("is_refusal", False),
            "api_error":  res.get("api_error", False),
            "chunks":     chunks,
            "time":       t,
        })
        st.rerun()  # rerun duy nhất — để hiển thị conversation

    st.markdown('<div class="inp-hint">Nhấn Enter để gửi · Shift+Enter để xuống dòng</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CỘT NGUỒN TRÍCH DẪN
# ─────────────────────────────────────────────
with col_src:
    conv      = get_conv()
    chunks    = conv.get("chunks") or []
    last_bot  = next((m for m in reversed(conv["messages"]) if m["role"] == "assistant"), None)
    cited_ids = last_bot.get("citations", []) if last_bot else []
    cited     = [c for c in chunks if c.get("provision_id") in cited_ids]
    others    = [c for c in chunks if c.get("provision_id") not in cited_ids]

    html_src = f"""<div class="src-wrap">
    <div class="src-hd">
      <div class="src-title">Nguồn trích dẫn <span class="src-badge">{len(cited)}</span></div>
      <span style="color:#9A8070;cursor:pointer">∧</span>
    </div>"""

    if not chunks:
        html_src += """
        <div class="src-empty">
          <div class="src-empty-icon">📋</div>
          <p>Gửi câu hỏi để xem nguồn văn bản pháp luật tại đây.</p>
        </div>"""
    else:
        def src_card(c: dict, dim: bool = False) -> str:
            pid  = c.get("provision_id", "")
            cont = c.get("content", {})
            p    = parse_pid(pid)
            noi  = cont.get("noi_dung", "")
            prev = noi[:190].replace("<", "&lt;").replace(">", "&gt;")
            hieu_luc = cont.get("hieu_luc", "")
            
            hl_badge = ''
            if hieu_luc == "het_hieu_luc":
                hl_badge = '<span style="font-size: 0.6rem; padding: 2px 5px; border-radius: 4px; background: #FFEEEE; color: #D32F2F; border: 1px solid #FFCDD2; margin-left: 6px; font-weight: 500; display: inline-block; vertical-align: middle;">Hết hiệu lực</span>'
            elif hieu_luc == "con_hieu_luc":
                hl_badge = '<span style="font-size: 0.6rem; padding: 2px 5px; border-radius: 4px; background: #E8F5E9; color: #2E7D32; border: 1px solid #C8E6C9; margin-left: 6px; font-weight: 500; display: inline-block; vertical-align: middle;">Còn hiệu lực</span>'
                
            op   = ' style="opacity:.68"' if dim else ''
            return f"""
            <div class="src-card"{op}>
              <details>
                <summary>
                  <div class="src-doc-tag">
                    <span style="display: inline-block; vertical-align: middle;">📄 {p['doc']}</span>
                    {hl_badge}
                  </div>
                  <div class="src-cls">{p['clause']}</div>
                  <div class="src-prev">"{prev}{'...' if len(noi)>190 else ''}"</div>
                  <div class="src-foot">
                    <span class="src-id">{pid}</span>
                    <span class="src-link">Xem chi tiết ▾</span>
                  </div>
                </summary>
                <div class="src-fulltext">{noi}</div>
              </details>
            </div>"""

        for c in cited:
            html_src += src_card(c)

        if others:
            html_src += f"""
            <div class="src-sec-lbl">
              Các nguồn liên quan khác
              <span class="src-badge src-badge-gray">{len(others)}</span>
            </div>"""
            for c in others[:3]:
                html_src += src_card(c, dim=True)

    html_src += "</div>"
    st.markdown(html_src, unsafe_allow_html=True)

