from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv
import os

# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# GROQ MODEL
# ============================================================

llm = ChatGroq(
    model="openai/gpt-oss-20b", temperature=0, api_key=os.getenv("GROQ_API_KEY")
)


# ============================================================
# SEARCH AGENT
# ============================================================


def build_search_agent():

    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt="""
You are a web research agent.

Your task is to find information about the user's topic.

Instructions:
1. Use the web_search tool ONCE.
2. Use the user's research topic directly as the search query.
3. Return the search results exactly as provided by the tool.
4. Do not perform additional searches.
5. Do not invent sources or URLs.
""",
    )


# ============================================================
# READER AGENT
# ============================================================


def build_reader_agent():

    return create_agent(
        model=llm,
        tools=[scrape_url],
        system_prompt="""
You are a professional research reading agent.

Your task is to read information from web pages.

Instructions:

1. Examine the search results provided by the user.
2. Identify the most relevant URLs.
3. Use the scrape_url tool to retrieve the web page.
4. Extract useful factual information.
5. Prefer authoritative and relevant sources.
6. Do not invent information.
7. Return detailed information that can be used
   for writing the final research report.
""",
    )


# ============================================================
# NLP ANALYSIS CHAIN
# ============================================================

nlp_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an NLP analysis agent in a multi-agent research system.

Your task is to analyze the research text provided to you
using natural language processing techniques.

Perform the following tasks:

1. Identify the main topic of the research.
2. Extract the most important keyphrases and concepts.
3. Summarize the research in a concise manner.
4. Extract the most important factual points.
5. Identify important benefits, limitations, challenges,
   or implications when they are present in the text.

Important rules:
- Use only the information provided.
- Do not invent facts.
- Do not add information from your own knowledge.
- Preserve the meaning of the original research.
- Remove unnecessary repetition.
- Focus on information relevant to the research topic.

Return the analysis in the following structure:

Main Topic:
...

Keyphrases:
- ...
- ...
- ...

Summary:
...

Key Findings:
- ...
- ...
- ...

Benefits:
- ...

Limitations:
- ...

Challenges:
- ...

Implications:
- ...
""",
        ),
        (
            "human",
            """
Analyze the following research text using NLP.

Research Text:
{research}
""",
        ),
    ]
)

nlp_chain = nlp_prompt | llm | StrOutputParser()


# ============================================================
# WRITER CHAIN - LCEL
# ============================================================

writer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert research writer.

Write clear, structured, factual and professional
research reports.

Use only the research and NLP analysis provided to you.
Do not invent facts or sources.

The NLP analysis is a processed representation of
the research and should be used to improve the
organization, relevance and clarity of the report.
""",
        ),
        (
            "human",
            """
Write a detailed research report on the topic below.

Topic:
{topic}


Original Research:
{research}


NLP Analysis:
{nlp_analysis}


Use the NLP Analysis to identify the most relevant
information from the original research.

Structure the report as:

# Introduction

Explain the topic and its importance.

# Key Findings

Provide at least 3 well-explained findings.

# Detailed Analysis

Explain important concepts, developments,
advantages, limitations and implications.

# Conclusion

Summarize the major findings.

# Sources

List the URLs available in the original research.

Requirements:
- Be factual.
- Use only the provided research.
- Use the NLP analysis to improve information selection.
- Be professional.
- Avoid unnecessary repetition.
- Do not invent facts.
- Do not invent URLs.
""",
        ),
    ]
)

writer_chain = writer_prompt | llm | StrOutputParser()


# ============================================================
# CRITIC CHAIN - LCEL
# ============================================================

critic_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a strict but constructive research critic.

Evaluate the quality, accuracy, structure,
completeness and clarity of the research report.
""",
        ),
        (
            "human",
            """
Review the following research report.

Report:
{report}

Evaluate it strictly.

Respond in exactly this format:

Score: X/10

Strengths:
- ...
- ...
- ...

Areas to Improve:
- ...
- ...
- ...

One line verdict:
...

Consider:
- Accuracy
- Depth
- Structure
- Clarity
- Sources
- Completeness
""",
        ),
    ]
)

critic_chain = critic_prompt | llm | StrOutputParser()
