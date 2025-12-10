import requests
from flask import Blueprint, request, jsonify

# Создаем "чертеж" (Blueprint)
currency_bp = Blueprint('currency', __name__)


@currency_bp.route('/currency', methods=['GET'])
def get_currency():
    param = request.args.get('param', 'today')
    url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=USD&json'

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data:
                return jsonify({
                    'currency': 'USD',
                    'rate': data[0]['rate'],
                    'date': data[0]['exchangedate'],
                    'param': param
                })
        return jsonify({'error': 'NBU API Error'}), 502
    except Exception as e:
        return jsonify({'error': str(e)}), 500