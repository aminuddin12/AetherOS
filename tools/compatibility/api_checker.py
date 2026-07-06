import sys
import importlib
import pkgutil
import inspect
from pathlib import Path
import json

def get_public_classes(package_name):
    classes = {}
    try:
        package = importlib.import_module(package_name)
    except ImportError:
        return classes
        
    prefix = package.__name__ + "."
    for _, modname, ispkg in pkgutil.walk_packages(package.__path__, prefix):
        try:
            module = importlib.import_module(modname)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and obj.__module__ == modname:
                    if not name.startswith("_"):
                        classes[f"{modname}.{name}"] = obj
        except Exception:
            continue
    return classes

def get_method_signatures(cls):
    sigs = {}
    for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        if not name.startswith("_") or name == "__init__":
            try:
                sig = inspect.signature(method)
                sigs[name] = str(sig)
            except ValueError:
                pass
    return sigs

def check_api():
    print("Checking Public API compatibility (Method Signatures)...")
    
    current_api = {}
    for pkg in ["core.kernel", "core.execution"]:
        classes = get_public_classes(pkg)
        for cls_name, cls_obj in classes.items():
            current_api[cls_name] = get_method_signatures(cls_obj)
            
    snapshot_file = Path("tests/snapshot/public_api_snapshot.json")
    if not snapshot_file.exists():
        print("Snapshot file does not exist. Creating new API snapshot...")
        snapshot_file.parent.mkdir(parents=True, exist_ok=True)
        with open(snapshot_file, "w") as f:
            json.dump(current_api, f, indent=2)
        print("API Snapshot created.")
        return 0
        
    with open(snapshot_file, "r") as f:
        baseline = json.load(f)
        
    breaking_changes = 0
    for cls_name, sigs in baseline.items():
        if cls_name not in current_api:
            print(f"ERROR: Class removed: {cls_name}")
            breaking_changes += 1
            continue
            
        current_sigs = current_api[cls_name]
        for method_name, old_sig in sigs.items():
            if method_name not in current_sigs:
                print(f"ERROR: Method removed: {cls_name}.{method_name}")
                breaking_changes += 1
                continue
                
            new_sig = current_sigs[method_name]
            if old_sig != new_sig:
                print(f"ERROR: Signature changed for {cls_name}.{method_name}")
                print(f"  Old: {old_sig}")
                print(f"  New: {new_sig}")
                breaking_changes += 1
                
    if breaking_changes > 0:
        print(f"Found {breaking_changes} breaking API changes!")
        return 1
        
    print("No breaking API changes detected.")
    return 0

if __name__ == "__main__":
    sys.exit(check_api())
