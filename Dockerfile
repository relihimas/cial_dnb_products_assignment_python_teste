# Usar a imagem base oficial do Python 3.10
FROM python:3.10-slim

# Instalar Git e PostgreSQL
RUN apt-get update && apt-get install -y \
    git \
    postgresql \
    postgresql-contrib

# Definir o diretório de trabalho
WORKDIR /app

# Clonar o repositório do GitHub
RUN git clone https://github.com/relihimas/cial_dnb_products_assignment_python_teste .

# Instalar as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Configurar PostgreSQL
RUN service postgresql start && \
    sudo -u postgres psql -c "CREATE DATABASE stock_db;" && \
    sudo -u postgres psql -c "CREATE USER stock_user WITH ENCRYPTED PASSWORD 'password';" && \
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE stock_db TO stock_user;" && \
    sudo -u postgres psql -c "CREATE TABLE stock (id SERIAL PRIMARY KEY, stock TEXT NOT NULL, amount INTEGER NOT NULL, created_on DATE NOT NULL);"

# Expor a porta que a aplicação Flask irá usar
EXPOSE 8000

# Definir o comando padrão para executar a aplicação
CMD ["nohup","postgresql","start","&&", "python3", "stock_server.py"]
