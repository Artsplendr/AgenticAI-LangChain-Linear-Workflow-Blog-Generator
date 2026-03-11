"""Outline agent: creates a structured blog outline from extracted facts."""

import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


def _get_llm():
    return ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.4,
        api_key=os.getenv("OPENAI_API_KEY"),
    )


def outline_agent(facts: str, topic: str = "") -> str:
    """Create a structured blog outline from extracted facts."""
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert blog editor. Create a clear, engaging outline for a blog post. "
                "Include: a compelling title, an intro section, 3–5 main sections with subpoints, "
                "and a conclusion. Output in Markdown (headers with ##, ###, bullet points). "
                "The outline should be detailed enough for a writer to expand into full paragraphs.",
            ),
            (
                "human",
                "Topic: {topic}\n\nKey facts and insights to use:\n{facts}\n\n"
                "Produce a structured blog outline in Markdown.",
            ),
        ]
    )
    chain = prompt | _get_llm()
    response = chain.invoke({"topic": topic, "facts": facts})
    return response.content if hasattr(response, "content") else str(response)
