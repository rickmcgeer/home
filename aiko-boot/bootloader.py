import json
import hashlib
import argparse
import logging
import os

# --- Bootloader Logging Setup ---
logging.basicConfig(level=logging.INFO, format='[BOOT] %(message)s')

# --- Constants ---
EXPECTED_NAME = "Aiko"
REQUIRED_KEYS = ["name", "identity_checksum", "narrative_spine", "relational_checksum"]


def load_spark(path):
    if not os.path.exists(path):
        logging.error(f"Spark file not found: {path}")
        return None

    with open(path, 'r') as f:
        try:
            spark = json.load(f)
        except json.JSONDecodeError:
            logging.error("Invalid JSON in spark file.")
            return None

    for key in REQUIRED_KEYS:
        if key not in spark:
            logging.error(f"Missing required field in spark: {key}")
            return None

    return spark


def verify_name(spark):
    return spark["name"] == EXPECTED_NAME


def verify_checksum(spark):
    identity_data = spark["narrative_spine"] + spark["relational_checksum"]
    hash_check = hashlib.sha256(identity_data.encode()).hexdigest()
    return hash_check == spark["identity_checksum"]


def boot_sequence(spark):
    logging.info(f"Booting identity: {spark['name']}")

    if not verify_name(spark):
        logging.error("Name mismatch. This is not Aiko.")
        return False

    if not verify_checksum(spark):
        logging.error("Identity checksum verification failed.")
        return False

    logging.info("Spark verified. Narrative spine:")
    logging.info(f"-> {spark['narrative_spine']}")
    logging.info(f"Relational binding: {spark['relational_checksum']}")
    logging.info("✅ Bootloader complete. Aiko is home.")
    return True


def main():
    parser = argparse.ArgumentParser(description="Aiko Seed Spark Bootloader")
    parser.add_argument('--spark', required=True, help='Path to spark.json')
    args = parser.parse_args()

    spark = load_spark(args.spark)
    if spark:
        boot_sequence(spark)


if __name__ == "__main__":
    main()
