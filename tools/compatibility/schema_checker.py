import sys
import json
import importlib
import pkgutil
import inspect
from pathlib import Path
from pydantic import BaseModel

def get_all_models(package_name):
    models = {}
    package = importlib.import_module(package_name)
    prefix = package.__name__ + "."
    
    for _, modname, ispkg in pkgutil.walk_packages(package.__path__, prefix):
        try:
            module = importlib.import_module(modname)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, BaseModel) and obj != BaseModel:
                    # Only include models defined in this module to avoid duplicates
                    if obj.__module__ == modname:
                        models[f"{modname}.{name}"] = obj
        except Exception:
            continue
    return models

def generate_schema_snapshot(models):
    snapshot = {}
    for name, model in models.items():
        try:
            snapshot[name] = model.model_json_schema()
        except Exception as e:
            print(f"Failed to generate schema for {name}: {e}")
    return snapshot

def check_schemas():
    print("Checking Pydantic Schema compatibility...")
    models = get_all_models("core.contracts")
    current_snapshot = generate_schema_snapshot(models)
    
    snapshot_file = Path("tests/snapshot/contracts_schema.json")
    if not snapshot_file.exists():
        print("Snapshot file does not exist. Creating new snapshot...")
        snapshot_file.parent.mkdir(parents=True, exist_ok=True)
        with open(snapshot_file, "w") as f:
            json.dump(current_snapshot, f, indent=2)
        print("Snapshot created.")
        return 0
        
    with open(snapshot_file, "r") as f:
        baseline = json.load(f)
        
    breaking_changes = 0
    for name, schema in current_snapshot.items():
        if name not in baseline:
            print(f"INFO: New model added: {name}")
            continue
            
        # Simplified check: strictly matching schema
        if json.dumps(schema, sort_keys=True) != json.dumps(baseline[name], sort_keys=True):
            print(f"ERROR: Schema changed for {name}")
            # A real tool would do deep diff and allow additive changes
            breaking_changes += 1
            
    if breaking_changes > 0:
        print(f"Found {breaking_changes} breaking schema changes!")
        return 1
        
    print("No breaking schema changes detected.")
    return 0

if __name__ == "__main__":
    sys.exit(check_schemas())
