"""
Entry point for the data ingestion pipeline.

This script is responsible for:
- Triggering ingestion logic
- Keeping execution separate from implementation details

All dataset-specifc logic lives in the ingestion package.
"""

# Import the function from ingestion/read_results
from ingestion.read_results import run_results_ingestion

def main():
    """
    Main execution function for running ingestion tasks.

    Additional ingestion steps (e.g., drivers, races) can be added later if we want
    """
    run_results_ingestion()

if __name__ == "__main__":
    main()