# Use Ubuntu latest as the base image
FROM ubuntu:latest

COPY init.sql /docker-entrypoint-initdb.d/

# Update the package list and install dependencies
RUN apt-get update && \
    apt-get install -y \
    software-properties-common \
    wget \
    curl \
    git \
    lsb-release \
    gnupg

# Python 3.11
RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.11 python3.11-venv python3.11-dev

# PostgreSQL
RUN apt-get install -y postgresql postgresql-contrib

# Clone the GitHub repository
RUN git clone https://github.com/relihimas/cial_dnb_products_assignment_python_teste /app

# Set up the PostgreSQL service
RUN service postgresql start
    
# Expose the PostgreSQL port
EXPOSE 8000

# Set the working directory
WORKDIR /app

# Start PostgreSQL when the container starts
CMD ["nohup","python3","stock_server.py"]