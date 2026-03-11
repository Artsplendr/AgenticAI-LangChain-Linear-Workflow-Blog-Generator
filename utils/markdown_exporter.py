"""Export blog article (or any text) to a Markdown file."""

from pathlib import Path


def export_to_markdown_file(content: str, path: str | Path) -> Path:
    """
    Write content to a Markdown file.

    Args:
        content: String content (e.g. blog article in Markdown).
        path: File path (string or Path). Created parent dirs if needed.

    Returns:
        Resolved Path of the written file.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path.resolve()
