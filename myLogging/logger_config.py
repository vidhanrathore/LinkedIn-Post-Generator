import logging

def setup_logger(name: str):
    logger = logging.getLogger(name)

    if logger.hasHandlers():
        logger.handlers.clear()  # Prevent duplicate logs if re-imported

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File handler
    fh = logging.FileHandler('app.log', mode='a')  # or mode='w' if you prefer overwriting each run
    fh.setFormatter(formatter) 
    
    logger.addHandler(fh)

    return logger

if __name__ == "__main__":
    logger = setup_logger(__name__)
    logger.info("Starting the Logger.config File...")
