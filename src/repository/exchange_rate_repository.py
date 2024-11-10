import boto3
from src.entity.exchange_rate_entity import ExchangeRateEntity


class ExchangeRateRepository:
    def __init__(self, table_name: str, region_name: str = "us-east-1") -> None:
        self.dynamodb = boto3.resource("dynamodb", region_name=region_name)
        self.table = self.dynamodb.Table(table_name)

    def get_exchange_rate_by_date(self, date: str):
        """
        Retrieves the exchange rate entry for a specific date.

        Args:
            date (str): The date in YYYY-MM-DD format to retrieve the exchange rate entry.

        Returns:
            dict: The exchange rate entry for the specified date or None if not found.
        """
        response = self.table.get_item(Key={"Date": date})

        print(response)

        return response.get("Item")

    def get_exchange_rate_by_currency(self, date: str, currency: str):
        """
        Retrieves the exchange rate for a specific currency on a specific date.

        Args:
            date (str): The date in YYYY-MM-DD format.
            currency (str): The currency to retrieve.

        Returns:
            float: The exchange rate for the specified currency or None if not found.
        """
        print(date, currency)
        rates = self.get_exchange_rate_by_date(date)

        if rates:
            return rates.get("Rates", {}).get(f"{currency}/USD")
        return None

    def get_exchange_rate_by_currencies(self, date: str, currencies: list):
        """
        Retrieves exchange rates for multiple currencies on a specific date.

        Args:
            date (str): The date in YYYY-MM-DD format.
            currencies (list): A list of currencies to retrieve.

        Returns:
            dict: A dictionary of exchange rates for the specified currencies.
        """
        rates = self.get_exchange_rate_by_date(date)

        if rates:
            rates_dict = rates.get("Rates", {})
            return {
                currency: rates_dict.get(f"{currency}/USD") for currency in currencies
            }
        return {}

    def post_exchange_rate(self, exchange_rate: ExchangeRateEntity):
        """
        Adds a new exchange rate entry to DynamoDB using an ExchangeRateEntity instance.

        Args:
            exchange_rate (ExchangeRateEntity): The entity containing exchange rate data.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            self.table.put_item(Item=exchange_rate.to_dict())

            return True
        except Exception as e:
            print(f"Error posting exchange rate: {e}")
            return False

    def delete_exchange_rate(self, date: str, currency: str):
        """
        Deletes a specific currency exchange rate from a given date's entry.

        Args:
            date (str): The date in YYYY-MM-DD format.
            currency (str): The currency to delete from the exchange rate entry.

        Returns:
            bool: True if successful, False otherwise.
        """
        rates = self.get_exchange_rate_by_date(date)

        if rates:
            rates_dict = rates.get("Rates", {})
            if f"{currency}/USD" in rates_dict:
                del rates_dict[f"{currency}/USD"]

                # Update the item in DynamoDB with the modified rates dictionary
                try:
                    self.table.update_item(
                        Key={"Date": date},
                        UpdateExpression="SET Rates = :r",
                        ExpressionAttributeValues={":r": rates_dict},
                    )
                    return True
                except Exception as e:
                    print(f"Error deleting currency from exchange rate: {e}")
                    return False
        return False


if __name__ == "__main__":
    exchange_rate_repository = ExchangeRateRepository("ExchangeRates")

    # Test get_exchange_rate_by_date
    print(exchange_rate_repository.get_exchange_rate_by_date("2021-09-01"))

    # Test get_exchange_rate_by_currency
    print(exchange_rate_repository.get_exchange_rate_by_currency("2021-09-01", "EUR"))

    # Test get_exchange_rate_by_currencies
    print(
        exchange_rate_repository.get_exchange_rate_by_currencies(
            "2021-09-01", ["EUR", "JPY"]
        )
    )

    # Test post_exchange_rate
    exchange_rate = ExchangeRateEntity(
        date="2021-09-01",
        rates={"EUR/USD": 1.2, "JPY/USD": 0.009},
    )
    print(exchange_rate_repository.post_exchange_rate(exchange_rate))

    # Test delete_exchange_rate
    print(exchange_rate_repository.delete_exchange_rate("2021-09-01", "JPY"))
