from playwright.sync_api import sync_playwright
import time
from stock_log import definelog

logger = definelog()

def stock_martketwatch(stock):

    try:

        logger.info(f"Starting WebScraping on MarketWatch for stock {stock}")

        stock = stock.lower()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            page.goto("https://www.marketwatch.com/investing/stock/aapl")

            time.sleep(20)

            company_name = page.query_selector('h1.company__name').inner_text()
            competitors_element = page.query_selector('div.element.element--table.overflow--table').inner_text()
            group_element = page.query_selector('div.group.group--elements.right').inner_text()

            print(company_name)
            print(competitors_element)
            print(group_element)

            market_watch_data = {
                "performance_data": {
                        "five_days": float(group_element),
                        "one_month": float(group_element),
                        "three_months": float(group_element),
                        "year_to_date": float(group_element),
                        "one_year": float(group_element)
                    },
                    "competitors": [
                        {
                            "name": "Competitor",
                            "market_cap": {
                                "Currency": "USD",
                                "Value": 2500.56
                            }
                        }
                    ]
            }
            browser.close()

        logger.info(f"Finished WebScraping on MarketWatch for stock {stock}")
        
        return market_watch_data
        
    except Exception as e:
        erro = f'Error during data extraction from MarketWatch - {e}'
        logger.error(erro)
        return erro