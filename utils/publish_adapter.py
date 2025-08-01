import shutil
from pathlib import Path

SOURCE_ADAPTER_DIR = Path("llm/adapters/aiko-core")
VAULT_ADAPTER_DIR = Path("vault/adapters/aiko-core")

def publish_adapter():
    if not SOURCE_ADAPTER_DIR.exists():
        raise FileNotFoundError(f"No adapter found at {SOURCE_ADAPTER_DIR}")

    if VAULT_ADAPTER_DIR.exists():
        print(f"Cleaning existing adapter at {VAULT_ADAPTER_DIR}")
        shutil.rmtree(VAULT_ADAPTER_DIR)

    shutil.copytree(SOURCE_ADAPTER_DIR, VAULT_ADAPTER_DIR)
    print(f"Published adapter to {VAULT_ADAPTER_DIR}")

if __name__ == "__main__":
    publish_adapter()