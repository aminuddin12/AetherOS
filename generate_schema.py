import os
import json
import importlib
import pkgutil
from pydantic import BaseModel

def iter_namespace(pkg):
    return [name for _, name, _ in pkgutil.iter_modules(pkg.__path__, pkg.__name__ + ".")]

def main():
    import core.contracts as contracts
    
    schema_dir = "docs/id/05-contracts/schema"
    os.makedirs(schema_dir, exist_ok=True)
    
    snapshot = {}
    
    # Simple hardcoded list of major aggregates and models to snapshot
    # Or we can just crawl all modules
    packages = [
        "core.contracts.base",
        "core.contracts.common",
        "core.contracts.event",
        "core.contracts.identity",
        "core.contracts.kernel",
        "core.contracts.memory",
        "core.contracts.metrics",
        "core.contracts.organization",
        "core.contracts.plugin",
        "core.contracts.provider",
        "core.contracts.task",
        "core.contracts.tool",
        "core.contracts.worker",
        "core.contracts.workspace"
    ]
    
    for pkg_name in packages:
        try:
            pkg = importlib.import_module(pkg_name)
            for mod_name in iter_namespace(pkg):
                mod = importlib.import_module(mod_name)
                for attr_name in dir(mod):
                    attr = getattr(mod, attr_name)
                    if isinstance(attr, type) and issubclass(attr, BaseModel) and attr is not BaseModel:
                        # Exclude some base Pydantic things or local imports if needed
                        # To keep it clean, we just try to get json schema
                        if attr.__module__ == mod_name: # Ensure it's defined in this module
                            try:
                                schema = attr.model_json_schema()
                                snapshot[attr_name] = schema
                                
                                # Write individual file
                                file_path = os.path.join(schema_dir, f"{attr_name}.json")
                                with open(file_path, "w") as f:
                                    json.dump(schema, f, indent=2)
                            except Exception as e:
                                pass
        except Exception as e:
            print(f"Error loading {pkg_name}: {e}")

    # Write full snapshot
    with open("docs/id/05-contracts/contracts_snapshot.json", "w") as f:
        json.dump(snapshot, f, indent=2)
        
    print(f"Generated {len(snapshot)} JSON schemas.")

if __name__ == "__main__":
    main()
