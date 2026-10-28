import sys
import os
import site


def is_sealed() -> bool:
    return sys.prefix != sys.base_prefix


def show_sealed_lab() -> None:
    print("LABORATORY STATUS: The laboratory is sealed")
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {os.path.basename(sys.prefix)}")
    print(f"Environment Path: {sys.prefix}")
    print("SUCCESS: You are working in an isolated environment!")
    print("Safe to install reagents without affecting")
    print("the global system.")
    print("Reagent installation path:")
    package = site.getsitepackages()
    installation_path = package[0] if package else "unknown"
    print(installation_path)


def show_open_lab() -> None:
    print("LABORATORY STATUS: You are working in the open")
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print("WARNING: You are in the global environment!")
    print("Every reagent you install here leaks into the whole system.")
    print("To seal the laboratory, run:")
    print("python3 -m venv lab_env")
    print("source lab_env/bin/activate # On Unix")
    print("lab_env\\Scripts\\activate # On Windows")
    print("Then run this program again.")


def main() -> None:
    if is_sealed():
        show_sealed_lab()
    else:
        show_open_lab()


if __name__ == "__main__":
    main()
