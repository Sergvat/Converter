import requests
import json
from config import exchanges, payload, headers

class ApiException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            return ApiException(f"Валюта {base} не найдена!")
        try:
            quote_key = exchanges[quote.lower()]
        except KeyError:
            raise ApiException(f"Валюта {quote} не найдена!")

        if base_key == quote_key:
            raise ApiException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise ApiException(f'Не удалось обработать количество валюты {amount}!')

        url = f"https://api.apilayer.com/exchangerates_data/convert?to={base_key}&from={quote_key}&amount={amount}"
        response = requests.request("GET", url, headers=headers, data=payload)

        result_json = json.loads(response.content)

        return result_json['result']
