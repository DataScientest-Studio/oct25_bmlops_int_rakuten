import ast
import json
from pathlib import Path

notebook = Path("/home/robfra/0_Portfolio_Projekte/Rakuten_Classification/notebooks/Rakuten_1.ipynb")  # passe an
modules = set()

nb = json.loads(notebook.read_text())

for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        code = "".join(cell["source"])
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for n in node.names:
                        modules.add(n.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        modules.add(node.module.split('.')[0])
        except:
            pass

print("\nGefundene Module:")
print(sorted(modules))
