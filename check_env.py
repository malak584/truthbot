import sys

def check_import(module_name):
    try:
        module = __import__(module_name)
        print(f"[OK] {module_name} version: {module.__version__}")
    except ImportError as e:
        print(f"[FAIL] {module_name} not found: {e}")
    except AttributeError:
        print(f"[OK] {module_name} installed (no __version__ attribute)")

def main():
    print(f"Python version: {sys.version}")
    print("-" * 20)
    
    libraries = [
        "numpy",
        "pandas",
        "sklearn",
        "matplotlib",
        "torch"
    ]
    
    for lib in libraries:
        check_import(lib)

if __name__ == "__main__":
    main()
