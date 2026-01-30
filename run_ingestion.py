"""
Entry point for the data ingestion pipeline.

This script is responsible for:
- Triggering ingestion logic
- Keeping execution separate from implementation details

All dataset-specifc logic lives in the ingestion package.
"""

from ingestion.read_results import run_results_ingestion
from ingestion.loader import load_config
from ingestion.logging_utils import setup_logger



def main():
    """
    Main execution function for running ingestion tasks.

    Additional ingestion steps (e.g., drivers, races) can be added later if we want
    """
    config = load_config()
    logger = setup_logger(config)

    logger.info("Ingestion run started")

    try:
        run_results_ingestion()
        logger.info("Ingestion run finished successfully")
    except Exception as e:
        logger.exception(f"Ingestion run failed: {e}")
        raise

if __name__ == "__main__":
    main()