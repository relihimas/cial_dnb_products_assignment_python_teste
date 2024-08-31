import requests
from pyquery import PyQuery as pq
from stock_log import definelog

requests.packages.urllib3.disable_warnings()
logger = definelog()

def stock_martketwatch(stock):

    try:
        competitors = []

        logger.info(f"Starting WebScraping on MarketWatch for stock {stock}")

        session = requests.session()

        stock = stock.lower()

        url = f"https://www.marketwatch.com/investing/stock/{stock}?mod=side_nav"

        header = {"Sec-Ch-Ua": "\"Chromium\";v=\"121\", \"Not A(Brand\";v=\"99\"", 
                "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Linux\"", "Upgrade-Insecure-Requests": "1", 
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.160 Safari/537.36", 
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 
                "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", 
                "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate, br", 
                "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8", "Priority": "u=0, i"}

        resp = session.get(url, headers=header, verify=False)
        resp = pq(resp.text)

        company_name = resp('h1.company__name').text()

        comp_name = []
        comp_mkt = []
        comp_currency = []

        for name in resp('.table__cell.w50 a'):
            comp_name.append(name.text)

        for mktcap in resp('.table__cell.number'):
            mktcap = mktcap.text
            comp_mkt.append(mktcap)
            if str(mktcap).startswith('$'):
                currency = 'USD'
            elif str(mktcap).startswith('₩'):
                currency = 'KRW'
            elif str(mktcap).startswith('¥'):
                currency = 'JPY'
            comp_currency.append(currency)

        combined = list(zip(comp_name, comp_mkt, comp_currency))

        for tupla in combined:

            dado_competidor = {
                            "name": tupla[0],
                            "market_cap": {
                                "Currency": tupla[2],
                                "Value": tupla[1]
                                }
                            }

            competitors.append(dado_competidor)

        pct_performance = []

        for value in resp('.element--table.performance .table__row .table__cell .content__item.value'):
            pct_performance.append(value.text)

        market_watch_data = {
            "company_name": company_name,
            "five_days": float(pct_performance[0].strip('%')),
            "one_month": float(pct_performance[1].strip('%')),
            "three_months": float(pct_performance[2].strip('%')),
            "year_to_date": float(pct_performance[3].strip('%')),
            "one_year": float(pct_performance[4].strip('%')),
                "competitors": [
                    competitors
                ]
        }

        logger.info(f"Finished WebScraping on MarketWatch for stock {stock}")
        
        return True, market_watch_data
        
    except Exception as e:
        erro = f'Error during data extraction from MarketWatch - {e}'
        logger.error(erro)
        return False, erro