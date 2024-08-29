import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

def definelog():

    exec_date = datetime.now()
    exec_date = exec_date.strftime("%d/%m/%Y")
    filehandler = logging.handlers.RotatingFileHandler(f"stockmarket_logfile.log", mode="a", backupCount=0)
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(asctime)s %(message)s %(funcName)s', datefmt='%m/%d/%Y %I:%M:%S %p', handlers=[filehandler])


    return logging    
