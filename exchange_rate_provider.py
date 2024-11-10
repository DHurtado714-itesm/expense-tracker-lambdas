import requests


def map_exchange_api_response(
    rates: dict, base_currency: str, selected_currencies: list
) -> dict:
    return {
        f"{currency}/{base_currency}": rates[currency]
        for currency in selected_currencies
        if currency in rates
    }


class ExchangeRate:
    def __init__(self) -> None:
        self.base_currency = "USD"
        self.selected_currencies = ["COP", "EUR", "MXN"]
        self.base_url = f"https://open.er-api.com/v6/latest/{self.base_currency}"

    def fetch_data(self):
        response = requests.get(self.base_url)

        if response.status_code == 200:
            data = response.json()

            return map_exchange_api_response(
                data["rates"], self.base_currency, self.selected_currencies
            )
        else:
            raise Exception("Fialed to fetch rates")
