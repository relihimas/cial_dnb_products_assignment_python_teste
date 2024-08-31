import unittest
from unittest.mock import patch
from flask import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from stock_server import app

json_retorno = {
    "aapl": {
        "company_code": "AAPL",
        "company_name": "TESTE",
        "competitors": [
            "TESTE"
        ],
        "performance_data": {
            "five_days": 1.0,
            "one_month": 1.0,
            "one_year": 1.0,
            "three_months": 1.0,
            "year_to_date": 1.0
        },
        "purchased_amount": 0,
        "purchased_status": "completed",
        "request_data": "2024-08-29",
        "status": "OK",
        "stock_values": {
            "close": 229.79,
            "high": 232.92,
            "low": 228.88,
            "open": 230.1
        }
    }
}

class StockApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('stock_main.main')
    def test_get_stock_success(self, mock_main):
        # Simula o retorno de um sucesso na função main
        mock_main.return_value = (True, json_retorno)
        
        response_stock_success = self.app.get('/stock/aapl')
        data = json.loads(response_stock_success.data)
        
        self.assertEqual(response_stock_success.status_code, 200)
        self.assertIn('aapl', data)
        self.assertEqual(data, json_retorno)

    @patch('stock_main.main')
    def test_get_stock_not_found(self, mock_main):
        # Simula o retorno de uma falha na função main
        mock_main.return_value = (False, "Stock name is not valid.")
        
        response_not_found = self.app.get('/stock/INVALID')
        data = json.loads(response_not_found.data)

        self.assertEqual(response_not_found.status_code, 404)
        self.assertIn('error', data)
        self.assertEqual(data['error'], "Stock name is not valid.")

    @patch('stock_main.main')
    def test_post_stock_success(self, mock_main):
        # Simula o retorno de um sucesso na função main
        mock_main.return_value = (True, "50 units of stock AAPL were added to your stock record")
        
        response = self.app.post('/stock/AAPL', json={'amount': 50})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertIn('message', data)
        self.assertEqual(data['message'], "50 units of stock AAPL were added to your stock record")

    def test_post_stock_missing_amount(self):
        # Teste para a ausência do campo "amount" no JSON
        response = self.app.post('/stock/AAPL', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Please, inform the amount purchased for that stock')

    def test_post_stock_empty_amount(self):
        # Teste para o envio de um valor vazio no campo "amount"
        response = self.app.post('/stock/AAPL', json={'amount': ''})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Please, inform the amount purchased for that stock')

if __name__ == '__main__':
    unittest.main()
