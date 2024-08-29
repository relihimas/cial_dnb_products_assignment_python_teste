key_polygon='bmN7i7CrzrpKqFvgbB1fEaztCwZKSUjJ'
dbname='stock_db'
user='stock_user'
password='password'
host='localhost'
port='5432'
insert_query="""INSERT INTO stock (stock, amount, created_on, updated_at) VALUES (%s, %s, %s, NOW() AT TIME ZONE 'America/Sao_Paulo')"""
update_query="""UPDATE stock SET amount = %s, updated_at = NOW() AT TIME ZONE 'America/Sao_Paulo' WHERE stock = %s"""
select_query="""SELECT amount FROM stock WHERE stock = %s""" 
port_server=8000