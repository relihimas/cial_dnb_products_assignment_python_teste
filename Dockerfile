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

RUN apt-get install -y python3.10 python3-pip python3-flask playwright

RUN pip install flask_caching requests playwright psycopg2-binary --break-system-packages

# PostgreSQL
RUN apt-get install -y postgresql postgresql-contrib

# Clone the GitHub repository
RUN git clone https://github.com/relihimas/cial_dnb_products_assignment_python_teste.git /app
  
# Expose the PostgreSQL port
EXPOSE 8000

CMD ["/app/app/init_db.sh", "&&", "nohup", "python3", "/app/app/stock_server.py"]