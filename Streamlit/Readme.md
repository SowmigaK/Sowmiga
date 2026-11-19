\# AI SQL Query Generator



An AI-powered Streamlit application that generates SQL queries, fixes SQL errors, and explains SQL topics using LangChain and Groq.



\## Features



\- \*\*English to SQL:\*\* Convert natural-language questions into SQL queries.

\- \*\*SQL Error Fixer:\*\* Identify SQL errors and generate corrected queries.

\- \*\*Learn SQL:\*\* Understand SQL concepts through AI-powered explanations.



\## Technology Stack



\- Python

\- Streamlit

\- LangChain

\- Groq API



\## LangChain Integration



LangChain is used as the AI orchestration layer between the Streamlit interface and Groq:



\- `ChatGroq` connects the application to the configured Groq model.

\- `PromptTemplate` provides a reusable structure for SQL prompts.

\- `StrOutputParser` converts model responses into plain text.

\- LangChain Expression Language (LCEL) chains the prompt, model, and parser.



This separates prompt formatting, model interaction, and response parsing from the Streamlit interface.



\## Prerequisites



\- Python 3.9 or newer

\- A Groq API key



\## Run Locally



\### 1. Clone the repository



```bash

git clone <your-repository-url>

cd Sowmiga

cd Streamlit

```



\### 2. Create a virtual environment



```bash

python -m venv .venv

```



\### 3. Activate the virtual environment



\*\*Windows PowerShell:\*\*



```powershell

.venv\\Scripts\\Activate.ps1

```



\*\*Linux/macOS:\*\*



```bash

source .venv/bin/activate

```



\### 4. Install dependencies



```bash

pip install -r requirements.txt

```



\### 5. Configure your Groq API key



Create a folder named `.streamlit` inside the project folder.



Inside it, create a file named `secrets.toml`.



Add your API key in the following format:



```toml

GROQ\_API\_KEY = "your\_actual\_groq\_api\_key"

```



Replace the placeholder with your own API key.



\*\*Never upload your actual API key to GitHub.\*\*



\### 6. Run the application



```bash

streamlit run app.py

```



Open the local URL displayed in the terminal, usually:



http://localhost:8501



\## Deploy on Streamlit Community Cloud



1\. Push the project to GitHub.

2\. Sign in to Streamlit Community Cloud using GitHub.

3\. Click \*\*Create app\*\*.

4\. Select your repository and branch.

5\. Set the main file path to:



&#x20;  `Streamlit/app.py`



6\. Open \*\*Advanced settings → Secrets\*\*.

7\. Add the following:



```toml

GROQ\_API\_KEY = "your\_actual\_groq\_api\_key"

```



8\. Click \*\*Deploy\*\*.



\## Security



\- Never commit API keys or credentials to GitHub.

\- Keep `secrets.toml` private.

\- Use Streamlit secrets for deployment.

\- If an API key is accidentally exposed, revoke it and generate a new one.



\## Project Structure



```text

Streamlit/

│

├── app.py

├── Readme.md

├── requirements.txt

└── .streamlit/

&#x20;   └── secrets.toml

```





