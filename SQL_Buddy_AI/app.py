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

log = logging.getLogger("sqlbuddy")
MAX_CSV_ROWS = 5000
CHAT_SUGGESTIONS = ["What is a JOIN?", "WHERE vs HAVING?", "How do I find duplicates?"]

st.set_page_config(page_title="SQL Buddy AI", page_icon="SQL", layout="wide")

CSS = """
<style>
.sb-hero {background:#0B1B3A; color:#fff; padding:22px 28px; border-radius:14px; margin-bottom:12px;}
.sb-hero h1 {color:#fff; font-size:2rem; margin:0 0 4px 0; padding:0;}
.sb-hero p {color:#C9D6F2; margin:0; font-size:1rem;}
.sb-note {background:#E4ECFF; border-left:4px solid #1D4ED8; padding:10px 14px; border-radius:6px; margin:6px 0 14px 0;}
.stTabs [data-baseweb="tab-highlight"] {background:#F59E0B;}
.stTabs [aria-selected="true"] {color:#0B1B3A; font-weight:600;}
/* ---------- sidebar ---------- */
section[data-testid="stSidebar"] .sb-side-title {font-size:.8rem; font-weight:700; letter-spacing:.06em;
    text-transform:uppercase; color:#1D4ED8; margin:0 0 6px 0;}
section[data-testid="stSidebar"] [data-testid="stMetricLabel"] p {font-weight:600; color:#0B1B3A;}
section[data-testid="stSidebar"] [data-testid="stMetricValue"] {color:#1D4ED8; font-weight:700;}
.sb-steps {background:#fff; border:1px solid #C9D6F2; border-radius:12px; padding:12px 14px; margin-top:4px;}
.sb-step {display:flex; gap:10px; align-items:flex-start; margin:0 0 10px 0; font-size:.9rem; line-height:1.35; color:#0B1B3A;}
.sb-step:last-child {margin-bottom:0;}
.sb-num {flex:0 0 22px; height:22px; border-radius:50%; background:#1D4ED8; color:#fff; font-size:.75rem;
    font-weight:700; display:flex; align-items:center; justify-content:center; margin-top:1px;}
.sb-tip {font-size:.85rem; color:#3B4D75; margin-top:12px;}

/* ---------- floating chat assistant ---------- */
.st-key-chat_widget {position:fixed; bottom:22px; right:22px; z-index:1000; width:auto;}
.st-key-chat_widget > div > div > button, .st-key-chat_widget [data-testid="stPopover"] > button {
    background:linear-gradient(135deg,#1D4ED8,#2DD4BF); color:#fff; border:none; border-radius:999px;
    padding:10px 22px; font-weight:600; box-shadow:0 6px 18px rgba(11,27,58,.35);}
.st-key-chat_widget [data-testid="stPopover"] > button:hover {filter:brightness(1.08); color:#fff;}
div[data-testid="stPopoverBody"] {width:min(380px, 94vw); max-height:80vh; overflow:auto; padding:0;
    border-radius:22px; border:1px solid #C9D6F2; box-shadow:0 12px 36px rgba(11,27,58,.28); background:#fff;}
.sb-chat-head {background:linear-gradient(120deg,#CFF7F2 0%,#7FE3DA 100%); padding:16px 18px;
    display:flex; align-items:center; gap:12px; border-radius:22px 22px 0 0;}
.sb-chat-logo {font-size:1.45rem; font-weight:800; color:#0B1B3A; line-height:1;}
.sb-chat-logo span {background:#1D4ED8; color:#fff; padding:2px 8px; border-radius:8px; margin-left:4px; font-size:1.1rem;}
.sb-chat-sub {font-size:.78rem; color:#0B1B3A; margin-top:4px; font-weight:500;}
.sb-chat-avatar {margin-left:auto; width:46px; height:46px; border-radius:50%; background:#fff;
    display:flex; align-items:center; justify-content:center; font-size:1.6rem; box-shadow:0 2px 6px rgba(11,27,58,.2);}
.sb-greet {background:#E4F1FF; color:#0B1B3A; padding:12px 14px; border-radius:16px 16px 16px 4px;
    margin:14px 16px 8px 16px; font-size:.92rem; line-height:1.45;}
.sb-chat-hint {font-size:.75rem; color:#5B6B8F; margin:0 16px 6px 16px;}
div[data-testid="stPopoverBody"] [data-testid="stVerticalBlock"] {gap:.5rem;}
div[data-testid="stPopoverBody"] div[data-testid="stVerticalBlockBorderWrapper"] > div {padding-left:12px; padding-right:12px;}
/* suggestion chips */
div[data-testid="stPopoverBody"] [class*="st-key-chat_chip_"] {padding:0 16px;}
div[data-testid="stPopoverBody"] [class*="st-key-chat_chip_"] button {border:1.5px solid #1D4ED8; background:#fff;
    color:#1D4ED8; border-radius:999px; padding:4px 14px; font-size:.85rem; min-height:0; width:auto;}
div[data-testid="stPopoverBody"] [class*="st-key-chat_chip_"] button:hover {background:#E4F1FF; color:#1D4ED8;}
/* message bubbles */
div[data-testid="stPopoverBody"] [data-testid="stChatMessage"] {background:#E4F1FF; border-radius:16px; padding:10px 12px;}
div[data-testid="stPopoverBody"] [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {background:#F1F5FF;}
/* input row */
div[data-testid="stPopoverBody"] [data-testid="stForm"] {border:none; padding:0 16px 8px 16px;}
div[data-testid="stPopoverBody"] [data-testid="stForm"] input {border-radius:999px; border:1.5px solid #7FA6F5; padding:10px 16px;}
div[data-testid="stPopoverBody"] [data-testid="stForm"] button {border-radius:999px; background:#1D4ED8; color:#fff; border:none; width:100%;}
.st-key-chat_clear {padding:0 16px 14px 16px;}
.st-key-chat_clear button {border-radius:999px; font-size:.8rem;}
/* Force all primary buttons to dark blue */
.stApp button[data-testid="stBaseButton-primary"] {
    background: #172554 !important;
    background-color: #172554 !important;
    color: #FFFFFF !important;
    border: 1px solid #172554 !important;
}

/* Hover */
.stApp button[data-testid="stBaseButton-primary"]:hover {
    background: #1E40AF !important;
    background-color: #1E40AF !important;
    color: #FFFFFF !important;
    border-color: #1E40AF !important;
}
/* Active tab underline */
.stTabs [data-baseweb="tab-highlight"] {
    background-color: #172554 !important;
}

/* Active tab text */
.stTabs button[aria-selected="true"] {
    color: #172554 !important;
}

/* Checkbox */
.stCheckbox [role="checkbox"][aria-checked="true"] {
    background-color: #172554 !important;
    border-color: #172554 !important;
}

/* Text input and text area focus border */
.stTextInput div[data-baseweb="input"]:focus-within,
.stTextArea div[data-baseweb="textarea"]:focus-within {
    border-color: #172554 !important;
    box-shadow: 0 0 0 1px #172554 !important;
}
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
    st.sidebar.write("Groq key detected:", bool(_secret("GROQ_API_KEY")))
    return build_llm(
        api_key=_secret("GROQ_API_KEY"),
        model=os.getenv("GROQ_MODEL", DEFAULT_MODEL),
        demo=False,
    )


ss = st.session_state
if "sandbox" not in ss:          # tables used by "Try it on sample data" and the chat assistant
    ss.sandbox = Sandbox()
if "practice_sb" not in ss:      # fixed tables used by Practice, never changed by the user
    ss.practice_sb = Sandbox()
ss.setdefault("chat", [])
ss.setdefault("history", [])
ss.setdefault("solved", set())
ss.setdefault("checks", {})
ss.setdefault("feedback", {})
ss.setdefault("loaded_dataset", DEFAULT_DATASET)

llm = get_llm()
sandbox: Sandbox = ss.sandbox



def guarded(fn, *args):
    """Run an AI call with friendly error handling."""
    try:
        return fn(*args)
    except Exception as e:
        st.error(f"AI request failed: {e}")
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
    '<div class="sb-hero"><h1>SQL Buddy AI</h1>'
    "<p>Ask in plain English, get working SQL, run it on sample data and practise until it sticks.</p></div>",
    unsafe_allow_html=True,
)

database = st.sidebar.selectbox("Choose your database", prompts.DIALECTS)
st.sidebar.caption("SQL will be written for the database you select here.")
st.sidebar.divider()
if llm.is_demo:
    st.sidebar.warning("Demo mode: answers are pre-written. Set GROQ_API_KEY to use live AI.")
st.sidebar.markdown(
    '<div class="sb-side-title">Where to start</div>'
    '<div class="sb-steps">'
    '<div class="sb-step"><div class="sb-num">1</div><div><b>Generate:</b> describe the query you need in plain English.</div></div>'
    '<div class="sb-step"><div class="sb-num">2</div><div><b>Try on sample data:</b> run the SQL and see real rows.</div></div>'
    '<div class="sb-step"><div class="sb-num">3</div><div><b>Practice:</b> solve challenges to learn.</div></div>'
    "</div>"
    '<div class="sb-tip">Need quick help? Use the <b>Ask SQL Buddy</b> chat button at the bottom right.</div>',
    unsafe_allow_html=True,
)

tab_gen, tab_fix, tab_practice, tab_learn, tab_play = st.tabs(
    ["Generate", "Fix & explain", "Practice", "Learn", "Try on sample data"]
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
        format_func=lambda c: f"{c.level}: {c.title} ({c.concept})",
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


CHAT_GREETING = (
    "Hello! I am SQL Buddy, your SQL guide. I can help you write queries, understand concepts "
    "and fix errors. Try one of the suggestions below!"
)

with st.container(key="chat_widget"):
    with st.popover("Ask SQL Buddy"):
        st.markdown(
            '<div class="sb-chat-head"><div><div class="sb-chat-logo">SQL Buddy<span>AI</span></div>'
            '<div class="sb-chat-sub">Your Anytime SQL Coach</div></div>'
            '<div class="sb-chat-avatar">SQL</div></div>',
            unsafe_allow_html=True,
        )
        st.markdown(f'<div class="sb-greet">{CHAT_GREETING}</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="sb-chat-hint">Short answers about SQL. It knows the tables in your sample-data tab.</div>',
            unsafe_allow_html=True,
        )
        messages_box = st.container()
        if not ss.chat:
            for i, suggestion in enumerate(CHAT_SUGGESTIONS):
                if st.button(suggestion, key=f"chat_chip_{i}"):
                    send_chat(suggestion)
        with st.form("chat_form", clear_on_submit=True):
            chat_text = st.text_input("Your question", key="chat_text", label_visibility="collapsed",
                                      placeholder="Just type your question about SQL")
            sent = st.form_submit_button("Send")
        if sent and chat_text.strip():
            send_chat(chat_text.strip())
        if ss.chat and st.button("Clear chat", key="chat_clear"):
            ss.chat = []
        with messages_box:
            for message in ss.chat:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

st.divider()
st.caption("SQL Buddy AI. Built with Python, Streamlit, LangChain and Groq.")
