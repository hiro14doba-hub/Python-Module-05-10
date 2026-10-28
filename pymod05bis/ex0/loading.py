import importlib


def import_check() -> bool:
    reagents = {
        "pandas": "Data manipulation ready",
        "numpy": "Numerical computation ready",
    }
    missing = []

    for name, desc in reagents.items():
        try:
            mod = importlib.import_module(name)
            version = getattr(mod, "__version__", "unknown")
            print(f"[OK] {name} ({version})")
            print(f"  {desc}")
        except ImportError:
            print(f"[FAIL] {name} is missing!")
            missing.append(name)
    return len(missing) == 0


def show_pip_vs_poetry() -> None:
    print("requirements.txt declares what to install;"
          " pip resolves it at install time.\n"
          "pyproject.toml declares the same constraints,"
          " and Poetry pins the resolved versions in poetry."
          "lock so every install is identical."
          )


def show_success() -> None:
    print("All reagents present and accounted for.")


def show_install_guide() -> None:
    print("\nMissing reagents detected! To install them:")
    print("Using pip:")
    print("  pip install -r requirements.txt")
    print("Using Poetry:")
    print("  poetry install")


def main() -> None:
    is_all_install = import_check()
    show_pip_vs_poetry()
    if is_all_install:
        show_success()
    else:
        show_install_guide()


if __name__ == "__main__":
    main()
