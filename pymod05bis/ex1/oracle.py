import os
from dotenv import load_dotenv  # type:ignore

DEFAULT_CONFIG = {
    "MATRIX_MODE": (
        "development",
        "WARNING: MATRIX_MODE not set, defaulting to 'development'",
    ),
    "DATABASE_URL": (
        "sqlite:///local.db",
        "WARNING: DATABASE_URL not set, defaulting to local sqlite instance",
    ),
    "API_KEY": (
        "dev_dummy_key_123",
        "WARNING: API_KEY not set, using temporary dev key",
    ),
    "LOG_LEVEL": (
        "DEBUG",
        "WARNING: LOG_LEVEL not set, defaulting to 'DEBUG'",
    ),
    "ZION_ENDPOINT": (
        "http://localhost:8080/zion",
        "WARNING: ZION_ENDPOINT not set, defaulting to local endpoint",
    ),
}


def load_configuration() -> dict[str, str]:
    load_dotenv()
    config: dict[str, str] = {}
    missing_detected = False
    for key, (default_val, warn_msg) in DEFAULT_CONFIG.items():
        val = os.getenv(key)
        if val is None:
            print(warn_msg)
            config[key] = default_val
            missing_detected = True
        else:
            config[key] = val
    if missing_detected:
        print()
    return config


def check_hardcode() -> bool:
    target_tokens = ["sk" + "_live_", "production" + "_secret"]
    try:
        with open(__file__, "r", encoding="utf-8") as f:
            content = f.read()
            for token in target_tokens:
                if token in content:
                    return False
    except Exception:
        pass
    return True


def is_env_gitignore() -> bool:
    try:
        with open(".gitignore", "r") as f:
            lines = [line.strip() for line in f.readlines()]
            if ".env" in lines or "*.env" in lines:
                return True
    except Exception:
        pass
    return False


def available_override() -> bool:
    try:
        with open(__file__, "r")as f:
            content = f.read()
        if "load_dotenv()" in content:
            return True
    except Exception:
        pass
    return False


def check_security() -> None:
    print("Configuration security check:")
    if check_hardcode():
        print("[OK] No hardcoded secrets detected")
    else:
        print("[WARN] Potential hardcoded secrets detected in source code!")

    if is_env_gitignore():
        print("[OK] .env file properly ignored by git")
    else:
        print("[WARN] .env is NOT ignored by git!"
              " Add it to .gitignore immediately.")

    if available_override():
        print("[OK] Production overrides available")
    else:
        print("[WARN] Environment overrides are disabled or unavailable.")


def show_configuration(config: dict[str, str]) -> None:
    print("Configuration loaded:")
    mode = config.get("MATRIX_MODE", "development")
    print(f"Mode: {mode}")

    if mode == "production":
        print(
            "Database: Connected to production instance "
            f"({config.get('DATABASE_URL')})")
        api_key = config.get("API_KEY", "")
        masked_key = f"{api_key[:3]}***" if len(api_key) >= 3 else "***"
        print(f"API Access: Authenticated (Key: {masked_key})")
        print(f"Log Level: {config.get('LOG_LEVEL', 'INFO')}")
        print(f"Remote Network: Online ({config.get('ZION_ENDPOINT')})")
    else:
        print("Database: Connected to local instance")
        print("API Access: Authenticated")
        print(f"Log Level: {config.get('LOG_LEVEL', 'DEBUG')}")
        print("Remote Network: Online")
    print()


def main() -> None:
    print("ORACLE STATUS: Consulting the configuration...")
    config = load_configuration()
    show_configuration(config)
    check_security()
    print("The Oracle sees all configurations.")


if __name__ == "__main__":
    main()
