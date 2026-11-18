import streamlit as st
from google import genai


# =====================================
# GEMINI AI CONNECTION
# =====================================

@st.cache_resource
def get_gemini_client():
    api_key = st.secrets.get("GEMINI_API_KEY")

    if not api_key:
        st.error("Gemini API key not found! Check secrets.toml")
        st.stop()

    return genai.Client(api_key=api_key)


def ask_gemini(prompt):
    client = get_gemini_client()

    response = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    return response.output_text


# =====================================
# 1. PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="AI SQL Query Generator",
    page_icon="🧠",
    layout="wide"
)


# =====================================
# 2. APPLICATION TITLE
# =====================================

st.title("🧠 SQL Buddy AI")

st.subheader("Your Personal AI SQL Query Generator")

st.write(
    "Convert simple English questions into SQL queries "
    "and learn SQL with easy explanations."
)

st.divider()


# =====================================
# 3. SIDEBAR
# =====================================

st.sidebar.title("⚙️ Settings")

database = st.sidebar.selectbox(
    "Select your database",
    ["MySQL", "PostgreSQL", "SQLite"]
)

st.sidebar.divider()

st.sidebar.info(
    "Learn SQL with the help of Artificial Intelligence."
)


# =====================================
# 4. MAIN APPLICATION TABS
# =====================================

tab1, tab2, tab3 = st.tabs([
    "💡 Generate SQL",
    "🔧 Fix SQL Errors",
    "📚 Learn SQL"
])


# =====================================
# 5. GENERATE SQL TAB
# =====================================

with tab1:
    st.header("English to SQL Generator")

    st.write("Enter your question in simple English.")

    question = st.text_area(
        "Your Question",
        placeholder="Example: Show all employees earning more than 30000",
        height=120,
        key="generate_question"
    )

    schema = st.text_area(
        "Database Table Structure (Optional)",
        placeholder="Table: employees\nColumns: employee_id, employee_name, salary",
        height=100,
        key="generate_schema"
    )

    if st.button("🚀 Generate SQL Query", type="primary"):

        if question.strip():

            prompt = f"""
You are an expert SQL developer and teacher.

Database: {database}

User question:
{question}

Database structure:
{schema if schema.strip() else "Not provided"}

Please:
1. Generate the correct SQL query.
2. Explain the query line by line.
3. Show an example of the expected output.
4. Mention assumptions if the table structure is missing.

Use simple English.
Do not execute the query.
"""

            try:
                with st.spinner("Gemini is generating your SQL..."):
                    answer = ask_gemini(prompt)

                st.success("SQL generated successfully!")
                st.markdown(answer)

            except Exception as e:
                st.error("Gemini connection failed.")
                st.exception(e)

        else:
            st.warning("Please enter your question.")


# =====================================
# 6. FIX SQL ERRORS TAB
# =====================================

with tab2:
    st.header("SQL Error Correction")

    wrong_query = st.text_area(
        "Enter your incorrect SQL query",
        placeholder="SELECT name FROM employees WHERE salary >",
        height=120
    )

    error = st.text_area(
        "Enter the error message",
        placeholder="Paste your SQL error here..."
    )

    if st.button("🔧 Fix SQL Query"):

        if wrong_query.strip():

            prompt = f"""
You are an expert SQL developer.

Database: {database}

Incorrect SQL query:
{wrong_query}

Error message:
{error if error.strip() else "No error message provided"}

Please:
1. Find the mistake in the SQL query.
2. Give the corrected SQL query.
3. Explain the correction in simple English.
4. Do not execute the query.
"""

            try:
                with st.spinner("Gemini is fixing your SQL query..."):
                    answer = ask_gemini(prompt)

                st.success("SQL query corrected successfully!")
                st.markdown(answer)

            except Exception as e:
                st.error("Gemini connection failed.")
                st.exception(e)

        else:
            st.warning("Please enter an SQL query.")


# =====================================
# 7. LEARN SQL TAB
# =====================================

with tab3:
    st.header("Learn SQL with AI")

    topic = st.selectbox(
        "Choose an SQL topic",
        [
            "SELECT",
            "WHERE",
            "ORDER BY",
            "GROUP BY",
            "HAVING",
            "JOINS",
            "SUBQUERIES",
            "PRIMARY KEY",
            "FOREIGN KEY"
        ]
    )

    if st.button("📖 Teach Me"):

        prompt = f"""
You are a friendly SQL teacher.

Teach me about the SQL topic: {topic}

Please explain:
1. What it is
2. Why it is used
3. Simple syntax
4. Easy examples
5. Common mistakes

Use simple English.
"""

        try:
            with st.spinner("Gemini is teaching you SQL..."):
                answer = ask_gemini(prompt)

            st.markdown(answer)

        except Exception as e:
            st.error("Gemini connection failed.")
            st.exception(e)


# =====================================
# 8. FOOTER
# =====================================

st.divider()

st.caption(
    "SQL Buddy AI | Built using Python and Streamlit"
)