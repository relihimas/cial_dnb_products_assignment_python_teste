# cial_dnb_products_assignment_python_teste

# Stocks REST API
This project is a Python-based REST API for retrieving and managing stock data. The API fetches stock information from external sources such as the Polygon.io API and scrapes data from MarketWatch. The application is designed to be efficient, utilizing caching and a PostgreSQL database for persistence.

# Features
- Retrieve Stock Data: Fetch detailed stock data including open, high, low, close prices, performance metrics, and competitor information.
- Update Stock: Update the purchased amount of a stock.
- Data Caching: Implement caching to reduce redundant API calls.
- Data Persistence: Store stock data and purchased amounts in a PostgreSQL database.
- Logging: Comprehensive logging for tracking API requests and errors.
- Docker Support: Easily deployable using Docker.

# Walktrough

First, start the application by building the image:

    docker build -t stock-api .

And then, run it:

    docker run -p 8000:8000 stock-api



## API Endpoints

### [GET] /stock/{stock_symbol}
  Returns the stock data for the given symbol.

  - curl example:

        curl --location 'http://127.0.0.1:8000/stock/aapl' \
        --data ''
    
### [POST] /stock/{stock_symbol}
  Update the stock entity with the purchased amount based on received argument: “amount” (of type Integer).

  - curl example

        curl --location 'http://127.0.0.1:5000/stock/aapl' \
        --header 'Content-Type: application/json' \
        --data '{"amount": 10}'

