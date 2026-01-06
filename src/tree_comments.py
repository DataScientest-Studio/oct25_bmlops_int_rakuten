# src/tree_comments.py
# imports 
from __future__ import annotations
from pathlib import Path

# comments
COMMENTS = {
    "airflow": "Workflow orchestration (ETL, scheduling)",
    "airflow/dags": "Production DAGs",
    "fastapi": "Inference & trigger API",
    "logs": "Runtime logs (ignored in Git)",
        }

CSS = """
<style>
.comment {
  margin-left: 12px;
  color: #666;
  font-style: italic;
}
</style>
""".strip()

def comment_tree():
    # Project root = parent of /src
    project_root = Path(__file__).resolve().parents[1]

    in_file = project_root / "tree.html"
    out_file = project_root / "tree_commented.html"

    if not in_file.exists():
        raise FileNotFoundError(f"Input HTML not found: {in_file}")

    html = in_file.read_text(encoding="utf-8")

    # Inject CSS once (if not already present)
    if "<style>" not in html:
        if "<head>" in html:
            html = html.replace("<head>", "<head>\n" + CSS + "\n", 1)
        else:
            # fallback: put CSS at start (rare, but safe)
            html = CSS + "\n" + html

    # adding comments
    for folder, comment in COMMENTS.items():
        html = html.replace(
            f'>{folder}</a><br>',
            f'>{folder}</a><span class="comment"> — {comment}</span><br>'
        )

    out_file.write_text(html, encoding="utf-8")
    print(f"Wrote: {out_file}")


if __name__ == "__main__":
    comment_tree()