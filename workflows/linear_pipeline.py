"""Linear pipeline: runs research -> fact extraction -> outline -> blog writing in sequence."""

from agents.research_agent import research_agent
from agents.fact_extractor_agent import fact_extractor_agent
from agents.outline_agent import outline_agent
from agents.blog_writer_agent import blog_writer_agent


def run_linear_pipeline(
    topic: str,
    use_tavily: bool = False,
) -> dict:
    """
    Run the full linear agent pipeline and return all intermediate outputs plus final article.

    Returns:
        dict with keys: research, facts, outline, article
    """
    research = research_agent(topic, use_tavily=use_tavily)
    facts = fact_extractor_agent(research)
    outline = outline_agent(facts, topic=topic)
    article = blog_writer_agent(outline, topic=topic)

    return {
        "research": research,
        "facts": facts,
        "outline": outline,
        "article": article,
    }
