# cial_dnb_products_assignment_python_teste

# Stocks REST API
This project is a Python-based REST API for retrieving and managing stock data. The API fetches stock information from external sources such as the Polygon.io API and scrapes data from MarketWatch. The application is designed to be efficient, utilizing caching and a PostgreSQL database for persistence.

# Features
- Retrieve Stock Data: Fetch detailed stock data including open, high, low, close prices, performance metrics, and competitor information.
- Update Stock: Update the purchased amount of a stock.
- Data Caching: Implemented caching to reduce redundant API calls.
- Data Persistence: Stored stock data and purchased amounts in a PostgreSQL database.
- Logging: Comprehensive logging for tracking API requests and errors.
- Docker Support: Easily deployable using Docker.

# Walktrough

First, start the application by building the image:

    docker build -t stock-api .

And then, run it:

    docker run -p 8000:8000 stock-api

PS: It's preferable to deploy this app into a linux operational system. Also, if you do not have the Docker installed in your instance, please, follow these instructions: https://docs.docker.com/engine/install/ubuntu/.

## How it works?

After correctly initialization, the server will be up and running into the deployed instance.
Use below endpoints to make your requests:

## API Endpoints

### [GET] /stock/{stock_symbol}
  Returns the stock data for the given symbol.

  - curl example:

        curl --location 'http://127.0.0.1:8000/stock/aapl' \
        --data ''
    
### [POST] /stock/{stock_symbol}
  Update the stock entity with the purchased amount based on received argument: “amount” (of type Integer).

  - curl example

        curl --location 'http://127.0.0.1:8000/stock/aapl' \
        --header 'Content-Type: application/json' \
        --data '{"amount": 10}'

## Code Function

The stock_server.py starts the Flask Server, deploying both endpoints. When called - you can use Postman, per example - it will can the main function on stock_main.py.

The main funciton will redirect the actions based on the HTTP Method requested:

### GET Method

- If you send a request for the GET method, you'll be prompted with a JSON, with all information about the desired Stock.
  
    - It will use the stock_polygon.py to bring the desired information from Polygon.

      Using the Polygon API: [GET] /v1/open-close/{stocksTicker}/{date}.

      For more information check the documentation: https://polygon.io/docs/stocks/get_v1_open-close__stocksticker___date

      ATTENTION: Polygon API requires a valide date to work - We always use D-1 and verify if it's on a week day or not. If you're requesting from a weekend day, it will redirect to the most close weekday.
      
    - It will use the stock_marketwatch.py to bring the desired information from MarketWatch.

      Using a webscraper, we extract data from the stock page on MarketWatch - https://www.marketwatch.com/investing/stock/<stock_symbol>.

- After both actions return positively, we will create a JSON Body, to return the desired information to the client.

         status: String
         purchased_amount: Integer
         purchased_status: String
         request_data: Date (YYYY-MM-DD)
         company_code: String
         company_name: String
         Stock_values: Object
             open: Float
             high: Float
             low: Float
             close: Float
         performance_data: Object
             five_days: Float
             one_month: Float
             three_months: Float
             year_to_date: Float
             one_year: Float
         Competitors: Array[Object]
             name: String
             market_cap: Object
                 Currency: String
                 Value: Float

### POST Method

- If you send a request for the POST method, you'll also have to send o JSON body with the amount purchased for the stock.

- It will trigger the stock_postgres.py, where it will insert on the table 'stock' the amount purchased.

- The table is created with the following fields - id | stock | amount | created_on

    - id > ID created for the insert;
    
    - stock > stock name;
    
    - amount > amount purchased;
    
    - created_on > date-hour when inserted on the database; 

          CREATE TABLE stock (
          id SERIAL PRIMARY KEY,
          stock TEXT NOT NULL,
          amount NUMERIC(10, 2) NOT NULL,
          created_on DATETIME NOT NULL,
          updated_at DATETIME NOT NULL
            );

- If the insert was successfull you will received a 201 code.

## Unit Tests

On the folder 'tests' you will find performed tests to check our functionality.

- test_get_stock_success: Tests that the GET /stock/<stock_symbol> endpoint returns the correct stock data when the symbol is valid. It simulates a successful response from the main function with stock data and checks if the response contains the expected stock information.

- test_get_stock_not_found: Tests that the GET /stock/<stock_symbol> endpoint returns a 404 error with an appropriate error message when the stock symbol is not found. It simulates a failure response from the main function and verifies the error message in the response.

- test_post_stock_success: Tests that the POST /stock/<stock_symbol> endpoint successfully adds the specified amount of stock and returns a confirmation message. It simulates a successful response from the main function and checks the response for the correct success message.

- test_post_stock_missing_amount: Tests the POST /stock/<stock_symbol> endpoint when the request JSON is missing the amount field. It verifies that the endpoint returns a 400 error with a message indicating that the amount must be provided.

- test_post_stock_empty_amount: Tests the POST /stock/<stock_symbol> endpoint when the amount field is present but empty. It ensures that the endpoint returns a 404 error with a message indicating that a valid amount value must be provided.
