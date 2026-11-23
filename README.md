# SQL Buddy AI – Intelligent SQL Query Assistant

An AI-powered SQL assistant that helps users generate SQL queries using natural language. Built with Python, Streamlit, LangChain, and Groq LLM integration, SQL Buddy AI makes working with SQL queries easier through an interactive interface.

## Live Application

**Try SQL Buddy AI:** https://sqlbuddy-ai-sowmiga.streamlit.app/

## Project Overview

SQL Buddy AI is an intelligent SQL query assistant designed to simplify SQL query writing. Users can describe their database requirements in natural language, select their preferred database type, and receive AI-generated SQL query suggestions.

The application uses Large Language Models (LLMs) through Groq API integration to provide relevant SQL assistance.

## Key Features

- **AI-Powered SQL Generation** – Generate SQL queries from natural language instructions.
- **Database Selection** – Select a database type to receive SQL queries tailored to its syntax.
- **Intelligent Assistance** – Get AI-generated suggestions for SQL-related tasks.
- **Interactive Interface** – User-friendly interface developed using Streamlit.
- **LLM Integration** – Uses Groq API with LangChain for AI-powered responses.
- **Flexible Model Configuration** – Supports configurable Groq models.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| LangChain | LLM integration and prompt handling |
| Groq API | AI-powered query generation |
| Git & GitHub | Version control and project management |

## Application Screenshots

Add your application screenshots below to showcase the interface and functionality.

<!-- Replace these paths with your actual screenshot locations -->

### Main Application
![SQL Buddy AI Main Interface](screenshots/main-interface.png)

### SQL Query Generation
![SQL Query Generation](screenshots/query-generation.png)

### AI Response
![SQL Buddy AI Response](screenshots/ai-response.png)

## Installation and Setup

Follow these steps to run SQL Buddy AI locally.

**1. Clone the repository**

```bash
git clone https://github.com/SowmigaK/Sowmiga.git
```

**2. Navigate to the project directory**

```bash
cd Sowmiga
```

**3. Install dependencies**

```bash
pip install -r Streamlit/requirements.txt
```

**4. Configure the Groq API Key**

Create a `.env` file or configure Streamlit secrets with your API key.

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

Never upload your actual API key to GitHub.

**5. Run the application**

```bash
streamlit run Streamlit/app.py
```

The application will open in your browser.

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| `GROQ_API_KEY` | Groq API authentication key | Yes |
| `GROQ_MODEL` | LLM model used for generating responses | No |

Default model: `openai/gpt-oss-120b`

##  Project Structure

```text
Sowmiga/
│
├── Streamlit/
│   ├── app.py
│   └── requirements.txt
│
├── sqlbuddy/
│
├── tests/
│
├── .gitignore
├── pytest.ini
└── README.md
```

##  How It Works

1. The user opens the SQL Buddy AI application.
2. Selects the preferred database type.
3. Enters a natural-language request describing the SQL requirement.
4. The application processes the request using LangChain and the Groq LLM.
5. The AI generates a relevant SQL query suggestion.
6. The generated response is displayed in the application.

**Note:** SQL Buddy AI generates SQL query suggestions. It does not directly connect to databases or execute SQL queries.

## Future Enhancements

- Database connectivity and live query execution.
- SQL query validation and optimization.
- Support for additional database systems.
- Advanced SQL learning and assistance features.

## Developer

**Sowmiga K**

Aspiring Data Analyst | Python Developer

GitHub: https://github.com/SowmigaK
