from stock_polygon import polygon
from stock_marketwatch import stock_martketwatch
from stock_postgres import database_operation
from stock_log import definelog
from datetime import datetime
import re

logger = definelog()

def valida_stock(stock):
    pattern = r'^[A-Z]{1,5}$'
    return bool(re.match(pattern, stock))

def get(stock):

    try:
        
        logger.info("Starting GET method")

        dados_polygon = polygon(stock)

        if not dados_polygon[0]:
            raise Exception(dados_polygon[1])

        # dados_marketwatch = stock_martketwatch(stock)

        # if not dados_marketwatch:
        #     raise Exception(dados_marketwatch)

        dados_marketwatch = "TESTE"

        stock = {
            "status": str(dados_polygon[1]['status']),
            "purchased_amount": 0,
            "purchased_status": "completed",
            "request_data": datetime.strptime(dados_polygon[1]['from'], "%Y-%m-%d").strftime('%Y-%m-%d'), 
            "company_code": str(dados_polygon[1]['symbol']),
            "company_name": dados_marketwatch,
            "stock_values": {
                "open": float(dados_polygon[1]['open']),
                "high": float(dados_polygon[1]['high']),
                "low": float(dados_polygon[1]['low']),
                "close": float(dados_polygon[1]['close']),
            }
            ,
            "performance_data": {
                "five_days": float(1.00),
                "one_month": float(1.00),
                "three_months": float(1.00),
                "year_to_date": float(1.00),
                "one_year": float(1.00)
            },
            "competitors": [
                dados_marketwatch
            ]
        }

        logger.info("Finishing GET method and returning data")

        return True, stock
    
    except Exception as e:
        logger.error(e)
        return False, e

def post(stock, amount):
    
    try:
        logger.info("Starting POST method")

        register = database_operation(stock, amount)

        if not register[0]:
            raise Exception(register[1])
        
        logger.info("Starting POST method and returning data")
        return True, amount

    except Exception as e:
        logger.error(e)
        return e

def main(method, stock, amount):

    try:

        stock = stock.upper()

        validacao = valida_stock(stock)
        if not validacao:
            raise Exception("Stock name is not valid.")
    
        logger.info('Starting main function')
        if method == 'get':
           logger.info('Get process')
           get_process = get(stock)
           if not get_process[0]:
               raise Exception(get_process[1])
           else:
               logger.info('Finishing Get process')
               return True, get_process[1]

        elif method == 'post':
            logger.info('Post process')
            post_process = post(stock, amount)
            if not post_process[0]:
                raise Exception(post_process[1])
            else:
                logger.info('Finishing Post process')
                return True, post_process[1]

    except Exception as e:
        logger.error(e)
        return False, e
