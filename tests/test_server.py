import unittest
from unittest.mock import patch, MagicMock
from flask import json
from app import app

class StockApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('stock_main.main')
    def test_get_stock_success(self, mock_main):
        # Simula o retorno de um sucesso na função main
        mock_main.return_value = (True, {"price": 100})
        
        response = self.app.get('/stock/AAPL')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('AAPL', data)
        self.assertEqual(data['AAPL']['price'], 100)

    @patch('stock_main.main')
    def test_get_stock_not_found(self, mock_main):
        # Simula o retorno de uma falha na função main
        mock_main.return_value = (False, "Stock not found")
        
        response = self.app.get('/stock/INVALID')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)
        self.assertEqual(data['error'], "Stock not found")

    @patch('stock_main.main')
    def test_post_stock_success(self, mock_main):
        # Simula o retorno de um sucesso na função main
        mock_main.return_value = (True, None)
        
        response = self.app.post('/stock/AAPL', json={'amount': '50'})
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
        self.assertEqual(data['error'], 'Please, send a valid amount value.')

if __name__ == '__main__':
    unittest.main()
