# ResearchNLP: Multi-Agent NLP-Based Research Assistant

ResearchNLP is a multi-stage, LLM-powered research assistant that searches the web, retrieves relevant information, performs NLP-based analysis, generates a structured research report, and evaluates the final report using a critic chain.

The system combines web search, web content extraction, semantic NLP analysis, LLM-based report generation, and automated evaluation into a single research pipeline.

---

## Project Overview

Traditional research requires manually searching multiple sources, reading large amounts of information, identifying important points, and organizing them into a report.

ResearchNLP automates this workflow using a sequence of specialized agents and LLM chains.

The system accepts a research topic from the user and processes it through five stages:

1. Search Agent
2. Reader Agent
3. NLP Analysis
4. Writer Chain
5. Critic Chain

The final output is a structured research report along with the intermediate NLP analysis and critic feedback.

---

##  System Architecture

```text
                    User Research Topic
                            │
                            ▼
                  ┌───────────────────┐
                  │   Search Agent    │
                  │                   │
                  │ Web Search        │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │   Reader Agent    │
                  │                   │
                  │ Web Page Scraping │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │   NLP Analysis    │
                  │                   │
                  │ • Topic Detection │
                  │ • Keyphrases      │
                  │ • Summarization   │
                  │ • Key Findings    │
                  │ • Benefits        │
                  │ • Limitations     │
                  │ • Challenges      │
                  │ • Implications    │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │   Writer Chain    │
                  │                   │
                  │ Research Report   │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │   Critic Chain    │
                  │                   │
                  │ Quality Evaluation│
                  └─────────┬─────────┘
                            │
                            ▼
                    Final Research Report

Pipeline Stages
1. Search Agent
The Search Agent uses a web search tool to find relevant information about the user's research topic.
Its responsibilities include:
- Searching for relevant sources
- Finding recent and detailed information
- Returning source information and URLs
- Avoiding invented sources

2. Reader Agent
The Reader Agent examines the search results and identifies relevant web pages.
It then uses the web scraping tool to retrieve deeper content from the selected source.
Its responsibilities include:
- Identifying relevant URLs
- Scraping web pages
- Extracting useful information
- Focusing on factual and relevant content

3. NLP Analysis
The NLP Analysis stage processes the retrieved research using an LLM-powered semantic NLP approach.
It performs:
- Main topic identification
- Keyphrase extraction
- Text summarization
- Key finding extraction
- Benefit extraction
- Limitation identification
- Challenge identification
- Implication identification
The structured NLP output is then passed to the Writer Chain.

4. Writer Chain
The Writer Chain combines:
- Original retrieved research
- NLP analysis
- User's research topic
It generates a structured research report containing:
- Introduction
- Key Findings
- Detailed Analysis
- Conclusion
- Sources

5. Critic Chain
The Critic Chain evaluates the generated report.
It checks:
- Accuracy
- Depth
- Structure
- Clarity
- Sources
- Completeness
The critic produces a score, strengths, areas for improvement, and an overall verdict.


 LLM Integration
The project uses the Groq API with the following model:
openai/gpt-oss-20b

The LLM is used across multiple stages for:
- Semantic NLP analysis
- Research report generation
- Report evaluation
The project uses LangChain to organize the agents and LLM chains.

.
 Technologies Used
- Python
- Streamlit
- LangChain
- Groq API
- GPT-OSS-20B
- BeautifulSoup
- DuckDuckGo Search
- python-dotenv


Installation

1. Clone the repository
git clone <YOUR_GITHUB_REPOSITORY_URL>

Move into the project directory:
cd multi-agent-research-nlp

2. Create a virtual environment
python -m venv venv

Activate it on Windows:
venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Configure the API key
Create a .env file in the project root.
Add:
GROQ_API_KEY=your_groq_api_key_here

The .env file is intentionally excluded from GitHub using .gitignore.
5. Run the application
streamlit run app.py

The application will open in the browser.
💡 Example
Input
How does Retrieval-Augmented Generation improve factual accuracy in large language models?

Pipeline
Search
   ↓
Web Content Retrieval
   ↓
NLP Analysis
   ↓
Report Generation
   ↓
Report Evaluation

NLP Analysis Output

The system extracts:
Main Topic
Keyphrases
Summary
Key Findings
Benefits
Limitations
Challenges
Implications

📊 Output
The application displays:
- Search Results
- Scraped Content
- NLP Analysis
- Research Report
- Critic Feedback
The final research report can also be downloaded from the Streamlit interface.

Security
API credentials are stored in an environment file.
The following files are excluded from version control:
.env
venv/
__pycache__/
*.pyc


🔮 Future Scope
Possible future improvements include:
- Multi-source document comparison
- PDF and document research support
- Citation verification
- More advanced factuality evaluation
- Persistent research memory
- Source ranking and credibility scoring
- Human feedback integration
- Local or open-source embedding-based retrieval