import logging
from pathlib import Path
from datetime import datetime

def setup_logger(config) -> logging.Logger:
    log_dir = config["logging"]["log_dir"]
    Path(log_dir).mkdir(parents = True, exist_ok = True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = Path(log_dir) / f"ingestion_{timestamp}.log"

    logger = logging.getLogger("ingestion")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    fh = logging.FileHandler(log_path, encoding = "utf-8")
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info(f"Logging to: {log_path}")

    return logger