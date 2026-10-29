import alchemy


def main() -> None:
    print("=== Alembic 1 ===")
    print("Accessing the alchemy module using 'import alchemy'")
    print(f"Testing create_air: {alchemy.create_air()}")
    print("Now show that not all functions can be reached")
    print("This will raise an exception!")
    try:
        print(f"Testing the hidden create_earth: {alchemy.create_earth()}")
    except AttributeError as e:
        print(f"Testing the hidden create_earth: Caught exception -> {e}")


if __name__ == "__main__":
    main()
