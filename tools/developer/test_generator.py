import os
import ast
from pathlib import Path

def generate_test_for_file(filepath: Path, test_dir: Path):
    with open(filepath, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())
        
    classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    
    if not classes and not functions:
        return
        
    rel_path = filepath.relative_to(Path("core"))
    test_filepath = test_dir / rel_path.parent / f"test_{rel_path.name}"
    
    if test_filepath.exists():
        return
        
    test_filepath.parent.mkdir(parents=True, exist_ok=True)
    
    module_path = "core." + str(rel_path.with_suffix("")).replace(os.sep, ".")
    
    lines = [
        "import pytest",
        f"import {module_path}",
        ""
    ]
    
    for cls in classes:
        lines.append(f"def test_{cls.name}_initialization():")
        lines.append(f"    # TODO: Implement test for {cls.name}")
        lines.append("    pass")
        lines.append("")
        
    for func in functions:
        lines.append(f"def test_{func.name}():")
        lines.append(f"    # TODO: Implement test for {func.name}")
        lines.append("    pass")
        lines.append("")
        
    with open(test_filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        
def run():
    print("Generating test stubs...")
    core_dir = Path("core")
    
    for section in ["contracts", "kernel", "execution"]:
        section_dir = core_dir / section
        test_dir = Path("tests") / section
        
        for root, _, files in os.walk(section_dir):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    filepath = Path(root) / file
                    generate_test_for_file(filepath, test_dir)
                    
    print("Done generating test stubs.")

if __name__ == "__main__":
    run()
