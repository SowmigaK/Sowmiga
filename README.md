# SQL Buddy AI

Streamlit app with five tabs and a floating chat assistant (bottom-right on every tab):

- **Generate**: English to SQL, with download, history and "run on sample data".
- **Fix & explain**: fix an error, explain a query, make it faster, or convert between MySQL, PostgreSQL and SQLite.
- **Practice**: 10 graded challenges. Answers are checked by comparing results, not wording.
- **Learn**: short lessons on core SQL topics.
- **Try on sample data**: run SQL on sample databases, your own CSV, or your own tables, with charts and a table diagram.

## Run
    pip install -r requirements.txt
    export GROQ_API_KEY=...          # without it the app starts in demo mode
    streamlit run app.py

## Test
    pip install -r requirements-dev.txt
    pytest

## Settings (environment variables)
- `GROQ_API_KEY`: live AI. `GROQ_MODEL`: model name.
- `SQLBUDDY_DEMO=1`: force demo mode (used by tests).
- `FREE_LIMIT`: free AI requests per session (default 20).
