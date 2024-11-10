import boto3
from exchange_rate_entity import ExchangeRateEntity


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
