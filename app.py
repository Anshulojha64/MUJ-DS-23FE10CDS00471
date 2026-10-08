import streamlit as st
import time

from pipeline import run_research_pipeline

# ── Page config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Research Pipeline",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ── Custom CSS ────────────────────────────────────────────────────────────────

st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=DM+Serif+Display&display=swap');

/* ── Base ── */

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #0d1117;
    color: #e6edf3;
}

/* ── Hide default Streamlit chrome ── */

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    padding: 2rem 3rem 4rem;
    max-width: 1100px;
}


/* ── Hero ── */

.hero {
    padding: 3.5rem 0 2rem;
    border-bottom: 1px solid #21262d;
    margin-bottom: 2.5rem;
}

.hero-label {
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    color: #58a6ff;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}

.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 3rem;
    font-weight: 400;
    color: #f0f6fc;
    line-height: 1.15;
    margin: 0 0 0.75rem;
}

.hero-sub {
    font-size: 1rem;
    color: #8b949e;
    font-weight: 300;
    max-width: 55ch;
    line-height: 1.65;
}


/* ── Input area ── */

.input-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 1.75rem 2rem;
    margin-bottom: 2rem;
}


/* Streamlit text-input override */

.stTextInput > label {
    font-size: 0.82rem;
    font-weight: 500;
    color: #8b949e;
    letter-spacing: 0.04em;
    margin-bottom: 0.4rem;
}

.stTextInput > div > div > input {
    background: #0d1117 !important;
    border: 1px solid #30363d !important;
    border-radius: 6px !important;
    color: #f0f6fc !important;
    font-size: 1rem !important;
    padding: 0.65rem 0.9rem !important;
    transition: border-color 0.15s;
}

.stTextInput > div > div > input:focus {
    border-color: #58a6ff !important;
    box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.1) !important;
}


/* ── Button ── */

.stButton > button {
    background: #238636 !important;
    color: #ffffff !important;
    border: 1px solid #2ea043 !important;
    border-radius: 6px !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    padding: 0.55rem 1.5rem !important;
    transition: background 0.15s, transform 0.1s !important;
    letter-spacing: 0.02em;
}

.stButton > button:hover {
    background: #2ea043 !important;
    transform: translateY(-1px);
}

.stButton > button:active {
    transform: translateY(0);
}


/* ── Step cards ── */

.step-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.75rem;
    margin-bottom: 2rem;
}

.step-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 1rem 1rem 0.9rem;
    position: relative;
    transition: border-color 0.2s;
}

.step-card.active {
    border-color: #58a6ff;
}

.step-card.done {
    border-color: #2ea043;
}

.step-card.waiting {
    opacity: 0.45;
}

.step-icon {
    font-size: 1.4rem;
    margin-bottom: 0.4rem;
}

.step-num {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    color: #58a6ff;
    text-transform: uppercase;
    margin-bottom: 0.2rem;
}

.step-name {
    font-size: 0.85rem;
    font-weight: 500;
    color: #e6edf3;
}

.step-desc {
    font-size: 0.75rem;
    color: #6e7681;
    margin-top: 0.2rem;
}

.step-badge {
    position: absolute;
    top: 0.7rem;
    right: 0.7rem;
    width: 8px;
    height: 8px;
    border-radius: 50%;
}

.step-badge.active {
    background: #58a6ff;
    animation: pulse 1.2s infinite;
}

.step-badge.done {
    background: #2ea043;
}

.step-badge.waiting {
    background: #30363d;
}

@keyframes pulse {
    0%, 100% {
        opacity: 1;
        transform: scale(1);
    }

    50% {
        opacity: 0.5;
        transform: scale(1.3);
    }
}


/* ── Result panels ── */

.result-panel {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 10px;
    margin-bottom: 1.25rem;
    overflow: hidden;
}

.result-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.85rem 1.25rem;
    background: #1c2128;
    border-bottom: 1px solid #21262d;
}

.result-header-icon {
    font-size: 1rem;
}

.result-header-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #e6edf3;
}

.result-header-badge {
    margin-left: auto;
    font-size: 0.68rem;
    font-weight: 500;
    background: #1f3c2a;
    color: #3fb950;
    border: 1px solid #2ea043;
    border-radius: 20px;
    padding: 0.15rem 0.6rem;
}

.result-body {
    padding: 1.25rem 1.5rem;
    font-size: 0.88rem;
    color: #c9d1d9;
    line-height: 1.75;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 420px;
    overflow-y: auto;
}

.result-body::-webkit-scrollbar {
    width: 5px;
}

.result-body::-webkit-scrollbar-track {
    background: transparent;
}

.result-body::-webkit-scrollbar-thumb {
    background: #30363d;
    border-radius: 3px;
}


/* ── Report panel (special) ── */

.report-panel {
    background: #0d1117;
    border: 1px solid #238636;
    border-radius: 10px;
    margin-bottom: 1.25rem;
    overflow: hidden;
}

.report-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.85rem 1.25rem;
    background: #111a14;
    border-bottom: 1px solid #238636;
}

.report-body {
    padding: 1.5rem 1.75rem;
    font-size: 0.92rem;
    color: #e6edf3;
    line-height: 1.8;
    word-break: break-word;
}


/* ── Feedback / critic panel ── */

.critic-panel {
    background: #0d1117;
    border: 1px solid #9e6a03;
    border-radius: 10px;
    margin-bottom: 1.25rem;
    overflow: hidden;
}

.critic-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.85rem 1.25rem;
    background: #1a1500;
    border-bottom: 1px solid #9e6a03;
}

.critic-body {
    padding: 1.25rem 1.5rem;
    font-size: 0.88rem;
    color: #c9d1d9;
    line-height: 1.75;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 420px;
    overflow-y: auto;
}


/* ── Status bar ── */

.status-bar {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.65rem 1rem;
    background: #1c2128;
    border: 1px solid #30363d;
    border-radius: 6px;
    font-size: 0.82rem;
    color: #8b949e;
    margin-bottom: 1.5rem;
}

.status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #58a6ff;
    animation: pulse 1s infinite;
    flex-shrink: 0;
}


/* ── Download button tweak ── */

.stDownloadButton > button {
    background: #1c2128 !important;
    color: #58a6ff !important;
    border: 1px solid #30363d !important;
    border-radius: 6px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    padding: 0.45rem 1.1rem !important;
}

.stDownloadButton > button:hover {
    border-color: #58a6ff !important;
    background: #161b22 !important;
}


/* ── Empty state ── */

.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: #6e7681;
}

.empty-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.empty-title {
    font-size: 1.1rem;
    font-weight: 500;
    color: #8b949e;
    margin-bottom: 0.4rem;
}

.empty-desc {
    font-size: 0.85rem;
    line-height: 1.6;
}

</style>
""",
    unsafe_allow_html=True,
)


# ── Session state defaults ─────────────────────────────────────────────────

for key in ("result", "running", "current_step", "error"):
    if key not in st.session_state:
        st.session_state[key] = None

if "running" not in st.session_state:
    st.session_state.running = False


# ── Hero ──────────────────────────────────────────────────────────────────

st.markdown(
    """
<div class="hero">
    <div class="hero-label">Multi-Agent System</div>
    <div class="hero-title">Research Pipeline</div>
    <div class="hero-sub">
        Five specialized stages working in sequence — web search, content scraping,
        NLP analysis, report drafting, and critical review — to produce a structured
        research brief on any topic.
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# ── Input card ────────────────────────────────────────────────────────────

st.markdown('<div class="input-card">', unsafe_allow_html=True)

col_input, col_btn = st.columns([5, 1], vertical_alignment="bottom")

with col_input:
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        label_visibility="visible",
    )

with col_btn:
    run_clicked = st.button("Run Pipeline", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)


# ── Step-status renderer ───────────────────────────────────────────────────


STEPS = [
    ("🔍", "01", "Search Agent", "Finding relevant sources"),
    ("📄", "02", "Reader Agent", "Scraping top resources"),
    ("🧠", "03", "NLP Analysis", "Extracting and analyzing text"),
    ("✍️", "04", "Writer Chain", "Drafting the report"),
    ("🧐", "05", "Critic Chain", "Reviewing & scoring"),
]


def render_steps(current: int | None, done_up_to: int | None):
    cards = ""

    for i, (icon, num, name, desc) in enumerate(STEPS):

        if done_up_to is not None and i < done_up_to:
            state_cls, badge_cls = "done", "done"

        elif current is not None and i == current:
            state_cls, badge_cls = "active", "active"

        else:
            state_cls, badge_cls = "waiting", "waiting"

        cards += f"""<div class="step-card {state_cls}">
    <div class="step-badge {badge_cls}"></div>
    <div class="step-icon">{icon}</div>
    <div class="step-num">{num}</div>
    <div class="step-name">{name}</div>
    <div class="step-desc">{desc}</div>
</div>"""

    st.markdown(
        f'<div class="step-grid">{cards}</div>',
        unsafe_allow_html=True,
    )


# ── Result panel helpers ───────────────────────────────────────────────────


def result_panel(icon, title, badge, body, panel_cls="result"):

    if panel_cls == "report":

        st.markdown(
            f"""
            <div class="report-panel">
                <div class="report-header">
                    <span class="result-header-icon">{icon}</span>
                    <span class="result-header-title">{title}</span>
                    <span class="result-header-badge">{badge}</span>
                </div>
                <div class="report-body">{body}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    elif panel_cls == "critic":

        st.markdown(
            f"""
            <div class="critic-panel">
                <div class="critic-header">
                    <span class="result-header-icon">{icon}</span>
                    <span class="result-header-title">{title}</span>
                    <span class="result-header-badge">{badge}</span>
                </div>
                <div class="critic-body">{body}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            f"""
            <div class="result-panel">
                <div class="result-header">
                    <span class="result-header-icon">{icon}</span>
                    <span class="result-header-title">{title}</span>
                    <span class="result-header-badge">{badge}</span>
                </div>
                <div class="result-body">{body}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ── Run pipeline ──────────────────────────────────────────────────────────

if run_clicked:

    if not topic or not topic.strip():

        st.warning("Please enter a research topic before running the pipeline.")

    else:

        st.session_state.result = None
        st.session_state.error = None
        st.session_state.running = True

        step_placeholder = st.empty()
        status_placeholder = st.empty()

        # Initial step display
        with step_placeholder:
            render_steps(0, None)

        with status_placeholder:
            st.markdown(
                '<div class="status-bar"><div class="status-dot"></div>'
                "Step 1 of 5 — Search Agent is finding sources…</div>",
                unsafe_allow_html=True,
            )

        try:

            # ── Import agents ─────────────────────────────────────────────

            from agents import (
                build_search_agent,
                build_reader_agent,
                nlp_chain,
                writer_chain,
                critic_chain,
            )

            # ── Step 1: Search ────────────────────────────────────────────

            search_agent = build_search_agent()

            search_result = search_agent.invoke(
                {
                    "messages": [
                        (
                            "user",
                            f"Find recent, reliable and detailed information about: {topic}",
                        )
                    ]
                }
            )

            search_results = search_result["messages"][-1].content

            # ── Step 2: Reader ────────────────────────────────────────────

            with step_placeholder:
                render_steps(1, 1)

            with status_placeholder:
                st.markdown(
                    '<div class="status-bar"><div class="status-dot"></div>'
                    "Step 2 of 5 — Reader Agent is scraping top resources…</div>",
                    unsafe_allow_html=True,
                )

            reader_agent = build_reader_agent()

            reader_result = reader_agent.invoke(
                {
                    "messages": [
                        (
                            "user",
                            f"""
Based on the following search results about '{topic}',
identify the most relevant URL and scrape it for deeper content.

Search Results:

{search_results[:4000]}

Use the scrape_url tool on the most relevant URL.
""",
                        )
                    ]
                }
            )

            scraped_content = reader_result["messages"][-1].content

            # ── Step 3: NLP Analysis ──────────────────────────────────────

            research_combined = (
                f"SEARCH RESULTS:\n{search_results}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{scraped_content}"
            )

            with step_placeholder:
                render_steps(2, 2)

            with status_placeholder:
                st.markdown(
                    '<div class="status-bar"><div class="status-dot"></div>'
                    "Step 3 of 5 — NLP Analysis is processing the research text…</div>",
                    unsafe_allow_html=True,
                )

            nlp_result = nlp_chain.invoke({"research": research_combined})

            # ── Step 4: Writer ────────────────────────────────────────────

            with step_placeholder:
                render_steps(3, 3)

            with status_placeholder:
                st.markdown(
                    '<div class="status-bar"><div class="status-dot"></div>'
                    "Step 4 of 5 — Writer is drafting the report…</div>",
                    unsafe_allow_html=True,
                )

            report = writer_chain.invoke(
                {
                    "topic": topic,
                    "research": research_combined,
                    "nlp_analysis": nlp_result,
                }
            )

            # ── Step 5: Critic ────────────────────────────────────────────

            with step_placeholder:
                render_steps(4, 4)

            with status_placeholder:
                st.markdown(
                    '<div class="status-bar"><div class="status-dot"></div>'
                    "Step 5 of 5 — Critic is reviewing and scoring the report…</div>",
                    unsafe_allow_html=True,
                )

            feedback = critic_chain.invoke({"report": report})

            # ── Save results ──────────────────────────────────────────────

            st.session_state.result = {
                "search_results": search_results,
                "scraped_content": scraped_content,
                "nlp_analysis": nlp_result,
                "report": report,
                "feedback": feedback,
            }

            st.session_state.running = False

            # Mark all steps as complete
            with step_placeholder:
                render_steps(None, 5)

            with status_placeholder:
                st.markdown(
                    '<div class="status-bar"><div class="status-dot"></div>'
                    "Pipeline completed successfully.</div>",
                    unsafe_allow_html=True,
                )

        except Exception as e:

            st.session_state.error = str(e)
            st.session_state.running = False

            with step_placeholder:
                render_steps(None, None)

            with status_placeholder:
                st.empty()


# ── Show results ──────────────────────────────────────────────────────────

if st.session_state.error:

    st.error(f"Pipeline error: {st.session_state.error}")


elif st.session_state.result:

    r = st.session_state.result

    # ── Search Results ────────────────────────────────────────────────────

    result_panel(
        "🔍",
        "Search Results",
        "Agent 1 complete",
        r["search_results"],
        panel_cls="result",
    )

    # ── Scraped Content ───────────────────────────────────────────────────

    result_panel(
        "📄",
        "Scraped Content",
        "Agent 2 complete",
        r["scraped_content"],
        panel_cls="result",
    )

    # ── NLP Analysis ──────────────────────────────────────────────────────

    result_panel(
        "🧠",
        "NLP Analysis",
        "Agent 3 complete",
        r["nlp_analysis"],
        panel_cls="result",
    )

    # ── Research Report ───────────────────────────────────────────────────

    result_panel(
        "✍️",
        "Research Report",
        "Agent 4 complete",
        r["report"],
        panel_cls="report",
    )

    # ── Critic Feedback ──────────────────────────────────────────────────

    result_panel(
        "🧐",
        "Critic Feedback",
        "Agent 5 complete",
        r["feedback"],
        panel_cls="critic",
    )

    # ── Download buttons ──────────────────────────────────────────────────

    dl_col1, dl_col2, _ = st.columns([1, 1, 3])

    with dl_col1:

        st.download_button(
            "⬇ Download Report",
            data=r["report"],
            file_name=f"report_{topic[:30].replace(' ', '_')}.txt",
            mime="text/plain",
        )

    with dl_col2:

        full_output = (
            f"TOPIC: {topic}\n\n"
            f"{'='*60}\nSEARCH RESULTS\n{'='*60}\n"
            f"{r['search_results']}\n\n"
            f"{'='*60}\nSCRAPED CONTENT\n{'='*60}\n"
            f"{r['scraped_content']}\n\n"
            f"{'='*60}\nNLP ANALYSIS\n{'='*60}\n"
            f"{r['nlp_analysis']}\n\n"
            f"{'='*60}\nRESEARCH REPORT\n{'='*60}\n"
            f"{r['report']}\n\n"
            f"{'='*60}\nCRITIC FEEDBACK\n{'='*60}\n"
            f"{r['feedback']}"
        )

        st.download_button(
            "⬇ Full Output",
            data=full_output,
            file_name=f"full_research_{topic[:30].replace(' ', '_')}.txt",
            mime="text/plain",
        )


else:

    # ── Empty state ───────────────────────────────────────────────────────

    render_steps(None, None)

    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-icon">🔬</div>

            <div class="empty-title">
                Ready to research
            </div>

            <div class="empty-desc">
                Enter a topic above and click
                <strong>Run Pipeline</strong>.<br>
                The five stages will work through search, scraping,
                NLP analysis, writing, and review in sequence.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
