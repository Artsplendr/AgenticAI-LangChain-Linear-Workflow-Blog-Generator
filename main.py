"""CLI entry point: run the linear blog generation pipeline."""

import argparse
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from workflows.linear_pipeline import run_linear_pipeline
from utils.markdown_exporter import export_to_markdown_file


def main():
    parser = argparse.ArgumentParser(
        description="Generate a blog article from a topic using a linear agent pipeline."
    )
    parser.add_argument(
        "topic",
        type=str,
        help="Topic for the blog post (e.g. 'Benefits of Python for data science')",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Optional path to save the article as Markdown (e.g. examples/my_blog.md)",
    )
    parser.add_argument(
        "--tavily",
        action="store_true",
        help="Use Tavily web search for the research step (requires TAVILY_API_KEY)",
    )
    args = parser.parse_args()

    print(f"Topic: {args.topic}")
    print("Running pipeline: Research → Facts → Outline → Article\n")

    result = run_linear_pipeline(args.topic, use_tavily=args.tavily)

    print("--- Research (summary) ---")
    print(result["research"][:500] + "..." if len(result["research"]) > 500 else result["research"])
    print("\n--- Facts ---")
    print(result["facts"][:400] + "..." if len(result["facts"]) > 400 else result["facts"])
    print("\n--- Outline ---")
    print(result["outline"][:400] + "..." if len(result["outline"]) > 400 else result["outline"])
    print("\n--- Article ---")
    print(result["article"])

    if args.output:
        out_path = export_to_markdown_file(result["article"], args.output)
        print(f"\nSaved article to: {out_path}")

    return result


if __name__ == "__main__":
    main()
