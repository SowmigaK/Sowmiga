"""SQL Buddy AI - generate, fix, explain, practise and try SQL, with a floating chat assistant."""
import logging
import os

import pandas as pd
import streamlit as st

from sqlbuddy import prompts
from sqlbuddy.datasets import CUSTOM_MODES, DEFAULT_DATASET, OWN_MODE, PRESETS, UPLOAD_MODE
from sqlbuddy.llm import DEFAULT_MODEL, build_llm
from sqlbuddy.practice import CHALLENGES, LEVELS, check_answer
from sqlbuddy.sandbox import DEFAULT_SETUP_SQL, Sandbox, SandboxError, sanitize_identifier
from sqlbuddy.schema_viz import schema_to_dot
from sqlbuddy.usage import UsageLimiter

log = logging.getLogger("sqlbuddy")
MAX_CSV_ROWS = 5000
CHAT_SUGGESTIONS = ["What is a JOIN?", "WHERE vs HAVING?", "Find duplicates"]

st.set_page_config(page_title="SQL Buddy AI", page_icon="🧠", layout="wide")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="st-"], button, input, textarea {font-family:'Plus Jakarta Sans', 'Segoe UI', system-ui, sans-serif;}

/* ---------- page ---------- */
.sb-hero {background:#0B1B3A; color:#fff; padding:22px 28px; border-radius:14px; margin-bottom:12px;}
.sb-hero h1 {color:#fff; font-size:2rem; margin:0 0 4px 0; padding:0;}
.sb-hero p {color:#C9D6F2; margin:0; font-size:1rem;}
.sb-note {background:#E4ECFF; border-left:4px solid #1D4ED8; padding:10px 14px; border-radius:6px; margin:6px 0 14px 0;}
.stTabs [data-baseweb="tab-highlight"] {background:#F59E0B;}
.stTabs [aria-selected="true"] {color:#0B1B3A; font-weight:600;}

/* ---------- sidebar ---------- */
section[data-testid="stSidebar"] {background:linear-gradient(180deg,#EEF3FF 0%,#E1EAFF 100%);}
section[data-testid="stSidebar"] .block-container, section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {padding-top:1.4rem;}
section[data-testid="stSidebar"] label p {font-size:.85rem; font-weight:600; color:#0B1B3A;}
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {color:#51608A; font-size:.8rem; margin-top:-.25rem;}

.sb-side-title {font-size:.95rem; font-weight:700; color:#0B1B3A; margin:1.6rem 0 .7rem 0;}

.sb-meter {background:#fff; border:1px solid #D3DEF8; border-radius:14px; padding:14px 16px; margin-top:1.4rem;}
.sb-meter-row {display:flex; align-items:baseline; justify-content:space-between; gap:8px;}
.sb-meter-label {font-size:.85rem; font-weight:600; color:#0B1B3A;}
.sb-meter-value {font-size:1.35rem; font-weight:700; color:#0B1B3A; line-height:1;}
.sb-meter-value small {font-size:.78rem; font-weight:500; color:#51608A;}
.sb-bar {height:6px; border-radius:99px; background:#E4ECFF; margin-top:10px; overflow:hidden;}
.sb-bar span {display:block; height:100%; border-radius:99px; background:linear-gradient(90deg,#2DD4BF,#1D4ED8);}
.sb-bar.low span {background:#F59E0B;}

.sb-demo {background:#FFF6E0; border:1px solid #F5D78A; border-radius:14px; padding:12px 14px; margin-top:1.4rem;
    font-size:.85rem; line-height:1.45; color:#5A4308;}
.sb-demo b {display:block; margin-bottom:2px; color:#3F2E04;}

.sb-steps {list-style:none; margin:0; padding:0; counter-reset:step;}
.sb-steps li {counter-increment:step; position:relative; padding:0 0 14px 38px; font-size:.86rem; line-height:1.45; color:#31405F;}
.sb-steps li::before {content:counter(step); position:absolute; left:0; top:0; width:26px; height:26px; border-radius:50%;
    background:#0B1B3A; color:#fff; font-size:.78rem; font-weight:700; display:flex; align-items:center; justify-content:center;}
.sb-steps li:not(:last-child)::after {content:""; position:absolute; left:12.5px; top:28px; bottom:2px; width:1px; background:#B8C7EE;}
.sb-steps b {display:block; color:#0B1B3A; font-size:.9rem; font-weight:600;}

.sb-tip {display:flex; gap:10px; align-items:flex-start; background:#fff; border:1px solid #D3DEF8; border-radius:14px;
    padding:12px 14px; margin-top:.4rem; font-size:.84rem; line-height:1.45; color:#31405F;}
.sb-tip svg {flex:0 0 auto; margin-top:1px;}
.sb-tip b {color:#0B1B3A;}

/* ---------- floating chat launcher ---------- */
.st-key-chat_widget {position:fixed; bottom:22px; right:22px; z-index:1000; width:auto;}
.st-key-chat_widget > div > div > button, .st-key-chat_widget [data-testid="stPopover"] > button {
    background:linear-gradient(135deg,#5EE0D6,#38BDF8); color:#0B1B3A; border:none; border-radius:999px;
    padding:11px 22px; font-weight:700; font-size:.95rem; box-shadow:0 8px 22px rgba(11,27,58,.30);}
.st-key-chat_widget [data-testid="stPopover"] > button:hover {filter:brightness(1.05); color:#0B1B3A;}

/* ---------- chat window ---------- */
div[data-testid="stPopoverBody"] {width:min(390px, 94vw); max-height:80vh; padding:0 !important; overflow:auto;
    border:none; border-radius:22px; box-shadow:0 22px 56px rgba(11,27,58,.32); background:#fff;}
div[data-testid="stPopoverBody"] [data-testid="stVerticalBlock"] {gap:.6rem;}

.sb-chat-head {display:flex; align-items:center; justify-content:space-between; gap:10px; padding:16px 20px 14px 20px;
    background:linear-gradient(115deg,#5EE0D6 0%,#A6EEE8 55%,#D9F8F5 100%);}
.sb-chat-brand {display:flex; align-items:center; gap:8px; font-size:1.5rem; font-weight:700; color:#0B1B3A; line-height:1;}
.sb-chat-brand .ai {background:#0B1B3A; color:#5EE0D6; font-size:1.15rem; padding:4px 8px; border-radius:7px;}
.sb-chat-sub {font-size:.8rem; font-weight:500; color:#27406B; margin-top:5px;}
.sb-chat-head svg {flex:0 0 auto;}

.st-key-chat_body {padding:6px 16px 16px 16px;}
.st-key-chat_body [data-testid="stCaptionContainer"] {color:#51608A; font-size:.78rem;}

/* messages */
.st-key-chat_body [data-testid="stChatMessage"] {background:transparent; padding:.2rem 0; gap:.55rem; align-items:flex-start;}
.st-key-chat_body [data-testid^="stChatMessageAvatar"] {width:2rem; height:2rem; background:#5EE0D6 !important; color:#0B1B3A !important;
    border-radius:50%; flex:0 0 auto;}
.st-key-chat_body [data-testid="stChatMessageContent"] {border-radius:18px 18px 18px 5px; padding:10px 14px; background:#E3F1FC;
    color:#0B1B3A; font-size:.9rem; line-height:1.5; max-width:calc(100% - 3rem);}
.st-key-chat_body [data-testid="stChatMessageContent"] p {margin:0 0 .4rem 0; color:inherit;}
.st-key-chat_body [data-testid="stChatMessageContent"] p:last-child {margin-bottom:0;}
.st-key-chat_body [data-testid="stChatMessageContent"] pre {border-radius:10px; font-size:.8rem;}
.st-key-chat_body [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {flex-direction:row-reverse;}
.st-key-chat_body [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid^="stChatMessageAvatar"] {
    background:#0B1B3A !important; color:#fff !important;}
.st-key-chat_body [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {
    background:#0B1B3A; color:#fff; border-radius:18px 18px 5px 18px;}

/* suggestion chips */
.st-key-chat_chips {display:flex; flex-direction:row !important; flex-wrap:wrap; gap:.45rem !important;}
.st-key-chat_chips > div {width:auto !important; flex:0 0 auto;}
.st-key-chat_chips button {background:#fff; color:#0B1B3A; border:1.5px solid #1F7FB8; border-radius:999px; padding:4px 14px;
    min-height:0; font-size:.82rem; font-weight:600;}
.st-key-chat_chips button:hover {background:#E3F1FC; border-color:#1F7FB8; color:#0B1B3A;}

/* input row */
.st-key-chat_input_row [data-testid="stForm"] {border:none; padding:0;}
.st-key-chat_input_row [data-baseweb="input"] {border-radius:999px; border:1.5px solid #7CC3E8; background:#fff; padding-left:6px;}
.st-key-chat_input_row [data-baseweb="input"]:focus-within {border-color:#1F7FB8; box-shadow:0 0 0 3px rgba(94,224,214,.35);}
.st-key-chat_input_row input {font-size:.9rem; color:#0B1B3A;}
.st-key-chat_input_row button {border-radius:999px; background:#0B1B3A; color:#fff; border:none; font-weight:600; min-height:2.5rem;}
.st-key-chat_input_row button:hover {background:#1D4ED8; color:#fff;}
.st-key-chat_clear button {background:transparent; border:none; color:#51608A; font-size:.78rem; padding:0; min-height:0;}
.st-key-chat_clear button:hover {color:#0B1B3A; background:transparent; text-decoration:underline;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ---------- setup ----------

def _secret(name):
    value = os.getenv(name)
    if value:
        return value
    try:
        return st.secrets.get(name)
    except Exception:  # no secrets.toml
        return None


@st.cache_resource
def get_llm():
    return build_llm(
        api_key=_secret("GROQ_API_KEY"),
        model=os.getenv("GROQ_MODEL", DEFAULT_MODEL),
        demo=os.getenv("SQLBUDDY_DEMO") == "1",
    )


ss = st.session_state
if "sandbox" not in ss:          # tables used by "Try it on sample data" and the chat assistant
    ss.sandbox = Sandbox()
if "practice_sb" not in ss:      # fixed tables used by Practice, never changed by the user
    ss.practice_sb = Sandbox()
if "limiter" not in ss:
    ss.limiter = UsageLimiter(int(os.getenv("FREE_LIMIT", "20")))
ss.setdefault("chat", [])
ss.setdefault("history", [])
ss.setdefault("solved", set())
ss.setdefault("checks", {})
ss.setdefault("feedback", {})
ss.setdefault("loaded_dataset", DEFAULT_DATASET)

llm = get_llm()
sandbox: Sandbox = ss.sandbox
limiter: UsageLimiter = ss.limiter


def guarded(fn, *args):
    """Run an AI call with the free-tier limit and friendly errors (never show stack traces)."""
    if not llm.is_demo and not limiter.consume():
        st.warning("You have used all free requests for this session. Upgrade to Pro for unlimited use.")
        return None
    try:
        with st.spinner("Thinking..."):
            return fn(*args)
    except Exception:
        log.exception("LLM call failed")
        st.error("The AI service is not responding. Please try again in a moment.")
        return None


def show_table(columns, rows, caption=True):
    df = pd.DataFrame(rows, columns=columns)
    st.dataframe(df)
    if caption:
        st.caption(f"{len(df)} row(s)")
    return df


def show_result(sql: str):
    """Run SQL on the sample data, show the table, and chart it when it makes sense."""
    try:
        columns, rows = sandbox.run(sql)
    except SandboxError as exc:
        st.error(str(exc))
        return
    df = show_table(columns, rows)
    st.caption("Sample data runs on SQLite, so MySQL or PostgreSQL-only syntax may fail here.")
    numeric = list(df.select_dtypes("number").columns)
    labels = [c for c in df.columns if c not in numeric]
    if len(df) > 1 and numeric and labels:
        st.bar_chart(df.set_index(labels[0])[numeric])


def preview_tables(sb: Sandbox):
    """Show each table with its first rows, so users see what data they can query."""
    for table in sb.tables():
        st.markdown(f"**{table}**")
        columns, rows = sb.run(f'SELECT * FROM "{table}" LIMIT 5')
        show_table(columns, rows, caption=False)


# ---------- header and sidebar ----------

st.markdown(
    '<div class="sb-hero"><h1>🧠 SQL Buddy AI</h1>'
    "<p>Ask in plain English, get working SQL, run it on sample data and practise until it sticks.</p></div>",
    unsafe_allow_html=True,
)

database = st.sidebar.selectbox("Your database", prompts.DIALECTS)
st.sidebar.caption("SQL Buddy writes queries for this database.")

if llm.is_demo:
    st.sidebar.markdown(
        '<div class="sb-demo"><b>Demo mode</b>Answers are sample replies. '
        "Add a GROQ_API_KEY to get live AI.</div>",
        unsafe_allow_html=True,
    )
else:
    share_left = 100 * limiter.remaining / limiter.limit if limiter.limit else 0
    low = " low" if share_left <= 20 else ""
    st.sidebar.markdown(
        '<div class="sb-meter"><div class="sb-meter-row">'
        '<span class="sb-meter-label">Free AI requests</span>'
        f'<span class="sb-meter-value">{limiter.remaining}<small> of {limiter.limit} left</small></span></div>'
        f'<div class="sb-bar{low}"><span style="width:{share_left:.0f}%"></span></div></div>',
        unsafe_allow_html=True,
    )

CHAT_ICON = (
    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#1D4ED8" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/></svg>'
)
st.sidebar.markdown(
    '<div class="sb-side-title">How to use SQL Buddy</div>'
    '<ol class="sb-steps">'
    "<li><b>Generate</b>Describe what you want in plain English.</li>"
    "<li><b>Try on sample data</b>Run the SQL and see real rows.</li>"
    "<li><b>Practice</b>Solve challenges until it sticks.</li>"
    "</ol>"
    f'<div class="sb-tip">{CHAT_ICON}<span><b>Quick question?</b> Open the chat button at the bottom right '
    "for a short answer.</span></div>",
    unsafe_allow_html=True,
)

tab_gen, tab_fix, tab_practice, tab_learn, tab_play = st.tabs(
    ["💡 Generate", "🛠️ Fix & explain", "🎯 Practice", "📚 Learn", "🧪 Try on sample data"]
)


# ---------- generate ----------

with tab_gen:
    question = st.text_area(
        "What do you want to find out?",
        placeholder="Show all employees earning more than 30000",
        height=100,
        key="generate_question",
    )
    if st.checkbox("Use the tables from the sample-data tab", value=True, key="use_playground"):
        schema = sandbox.describe()
        with st.expander("Tables being used"):
            st.code(schema, language="text")
    else:
        schema = st.text_area(
            "Table structure (optional)",
            placeholder="Table: employees\nColumns: employee_id, employee_name, salary",
            height=100,
            key="generate_schema",
        )

    if st.button("Generate SQL", type="primary"):
        if not question.strip():
            st.warning("Type a question first.")
        else:
            answer = guarded(llm.ask, prompts.generate_prompt(question, schema, database))
            ss.last_generated = answer
            if answer:
                ss.history.append({"question": question.strip(), "sql": prompts.extract_sql(answer) or ""})

    if ss.get("last_generated"):
        st.markdown(ss.last_generated)
        sql = prompts.extract_sql(ss.last_generated)
        if sql:
            left, right = st.columns(2)
            left.download_button("Download .sql", sql, file_name="query.sql")
            if right.button("Run on sample data"):
                show_result(sql)

    if ss.history:
        with st.expander(f"History ({len(ss.history)})"):
            for item in reversed(ss.history[-10:]):
                st.markdown(f"**{item['question']}**")
                if item["sql"]:
                    st.code(item["sql"], language="sql")
            export = "\n\n".join(f"-- {h['question']}\n{h['sql']}" for h in ss.history if h["sql"])
            st.download_button("Download all as .sql", export, file_name="history.sql", key="dl_history")


# ---------- fix & explain ----------

with tab_fix:
    mode = st.radio("What do you need?", ["Fix an error", "Explain a query", "Make it faster", "Convert dialect"],
                    horizontal=True)
    user_sql = st.text_area("Your SQL query", placeholder="SELECT name FROM employees WHERE salary >",
                            height=120, key="fix_query")
    error = target = None
    if mode == "Fix an error":
        error = st.text_area("Error message (optional)", placeholder="Paste the error here", key="fix_error")
    elif mode == "Convert dialect":
        target = st.selectbox("Convert to", [d for d in prompts.DIALECTS if d != database], key="convert_to")
        st.caption(f"From {database} (set in the sidebar).")

    if st.button(mode, type="primary", key="fix_go"):
        if not user_sql.strip():
            st.warning("Paste a query first.")
        else:
            if mode == "Fix an error":
                prompt = prompts.fix_prompt(user_sql, error, database)
            elif mode == "Explain a query":
                prompt = prompts.explain_prompt(user_sql, database)
            elif mode == "Make it faster":
                prompt = prompts.optimize_prompt(user_sql, database)
            else:
                prompt = prompts.convert_prompt(user_sql, database, target)
            answer = guarded(llm.ask, prompt)
            if answer:
                st.markdown(answer)


# ---------- practice ----------

with tab_practice:
    st.markdown(
        '<div class="sb-note"><b>Test yourself.</b> Each challenge asks a question about the practice tables. '
        "Write a query and press <i>Check answer</i>. We run it and compare the <b>result</b> with the correct one, "
        "so your query does not need to look like ours.</div>",
        unsafe_allow_html=True,
    )
    progress_slot = st.empty()

    level = st.radio("Level", ["All", *LEVELS], horizontal=True)
    pool = [c for c in CHALLENGES if level == "All" or c.level == level]
    challenge = st.selectbox(
        "Challenge", pool,
        format_func=lambda c: f"{'✅' if c.id in ss.solved else '⬜'}  {c.level}: {c.title} ({c.concept})",
    )

    with st.expander("Practice tables (read-only)"):
        preview_tables(ss.practice_sb)

    st.subheader(challenge.title)
    st.write(challenge.question)
    answer = st.text_area("Your query", height=110, key=f"answer_{challenge.id}",
                          placeholder="SELECT ... FROM ...")

    check_col, hint_col, solution_col = st.columns(3)
    if check_col.button("Check answer", type="primary", key=f"check_{challenge.id}"):
        if not answer.strip():
            st.warning("Write a query first.")
        else:
            result = check_answer(ss.practice_sb, challenge, answer)
            ss.checks[challenge.id] = (result, answer)
            if result.correct:
                ss.solved.add(challenge.id)
    with hint_col.popover("Hint"):
        st.write(challenge.hint)
    with solution_col.popover("Show solution"):
        st.code(challenge.solution, language="sql")

    checked = ss.checks.get(challenge.id)
    if checked:
        result, attempt = checked
        if result.correct:
            st.success(result.message)
        else:
            st.error(result.message)
        if result.columns:
            st.caption("Your result")
            show_table(result.columns, result.rows)
        if not result.correct and st.button("Explain my mistake", key=f"explain_{challenge.id}"):
            feedback = guarded(llm.ask, prompts.practice_feedback_prompt(
                challenge.question, attempt, result.message, database))
            if feedback:
                ss.feedback[challenge.id] = feedback
        if ss.feedback.get(challenge.id) and not result.correct:
            st.info(ss.feedback[challenge.id])

    with progress_slot.container():
        solved_count = len(ss.solved)
        st.progress(solved_count / len(CHALLENGES), text=f"{solved_count} of {len(CHALLENGES)} solved")


# ---------- learn ----------

with tab_learn:
    topic = st.selectbox("Topic", ["SELECT", "WHERE", "ORDER BY", "GROUP BY", "HAVING", "JOINS",
                                   "SUBQUERIES", "PRIMARY KEY", "FOREIGN KEY"])
    if st.button("Teach me"):
        answer = guarded(llm.ask, prompts.learn_prompt(topic, database))
        if answer:
            st.markdown(answer)
            st.caption("Ready to try it? Open the Practice tab.")


# ---------- try on sample data ----------

with tab_play:
    st.markdown(
        '<div class="sb-note"><b>Why this tab?</b> The AI gives you SQL as text. Here you can <b>run it on sample '
        "data</b> and see real rows and a chart, so you know it works before you use it on your real database. "
        "Everything here is temporary and never touches your own database.</div>",
        unsafe_allow_html=True,
    )

    st.markdown("#### 1. Choose your data")
    choice = st.radio("Data", [*PRESETS, *CUSTOM_MODES], key="dataset", horizontal=True,
                      label_visibility="collapsed")
    if choice != ss.loaded_dataset:
        if choice in PRESETS:
            sandbox.load(PRESETS[choice].setup)
        ss.loaded_dataset = choice

    if choice == UPLOAD_MODE:
        uploaded = st.file_uploader("CSV file (up to 5,000 rows)", type="csv")
        if uploaded is not None:
            default_name = sanitize_identifier(uploaded.name.rsplit(".", 1)[0], "data")
            table_name = st.text_input("Table name", value=default_name, key=f"csv_name_{uploaded.name}")
            if st.button("Add as a table"):
                try:
                    df = pd.read_csv(uploaded)
                    if len(df) > MAX_CSV_ROWS:
                        raise SandboxError(f"The file has {len(df)} rows. The limit is {MAX_CSV_ROWS}.")
                    kinds = {"i": "INTEGER", "u": "INTEGER", "f": "REAL"}
                    columns = [(str(c), kinds.get(df[c].dtype.kind, "TEXT")) for c in df.columns]
                    rows = [tuple(r) for r in df.astype(object).where(df.notna(), None).values.tolist()]
                    created = sandbox.add_table(table_name, columns, rows)
                    st.success(f"Added table {created} with {len(rows)} rows.")
                except SandboxError as exc:
                    st.error(str(exc))
                except Exception:
                    st.error("That file could not be read as a CSV.")
        st.caption("Your file stays in memory for this session only.")
    elif choice == OWN_MODE:
        setup_sql = st.text_area("CREATE TABLE and INSERT statements (SQLite)", value=DEFAULT_SETUP_SQL,
                                 height=240, key="setup_sql")
        if st.button("Load these tables"):
            try:
                sandbox.load(setup_sql)
                st.success("Tables loaded.")
            except SandboxError as exc:
                st.error(str(exc))

    table_names = list(sandbox.tables())
    left, right = st.columns(2)
    with left:
        with st.expander("Your tables and first rows", expanded=True):
            preview_tables(sandbox)
    with right:
        st.caption("Table diagram. Bold columns are primary keys, arrows are foreign keys.")
        st.graphviz_chart(schema_to_dot(sandbox.tables(), sandbox.foreign_keys()))

    st.markdown("#### 2. Run a query")
    examples = list(PRESETS[choice].examples) if choice in PRESETS else (
        [("Preview a table", f'SELECT * FROM "{table_names[0]}" LIMIT 10;')] if table_names else [])
    if examples:
        label = st.selectbox("Start from an example", [e[0] for e in examples], key=f"example_{choice}")
        starting_sql = dict(examples)[label]
    else:
        label, starting_sql = "blank", ""
    query = st.text_area("Your SELECT query", value=starting_sql, height=130, key=f"q_{choice}_{label}")

    st.markdown("#### 3. See the result")
    if st.button("Run query", type="primary"):
        show_result(query)


# ---------- floating chat assistant (bottom-right on every tab) ----------

def send_chat(text: str):
    ss.chat.append({"role": "user", "content": text})
    reply = guarded(llm.chat, prompts.chat_messages(ss.chat, database, sandbox.describe()))
    if reply:
        ss.chat.append({"role": "assistant", "content": reply})


CHAT_HEADER = (
    '<div class="sb-chat-head"><div>'
    '<div class="sb-chat-brand">SQL Buddy <span class="ai">AI</span></div>'
    '<div class="sb-chat-sub">Your anytime SQL coach</div></div>'
    '<svg width="64" height="64" viewBox="0 0 64 64" aria-hidden="true">'
    '<circle cx="32" cy="32" r="30" fill="#fff" opacity=".55"/>'
    '<ellipse cx="32" cy="19" rx="15" ry="6" fill="#0B1B3A"/>'
    '<path d="M17 19v10c0 3.3 6.7 6 15 6s15-2.7 15-6V19" fill="#1D4ED8"/>'
    '<path d="M17 29v10c0 3.3 6.7 6 15 6s15-2.7 15-6V29" fill="#38BDF8"/>'
    '<path d="M17 39v6c0 3.3 6.7 6 15 6s15-2.7 15-6v-6" fill="#0B1B3A"/>'
    '<circle cx="26" cy="31" r="1.8" fill="#fff"/><circle cx="38" cy="31" r="1.8" fill="#fff"/>'
    '</svg></div>'
)
CHAT_GREETING = (
    "Hello! I am SQL Buddy, your SQL guide. I can write queries, explain errors and answer quick "
    "questions about the tables in your sample data. Try one of the suggestions below."
)

with st.container(key="chat_widget"):
    with st.popover("Ask SQL Buddy", icon=":material/chat_bubble:"):
        st.markdown(CHAT_HEADER, unsafe_allow_html=True)
        with st.container(key="chat_body"):
            messages_box = st.container(height=300, border=False)
            if not ss.chat:
                with st.container(key="chat_chips"):
                    for i, suggestion in enumerate(CHAT_SUGGESTIONS):
                        if st.button(suggestion, key=f"chat_chip_{i}"):
                            send_chat(suggestion)
            with st.container(key="chat_input_row"):
                with st.form("chat_form", clear_on_submit=True, border=False):
                    field, send_col = st.columns([5, 2], vertical_alignment="center")
                    chat_text = field.text_input("Your question", key="chat_text", label_visibility="collapsed",
                                                 placeholder="Just type your query to get started")
                    sent = send_col.form_submit_button("Send", icon=":material/send:", use_container_width=True)
            if sent and chat_text.strip():
                send_chat(chat_text.strip())
            if ss.chat:
                with st.container(key="chat_clear"):
                    if st.button("Clear chat", key="chat_clear_btn"):
                        ss.chat = []
            with messages_box:
                if not ss.chat:
                    with st.chat_message("assistant", avatar=":material/smart_toy:"):
                        st.markdown(CHAT_GREETING)
                for message in ss.chat:
                    avatar = ":material/smart_toy:" if message["role"] == "assistant" else ":material/person:"
                    with st.chat_message(message["role"], avatar=avatar):
                        st.markdown(message["content"])

st.divider()
st.caption("SQL Buddy AI. Built with Python, Streamlit, LangChain and Groq.")
