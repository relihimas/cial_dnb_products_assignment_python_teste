# Use Ubuntu latest as the base image
FROM ubuntu:latest

# Update the package list and install dependencies
RUN apt-get update && \
    apt-get install -y \
    software-properties-common \
    wget \
    curl \
    git \
    lsb-release \
    gnupg

RUN apt-get install -y python3.10 python3-pip python3-flask 
RUN pip install flask_caching requests playwright psycopg2-binary pyquery --break-system-packages

# PostgreSQL
RUN apt-get install -y postgresql postgresql-contrib postgresql-client

# Clone the GitHub repository
RUN git clone https://github.com/relihimas/cial_dnb_products_assignment_python_teste.git /app

EXPOSE 8000

CMD nohup python3 ./app/app/stock_server.py