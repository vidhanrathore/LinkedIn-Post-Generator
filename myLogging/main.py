# main.py
from logger_config import setup_logger

logger = setup_logger(__name__)

def main():
    logger.info("Starting the application...")
    logger.debug("This is a debug message")
    logger.warning("This is a warning")
    logger.error("This is an error")
    logger.critical("Critical issue!")
    import time

    print("Program starts.")
    logger.info("Program Started.")
    time.sleep(3)  # Pause for 3 seconds
    print("Program resumes after 3 seconds.")
    logger.info("Program End.")
    

if __name__ == "__main__":
    main()
