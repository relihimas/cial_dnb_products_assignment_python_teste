import psycopg2
from psycopg2 import sql
import constants as cnt
from stock_log import definelog
from datetime import datetime

logger = definelog()

def check_stock(cur, conn, stock):

    try:
        logger.info("Verifying if Stock already exists on the database")
        with conn.cursor() as cur:
                    
            select_query = sql.SQL(cnt.select_query)
            cur.execute(select_query, (stock,))
            result = float(cur.fetchone()[0])

        logger.info("Verification complete")
        return result
    
    except Exception as e:
        return None

def insert_amount(cur, conn, stock, amount):
    
    try: 
        logger.info("Inserting data into Postgres Database")

        agora = datetime.now()
        data_hora_formatada = agora.strftime('%Y-%m-%d %H:%M:%S')

        insert_query = cnt.insert_query

        cur.execute(insert_query, (stock, amount, data_hora_formatada))

        # Commit das mudanças
        conn.commit()

        logger.info("Data inserted to Postgres Database successfully")

        return True, amount
    
    except Exception as e:
        return False, e

def update_amount(cur, conn, stock, amount):
    
    try: 
        logger.info("Inserting data into Postgres Database")

        agora = datetime.now()
        data_hora_formatada = agora.strftime('%Y-%m-%d %H:%M:%S')

        update_query = cnt.update_query

        cur.execute(update_query, (amount, stock))
        
        conn.commit()
        logger.info(f"Stock {stock} updated successfully with new amount {amount}")

        return True, amount
    
    except Exception as e:
        return False, e


def database_operation(stock, amount):
    
    try:
        conn = psycopg2.connect(
            dbname=cnt.dbname,
            user= cnt.user,
            password= cnt.password,
            host= cnt.host,
            port= cnt.port
        )

        cur = conn.cursor()

        logger.info("Connection to Postgres Database successful")

        stock = stock.upper()

        valor = check_stock(cur, conn, stock)

        if  valor == None:
            insert_amount(cur, conn, stock, amount)
            cur.close()
            conn.close()
            logger.info("Data inserted to Postgres Database successfully")
            return True, amount

        else:
            amount_update = valor + amount
            update_amount(cur, conn, stock, amount_update)
            cur.close()
            conn.close()
            logger.info("Data updated to Postgres Database successfully")
            return True, amount_update

    except Exception as e:
        return e
    