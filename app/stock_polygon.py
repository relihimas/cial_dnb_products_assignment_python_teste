import requests
from datetime import datetime, timedelta
from stock_log import definelog
import constants as cnt

logger = definelog()

def verificar_fim_de_semana(data):
    
    logger.info("Verifying if date is a weekday.")

    try:

        data_obj = datetime.strptime(data, "%Y-%m-%d")

        if data_obj.weekday() == 5:
            
            data_obj = data_obj - timedelta(days=1)

            return data_obj
            
        if data_obj.weekday() == 6:

            data_obj = data_obj - timedelta(days=2)

            return data_obj

            erro = 'Informed date is Saturday or Sunday'
            logger.error(erro)
            raise Exception(erro)
        else:
            logger.info("Informed date is between Monday and Friday")
            return True

    except Exception as e:
        logger.error(e)
        return e

def formatador_data(data):
    
    logger.info("Formatting date")
    
    try:
    
        data_formatada = datetime.strptime(data, "%Y-%m-%d").strftime("%Y-%m-%d")
    
    except ValueError:
    
        formatos_possiveis = ["%d/%m/%Y", "%d-%m-%Y", "%m/%d/%Y", "%m-%d-%Y", "%Y/%m/%d"]
    
        for formato in formatos_possiveis:
            try:
                data_formatada = datetime.strptime(data, formato).strftime("%Y-%m-%d")
                break
            except ValueError:
                continue
        else:
            erro = f"Invalid format date: {data}"
            logger.error(erro)
            raise ValueError(erro)
    
    logger.info("Date formatted with success")

    return data_formatada

def polygon(stock):

    logger.info("Polygon data extraction")

    try:
        
        stock = stock.upper()

        hoje = datetime.now()
        ontem = hoje - timedelta(days=1)
        data_uso = ontem.strftime('%Y-%m-%d')
        ajuste_data = formatador_data(data_uso)
        verificar_fim_de_semana(ajuste_data)

        url_polygon = f"https://api.polygon.io/v1/open-close/{stock}/{ajuste_data}"

        payload_polygon = {}
        headers_polygon = {
        'Authorization': f'Bearer {cnt.key_polygon}'
        }

        response = requests.get(url_polygon, headers=headers_polygon, data=payload_polygon)

        if response.status_code != 200:
            erro = f"Error on the data extraction from Polygon - {response.status_code} - {response.text}'"
            logger.error(erro)
            raise Exception(erro)
        
        return True, response.json()

    except Exception as e:
        logger.error(e)
        return False, e