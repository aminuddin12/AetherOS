import os
import ast

FORBIDDEN_MODULES = [
    "openai", "fastapi", "sqlalchemy", "redis", "langgraph", "openhands",
    "provider", "workspace", "database", "docker", "flask", "django",
    "httpx", "requests", "aiohttp", "celery", "dramatiq",
]

FORBIDDEN_INTERNAL_IMPORTS = [
    "core.kernel.internal",
]

def check_imports(directory):
    errors = []

    for root, _, files in os.walk(directory):
        for file in files:
            if not file.endswith(".py"):
                continue
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                try:
                    tree = ast.parse(f.read(), filename=path)
                except SyntaxError as e:
                    errors.append(f"SYNTAX ERROR in {path}: {e}")
                    continue

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        for forbidden in FORBIDDEN_MODULES + FORBIDDEN_INTERNAL_IMPORTS:
                            if alias.name == forbidden or alias.name.startswith(forbidden + "."):
                                errors.append(f"{path}: forbidden import '{alias.name}'")
                elif isinstance(node, ast.ImportFrom):
                    if node.level == 0 and node.module:
                        for forbidden in FORBIDDEN_MODULES + FORBIDDEN_INTERNAL_IMPORTS:
                            if node.module == forbidden or node.module.startswith(forbidden + "."):
                                errors.append(f"{path}: forbidden 'from {node.module}'")

    return errors

if __name__ == "__main__":
    print("=" * 60)
    print("Architecture Validation: core/execution/")
    print("=" * 60)

    errs = check_imports("core/execution")
    if errs:
        print(f"\nFAILED — {len(errs)} violation(s):\n")
        for e in errs:
            print(f"  ❌ {e}")
        exit(1)
    else:
        print("\n✅ PASSED — No forbidden imports found.")

    print("\n" + "=" * 60)
    print("Architecture Validation: core/kernel/ (re-check)")
    print("=" * 60)

    errs2 = check_imports("core/kernel")
    if errs2:
        print(f"\nFAILED — {len(errs2)} violation(s):\n")
        for e in errs2:
            print(f"  ❌ {e}")
        exit(1)
    else:
        print("\n✅ PASSED — No forbidden imports found.")

    print("\n✅ All architecture validations passed.")
