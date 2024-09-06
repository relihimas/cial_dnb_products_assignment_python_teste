import psycopg2
from psycopg2 import sql
import constants as cnt
from stock_log import definelog
from datetime import datetime

logger = definelog()

def database_connection():
    
    try:
        conn = psycopg2.connect(
            dbname=cnt.dbname,
            user= cnt.user,
            password= cnt.password,
            host= cnt.host,
            port= cnt.port
        )

        cur = conn.cursor()

        return cur, conn

    except Exception as e:
        logger.error(e)
        return e

def create_stock():

    try:

        cur, conn = database_connection()

        logger.info("Creating Stock table")
        
        create_query = sql.SQL(cnt.create_query)
        cur.execute(create_query)
        cur.commit()

        cur.close()
        conn.close()
    
    except Exception as e:
        return None


def check_stock(stock):

    try:

        cur, conn = database_connection()

        logger.info("Verifying if Stock already exists on the database")
        
        select_query = sql.SQL(cnt.select_query)
        cur.execute(select_query, (stock,))
        result = cur.fetchone()

        if result == None:
            logger.info("Stock not presented in stock table")
            cur.close()
            conn.close()
            return None
        else:
            logger.info("Verification complete")
            cur.close()
            conn.close()

            return result
    
    except Exception as e:
        return None

def insert_amount(stock, amount):
    
    try: 

        cur, conn = database_connection()

        logger.info("Inserting data into Postgres Database")

        agora = datetime.now()
        data_hora_formatada = agora.strftime('%Y-%m-%d %H:%M:%S')

        insert_query = cnt.insert_query

        cur.execute(insert_query, (stock, amount, data_hora_formatada))
        conn.commit()

        logger.info("Data inserted to Postgres Database successfully")

        cur.close()
        conn.close()

        return True, amount
    
    except Exception as e:
        return False, e

def update_amount(stock, amount):
    
    try:

        cur, conn = database_connection()

        logger.info("Inserting data into Postgres Database")
      
        update_query = cnt.update_query

        cur.execute(update_query, (amount, stock))
        conn.commit()

        logger.info(f"Stock {stock} updated successfully with new amount {amount}")

        cur.close()
        conn.close()

        return True, amount
    
    except Exception as e:
        return False, e


def database_operation(stock, amount):
    
    try:

        logger.info("Connection to Postgres Database successful")

        stock = stock.upper()

        check_tabela = create_stock()

        valor = check_stock(stock)

        if  valor == None:
            insert_amount(stock, amount)
            logger.info("Data inserted to Postgres Database successfully")
            return True, amount

        else:
            amount_update = valor + amount
            update_amount(stock, amount_update)
            logger.info("Data updated to Postgres Database successfully")
            return True, amount_update

    except Exception as e:
        return e
