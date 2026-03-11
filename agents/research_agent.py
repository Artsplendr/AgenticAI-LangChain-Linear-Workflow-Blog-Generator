"""Research agent: searches the web and gathers raw information about the topic."""

import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


def _get_llm():
    return ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.3,
        api_key=os.getenv("OPENAI_API_KEY"),
    )


def _research_with_llm(topic: str) -> str:
    """Use LLM to simulate or summarize research when Tavily is not available."""
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a research assistant. Given a topic, produce a concise research summary "
                "with key points, statistics, and notable facts. Write in clear paragraphs. "
                "If you cannot search the web, use your knowledge to provide a solid overview.",
            ),
            ("human", "Research the following topic and provide a summary:\n\n{topic}"),
        ]
    )
    chain = prompt | _get_llm()
    response = chain.invoke({"topic": topic})
    return response.content if hasattr(response, "content") else str(response)


def research_agent(topic: str, use_tavily: bool = False) -> str:
    """
    Gather raw information about the topic.
    If use_tavily is True and TAVILY_API_KEY is set, uses Tavily search; otherwise uses LLM.
    """
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if use_tavily and tavily_api_key:
        try:
            from tavily import TavilyClient

            client = TavilyClient(api_key=tavily_api_key)
            result = client.search(query=topic, max_results=5, search_depth="basic")
            texts = [r.get("content", "") for r in result.get("results", [])]
            raw = "\n\n".join(texts)
            if not raw.strip():
                return _research_with_llm(topic)
            # Summarize search results into one research blob
            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "You are a research assistant. Synthesize the following search results "
                        "into one coherent research summary with key facts and insights.",
                    ),
                    ("human", "Topic: {topic}\n\nSearch results:\n{raw}"),
                ]
            )
            chain = prompt | _get_llm()
            response = chain.invoke({"topic": topic, "raw": raw})
            return response.content if hasattr(response, "content") else str(response)
        except Exception:
            return _research_with_llm(topic)
    return _research_with_llm(topic)
