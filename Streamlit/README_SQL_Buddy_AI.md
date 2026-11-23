# SQL Buddy AI – AI-Powered SQL Assistant

SQL Buddy AI is a Streamlit application that helps users write, troubleshoot, and learn SQL with the assistance of a large language model served through Groq. Users can describe a task in plain English, provide an optional database schema, and receive a suggested SQL query with an explanation.

The application is designed as a learning and productivity assistant. **It generates and explains SQL; it does not connect to or execute queries against a database.**

---

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Configure the Groq API Key](#configure-the-groq-api-key)
- [Run the Application](#run-the-application)
- [Deploy on Streamlit Community Cloud](#deploy-on-streamlit-community-cloud)
- [Configuration](#configuration)
- [Security Notes](#security-notes)
- [Limitations](#limitations)

---

## Features

### 1. English-to-SQL Generator
- Convert a question written in plain English into a SQL query.
- Choose the target SQL dialect: MySQL, PostgreSQL, or SQLite.
- Optionally provide table and column details to give the model more context.
- Receive a line-by-line explanation, an example of the expected output, and any assumptions made when schema details are missing.

### 2. SQL Error Fixer
- Submit an incorrect SQL query.
- Optionally include the error message returned by your SQL tool.
- Get a suggested corrected query and a simple explanation of the correction.

### 3. Learn SQL
- Select a topic and request an AI-generated lesson.
- Available topics include `SELECT`, `WHERE`, `ORDER BY`, `GROUP BY`, `HAVING`, `JOINS`, `SUBQUERIES`, `PRIMARY KEY`, and `FOREIGN KEY`.
- Learn through explanations, syntax, examples, and common mistakes.

---

## How It Works

1. The user selects a database dialect and opens one of the application tabs.
2. The user enters a natural-language question, an SQL query to troubleshoot, or an SQL topic to study.
3. Streamlit passes the request to the Python application.
4. LangChain builds the prompt and sends it to the configured Groq chat model.
5. The model's response is converted to text and displayed in the Streamlit interface.

### LangChain Integration

- **`ChatGroq`** connects the application to a chat model hosted by Groq.
- **`PromptTemplate`** prepares the prompt for the model.
- **`StrOutputParser`** converts the model response into a text output.
- **LangChain Expression Language (LCEL)** connects the prompt, model, and output parser into a processing chain.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Web interface |
| LangChain Core | Prompt templates and output parsing |
| LangChain Groq | Connection to the Groq chat model |
| Groq API | AI model inference |

---

## Project Structure

```text
Streamlit/
├── app.py
├── README.md
├── requirements.txt
└── .streamlit/
    └── secrets.toml       # Local secret configuration; do not commit
```

The `.streamlit/secrets.toml` file is created locally during setup. It should not be uploaded to a public repository.

---

## Prerequisites

Before running the project, make sure you have:

- Python 3.9 or newer.
- A Groq API key.
- Git, if you are cloning the project from GitHub.
- Internet access while using the AI features.

---

## Installation and Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
```

Move into the project directory. If the project is inside a folder named `Streamlit` in your repository:

```bash
cd <repository-folder>/Streamlit
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows Command Prompt**

```cmd
.venv\Scripts\activate.bat
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

### 4. Install the dependencies

If the project includes `requirements.txt`, run:

```bash
pip install -r requirements.txt
```

The application uses these direct Python packages:

```bash
pip install streamlit langchain-core langchain-groq
```

---

## Configure the Groq API Key

The application reads the API key from the `GROQ_API_KEY` environment variable or Streamlit secrets.

### Option A: Streamlit secrets (recommended for local use)

1. Create a folder named `.streamlit` in the project directory.
2. Inside it, create a file named `secrets.toml`.
3. Add your Groq API key:

```toml
GROQ_API_KEY = "your_groq_api_key"
```

### Option B: Environment variable

**Windows PowerShell**

```powershell
$env:GROQ_API_KEY = "your_groq_api_key"
```

**macOS / Linux**

```bash
export GROQ_API_KEY="your_groq_api_key"
```

Replace the example value with your own key. Do not paste your real API key into source code, README files, screenshots, or public commits.

---

## Run the Application

From the project directory, with the virtual environment activated, run:

```bash
streamlit run app.py
```

Streamlit will display a local address in the terminal. Open it in your browser. The default local address is usually:

```text
http://localhost:8501
```

---

## Deploy on Streamlit Community Cloud

1. Push the project to a GitHub repository.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/) and sign in.
3. Choose **Create app**.
4. Select the repository and branch containing the project.
5. Set the application entry point to the location of `app.py` in the repository. For example, use `Streamlit/app.py` if the folder is named `Streamlit` at the repository root.
6. Open the app's **Advanced settings** or **Secrets** section.
7. Add the secret in TOML format:

```toml
GROQ_API_KEY = "your_groq_api_key"
```

8. Save the settings and deploy the application.

Keep the API key in the deployment secrets configuration; never add it to the GitHub repository.

---

## Configuration

The application supports the following configuration values:

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | Yes | API key used to authenticate with Groq. It can be supplied through an environment variable or Streamlit secrets. |
| `GROQ_MODEL` | No | Groq model identifier. If not set, the application uses `openai/gpt-oss-120b` by default. |

To override the default model, set `GROQ_MODEL` to a model identifier available to your Groq account.

---

## Security Notes

- Never commit `.streamlit/secrets.toml` or any file containing a real API key.
- Add local secret files and virtual-environment folders to `.gitignore`.
- Use Streamlit secrets for hosted deployments.
- If an API key is exposed, revoke it in your Groq account and create a replacement.
- Review AI-generated SQL before using it in any database environment.

---

## Limitations

- SQL queries are generated as suggestions and are **not executed** by this application.
- The selected database option guides the model's response; the application does not establish a database connection.
- Generated answers may contain errors or assumptions. Check the query against your actual schema and database dialect before use.
- AI features require a valid Groq API key and an available model.

---

*Built with Python, Streamlit, LangChain, and Groq.*
