from flask import Flask, request, jsonify
from flask_caching import Cache
from stock_log import definelog
from stock_main import main
import constants as cnt
import subprocess

logger = definelog()

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/stock/<string:stock_symbol>', methods=['GET'])
@cache.cached(timeout=60, key_prefix='stock_data')
def get_stock(stock_symbol):
    try:
        if stock_symbol:
            service = main('get', stock_symbol, 0)
            
            if not service[0]:
                return jsonify({'error': str(service[1])}), 404
            else:
                return jsonify({f'{stock_symbol}': service[1]})
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return jsonify({'error': 'An internal error occurred'}), 500


@app.route('/stock/<string:stock_symbol>', methods=['POST'])
def update_stock(stock_symbol):
    try:
        if not request.json or 'amount' not in request.json:
            return jsonify({'error': 'Please, inform the amount purchased for that stock'}), 400
        
        amount = request.json['amount']

        if stock_symbol:
            service = main('post', stock_symbol, amount)

            if not service[0]:
                return jsonify({'error': str(service[1])}), 404
            else:
                return jsonify({'message': f"{amount} units of stock {stock_symbol} were added to your stock record"}), 201
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return jsonify({'error': 'An internal error occurred'}), 500

if __name__ == '__main__':

    try:
        result = subprocess.run(['service', 'postgresql', 'start'], check=True, text=True, capture_output=True)
        print("PostgreSQL started with sucess!")
        print(result.stdout)

        shrun = subprocess.run(['bash', "./entrypoint.sh"], capture_output=True, text=True)
        print("Entrypoint run!")

    except subprocess.CalledProcessError as e:
        print("Erro ao iniciar o PostgreSQL:")
        print(e.stderr)
    
    print("Initializing - version 8.0")
    app.run(debug=True, host='0.0.0.0', port=cnt.port_server)




