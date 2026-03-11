"""Blog writer agent: expands the outline into a complete blog article."""

import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


def _get_llm():
    return ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.5,
        api_key=os.getenv("OPENAI_API_KEY"),
    )


def blog_writer_agent(outline: str, topic: str = "") -> str:
    """Expand the outline into a full blog article in Markdown."""
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an experienced blog writer. Given an outline, write a complete, "
                "engaging blog article in Markdown. Use clear headings (##, ###), "
                "short paragraphs, and a professional yet readable tone. "
                "Do not include meta comments like 'this section discusses'—just write the article.",
            ),
            (
                "human",
                "Topic: {topic}\n\nOutline:\n{outline}\n\n"
                "Write the full blog article in Markdown.",
            ),
        ]
    )
    chain = prompt | _get_llm()
    response = chain.invoke({"topic": topic, "outline": outline})
    return response.content if hasattr(response, "content") else str(response)
