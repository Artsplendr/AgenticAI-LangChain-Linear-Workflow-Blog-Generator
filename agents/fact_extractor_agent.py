"""Fact extraction agent: filters research and extracts important insights and concepts."""

import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


def _get_llm():
    return ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.2,
        api_key=os.getenv("OPENAI_API_KEY"),
    )


def fact_extractor_agent(research: str) -> str:
    """Filter research results and extract important insights and concepts."""
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert at extracting key facts and concepts from text. "
                "Given research content, output a structured list of: "
                "1) Key facts (with numbers or dates when relevant), "
                "2) Important concepts and definitions, "
                "3) Notable quotes or insights. "
                "Keep the output concise and well-organized. Use bullet points.",
            ),
            ("human", "Extract key facts and insights from this research:\n\n{research}"),
        ]
    )
    chain = prompt | _get_llm()
    response = chain.invoke({"research": research})
    return response.content if hasattr(response, "content") else str(response)
