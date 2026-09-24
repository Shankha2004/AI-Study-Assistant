import streamlit as st
import requests

st.set_page_config(
    page_title="CourseMate | Study Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

BACKEND_URL = "http://127.0.0.1:8000"

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap');

    :root {
        --paper:      #f1ead9;
        --paper-2:    #e7dec8;
        --ink:        #26301f;
        --ink-soft:   #5d6350;
        --cloth:      #2f4a3d;
        --cloth-dark: #223a2f;
        --mark:       #e8b73f;
        --mark-soft:  #f4dfa6;
        --rule:       #cdc1a2;
    }

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp {
        background-color: var(--paper);
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.035'/%3E%3C/svg%3E");
    }
    section[data-testid="stSidebar"] {
        background: var(--cloth);
        border-right: 1px solid var(--cloth-dark);
    }
    section[data-testid="stSidebar"] * { color: var(--paper) !important; }
    section[data-testid="stSidebar"] .stCaption, section[data-testid="stSidebar"] small { color: #c7d3c9 !important; }

    h1, h2, h3, h4 { color: var(--ink) !important; }
    p, li, label { color: var(--ink) !important; }

    .hero { display: flex; align-items: center; gap: 2.5rem; padding: 1.2rem 0 2.4rem 0; }
    .hero-text { flex: 1.1; min-width: 280px; }
    .hero-art { flex: 1; min-width: 260px; }
    .hero .kicker {
        font-size: 0.8rem; font-weight: 500; color: var(--cloth);
        margin-bottom: 0.5rem;
    }
    .hero h1 {
        font-family: 'Fraunces', serif;
        font-weight: 600;
        font-size: 3rem;
        line-height: 1.05;
        margin: 0 0 0.9rem 0;
        color: var(--ink) !important;
    }
    .hero h1 .hl {
        background: linear-gradient(120deg, var(--mark-soft) 0%, var(--mark-soft) 100%);
        background-repeat: no-repeat;
        background-size: 100% 40%;
        background-position: 0 78%;
        padding: 0 0.1em;
    }
    .hero p.lede {
        font-size: 1.08rem;
        line-height: 1.65;
        color: var(--ink-soft) !important;
        max-width: 42ch;
        margin: 0 0 1.3rem 0;
    }
    .hero .steps { display: flex; flex-direction: column; gap: 0.55rem; }
    .hero .steps div {
        font-size: 0.92rem; color: var(--ink-soft) !important;
        display: flex; align-items: baseline; gap: 0.6rem;
    }
    .hero .steps .n {
        font-family: 'Fraunces', serif; font-weight: 600; color: var(--cloth);
        font-size: 1rem; width: 1.1rem;
    }

    .feature-row { display: flex; gap: 1.1rem; margin: 0.6rem 0 2.2rem 0; }
    .feature {
        flex: 1;
        background: var(--paper-2);
        border: 1px solid var(--rule);
        border-radius: 4px;
        padding: 1.15rem 1.2rem;
    }
    .feature svg { margin-bottom: 0.55rem; }
    .feature h4 {
        font-family: 'Fraunces', serif; font-weight: 600;
        font-size: 1.02rem; margin: 0 0 0.3rem 0; color: var(--ink) !important;
    }
    .feature p { font-size: 0.87rem; line-height: 1.5; color: var(--ink-soft) !important; margin: 0; }

    hr { border-color: var(--rule) !important; }
    section[data-testid="stSidebar"] hr { border-color: #3d5a4c !important; }

    .stButton > button {
        background: var(--mark) !important;
        color: var(--cloth-dark) !important;
        border: none !important;
        border-radius: 4px !important;
        font-weight: 600 !important;
    }
    .stButton > button:hover { background: #f0c65c !important; }
    .stButton > button p { color: var(--cloth-dark) !important; }

    div[data-testid="stFileUploader"] {
        background: var(--cloth-dark);
        border: 1px dashed #4a6b5a;
        border-radius: 6px;
        padding: 0.6rem;
    }

    div[data-testid="stMetric"] {
        background: var(--cloth-dark);
        border: 1px solid #3d5a4c;
        border-radius: 6px;
        padding: 0.5rem 0.4rem;
    }
    div[data-testid="stMetricValue"] { color: var(--paper) !important; }
    div[data-testid="stMetricLabel"] { color: #b9c7bd !important; }

    div[data-testid="stChatMessage"] {
        background: var(--paper-2);
        border: 1px solid var(--rule);
        border-radius: 8px;
    }
    div[data-testid="stExpander"] {
        background: var(--paper-2);
        border: 1px solid var(--rule);
        border-radius: 6px;
    }

    /* ---- High-Contrast Chat Input Styling ---- */
    div[data-testid="stBottom"], div[data-testid="stBottom"] > div {
        background-color: var(--paper) !important;
    }
    div[data-testid="stChatInput"] {
        background-color: transparent !important;
    }
    div[data-testid="stChatInput"] > div {
        background-color: var(--paper-2) !important;
        border: 1.5px solid var(--cloth) !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 12px rgba(38, 48, 31, 0.08) !important;
    }
    div[data-testid="stChatInput"] textarea {
        background-color: transparent !important;
        color: var(--ink) !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: var(--ink-soft) !important;
        opacity: 0.85 !important;
    }
    div[data-testid="stChatInput"] button {
        background-color: var(--mark) !important;
        color: var(--cloth-dark) !important;
        border-radius: 6px !important;
    }
    div[data-testid="stChatInput"] button:hover {
        background-color: #f0c65c !important;
    }
    div[data-testid="stChatInput"] button svg {
        fill: var(--cloth-dark) !important;
    }

    .source-box {
        background: var(--paper);
        border-left: 3px solid var(--mark);
        padding: 10px 14px;
        margin-top: 8px;
        border-radius: 0 6px 6px 0;
        font-family: 'Fraunces', serif;
        font-size: 0.94rem;
        line-height: 1.55;
        color: var(--ink-soft) !important;
    }
    .source-box b {
        color: var(--cloth) !important;
        font-family: 'Inter', sans-serif;
        font-size: 0.74rem;
        letter-spacing: 0.03em;
    }
</style>
""", unsafe_allow_html=True)

def render_sources(sources):
    if not sources:
        return

    with st.expander("Referenced passages", expanded=False):

        for i, source in enumerate(sources, 1):

            page = source.get("page", "?")
            text = source.get("text", "")

            st.markdown(
                f"""
                <div class="source-box">
                    <b>SOURCE {i} · PAGE {page}</b>
                    <br><br>
                    {text}
                </div>
                """,
                unsafe_allow_html=True
            )

if "messages" not in st.session_state:
    st.session_state.messages = []
if "doc_ready" not in st.session_state:
    st.session_state.doc_ready = False
if "current_document_id" not in st.session_state:
    st.session_state.current_document_id = None
if "indexed_chunks" not in st.session_state:
    st.session_state.indexed_chunks = 0
if "current_file" not in st.session_state:
    st.session_state.current_file = None

with st.sidebar:
    st.markdown("""
    <svg width="30" height="30" viewBox="0 0 30 30" fill="none">
      <path d="M4 6h9a4 4 0 0 1 4 4v15a4 4 0 0 0-4-3H4V6Z" stroke="#f1ead9" stroke-width="1.6" stroke-linejoin="round"/>
      <path d="M26 6h-9a4 4 0 0 0-4 4v15a4 4 0 0 1 4-3h9V6Z" stroke="#e8b73f" stroke-width="1.6" stroke-linejoin="round"/>
    </svg>
    """, unsafe_allow_html=True)
    st.markdown("### Your desk")
    st.caption("Add a syllabus, lecture notes, or a paper — answers stay grounded in what's on the desk.")

    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"], help="Standard PDF, up to 200MB")

    if uploaded_file is not None:
        st.caption(f"**{uploaded_file.name}** · {round(uploaded_file.size / 1024, 1)} KB")

        process_btn = st.button("Index document", use_container_width=True, type="primary")
        if process_btn:
            with st.status("Reading & indexing...", expanded=True) as status:
                st.write("Sending document to the retrieval pipeline...")
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                try:
                    response = requests.post(f"{BACKEND_URL}/upload", files=files, timeout=120)
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.doc_ready = True
                        st.session_state.indexed_chunks = data.get("chunks_indexed", 0)
                        st.session_state.current_file = data.get("filename", uploaded_file.name)
                        st.session_state.current_document_id = data.get("document_id")
                        status.update(label="Ready for questions", state="complete", expanded=False)
                        st.toast("Document indexed.", icon="📚")
                    else:
                        status.update(label="Couldn't process that file", state="error")
                        st.error(f"Error details: {response.text}")
                except requests.exceptions.ConnectionError:
                    status.update(label="Backend unreachable", state="error")
                    st.error("Can't connect to the server. Check that the backend is running.")
                except Exception as ex:
                    status.update(label="Something went wrong", state="error")
                    st.error(f"An error occurred: {ex}")
            
        if st.session_state.doc_ready:

            if st.button("📄 Summarize PDF", use_container_width=True):

                with st.spinner("Generating summary..."):

                    response = requests.post(
                        f"{BACKEND_URL}/summarize",
                        params={
                            "document_id": st.session_state.current_document_id
                        },
                        timeout=120
                    )

                if response.status_code == 200:
                    data = response.json()
                    st.session_state.summary = data["summary"]
                else:
                    st.error(f"Failed to generate summary: {response.text}")

            if st.button("📝 Generate Quiz", use_container_width=True):

                with st.spinner("Generating quiz..."):

                    response = requests.post(
                        f"{BACKEND_URL}/quiz",
                        params={
                            "document_id": st.session_state.current_document_id
                        },
                        timeout=120
                    )

                if response.status_code == 200:

                    data = response.json()

                    st.session_state.quiz = data["quiz"]

                else:

                    st.error(
                        f"Failed to generate quiz: {response.text}"
                    )


    st.markdown("---")
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric(label="Status", value="Ready" if st.session_state.doc_ready else "Idle")
    with col_stat2:
        st.metric(label="Chunks", value=st.session_state.indexed_chunks)



    st.markdown("---")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.summary = None
        st.session_state.doc_ready = False
        st.session_state.indexed_chunks = 0
        st.session_state.current_file = None
        st.session_state.current_document_id = None

        st.rerun()

st.markdown("""
<div class="hero">
  <div class="hero-text">
    <div class="kicker">STUDY ASSISTANT</div>
    <h1>Ask your notes<br>a <span class="hl">real question.</span></h1>
    <p class="lede">CourseMate reads your lecture slides and papers, then answers strictly from what's on the page — every claim traces back to a passage you can check yourself.</p>
    <div class="steps">
      <div><span class="n">1</span> Upload a PDF from the desk on the left</div>
      <div><span class="n">2</span> Ask a question in plain language</div>
      <div><span class="n">3</span> Read the answer, then check the source line it came from</div>
    </div>
  </div>
  <div class="hero-art">
    <svg width="100%" height="220" viewBox="0 0 420 240" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="20" y="14" width="380" height="212" rx="6" fill="#e7dec8" stroke="#cdc1a2"/>
      <rect x="46" y="42" width="180" height="10" rx="2" fill="#26301f" opacity="0.75"/>
      <rect x="46" y="66" width="300" height="8" rx="2" fill="#5d6350" opacity="0.5"/>
      <rect x="46" y="84" width="270" height="8" rx="2" fill="#5d6350" opacity="0.5"/>
      <rect x="44" y="100" width="230" height="14" rx="2" fill="#e8b73f" opacity="0.55"/>
      <rect x="46" y="126" width="300" height="8" rx="2" fill="#5d6350" opacity="0.5"/>
      <rect x="46" y="144" width="180" height="8" rx="2" fill="#5d6350" opacity="0.5"/>
      <rect x="44" y="160" width="150" height="14" rx="2" fill="#e8b73f" opacity="0.55"/>
      <rect x="46" y="186" width="260" height="8" rx="2" fill="#5d6350" opacity="0.5"/>
      <rect x="46" y="204" width="120" height="8" rx="2" fill="#5d6350" opacity="0.5"/>
    </svg>
  </div>
</div>
""", unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div class="feature-row">
      <div class="feature">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none"><circle cx="10.5" cy="10.5" r="6.5" stroke="#2f4a3d" stroke-width="1.7"/><path d="M19.5 19.5 15 15" stroke="#2f4a3d" stroke-width="1.7" stroke-linecap="round"/></svg>
        <h4>Find a passage</h4>
        <p>Locate a precise definition or formula without paging through the document.</p>
      </div>
      <div class="feature">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none"><path d="M4 20h16" stroke="#2f4a3d" stroke-width="1.7" stroke-linecap="round"/><path d="M6 20 15 4l3 1.7L9.5 21.7 6 20Z" stroke="#2f4a3d" stroke-width="1.7" stroke-linejoin="round"/></svg>
        <h4>Summaries</h4>
        <p>Turn a dense chapter into a core-concept review in seconds.</p>
      </div>
      <div class="feature">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none"><path d="M12 3 2 8l10 5 10-5-10-5Z" stroke="#2f4a3d" stroke-width="1.7" stroke-linejoin="round"/><path d="M6 11.5v5c0 1.2 2.7 3.5 6 3.5s6-2.3 6-3.5v-5" stroke="#2f4a3d" stroke-width="1.7"/></svg>
        <h4>Exam prep</h4>
        <p>Turn slides into test-ready explanations, in plain language.</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

if "summary" in st.session_state:

    st.markdown("## 📄 PDF Summary")

    st.markdown(st.session_state.summary)

    st.markdown("---")

if "quiz" in st.session_state:

    st.markdown("## 📝 Quiz")

    st.markdown(st.session_state.quiz)

    st.markdown("---")

for msg in st.session_state.messages:
    avatar = "🙋" if msg["role"] == "user" else "📚"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        render_sources(msg.get("sources"))

user_query = st.chat_input("Ask a question about your uploaded materials...")

if user_query:
    if not st.session_state.doc_ready:
        st.warning("⚠️ Please upload and index a PDF from the sidebar first.")
    else:
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user", avatar="🙋"):
            st.markdown(user_query)

        with st.chat_message("assistant", avatar="📚"):
            with st.spinner("Reading through the relevant passages..."):
                try:
                    response = requests.post(f"{BACKEND_URL}/ask", json={"question": user_query, "document_id": st.session_state.current_document_id}, timeout=60)
                    if response.status_code == 200:
                        payload = response.json()
                        answer = payload.get("answer", "No response generated.")
                        sources = payload.get("sources", [])

                        st.markdown(answer)
                        render_sources(sources)

                        st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
                    else:
                        st.error(f"Error {response.status_code}: {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Backend unreachable. Make sure your backend server is running.")
                except Exception as e:
                    st.error(f"Failed to fetch response: {e}")