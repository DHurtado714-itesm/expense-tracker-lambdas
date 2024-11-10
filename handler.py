from datetime import datetime
import json
import os
import requests
from enum import Enum


class NotionProperties(Enum):
    ID = "id"
    NUMBER = "number"
    SELECT = "select"


def map_exchange_api_response(
    rates: dict, base_currency: str, selected_currencies: list
) -> dict:
    return {
        f"{currency}/{base_currency}": rates[currency]
        for currency in selected_currencies
        if currency in rates
    }


def map_properties_from_notion_response(response: dict, properties: dict) -> list:
    """
    Extracts specified properties from Notion response with support for multiple types.

    Args:
        response (dict): The Notion API response containing pages.
        properties (dict): A dictionary where keys are property names and values are the NotionProperties enum type.

    Returns:
        list: A list of dictionaries with the specified properties and their values.
    """
    results = []
    for page in response.get("results", []):
        entry = {}
        for property_name, property_type in properties.items():
            # Access the specified property within properties based on type
            property_data = page["properties"].get(property_name, {})

            if property_type == NotionProperties.ID:
                entry[property_name] = page["id"]
            elif property_type == NotionProperties.NUMBER:
                entry[property_name] = property_data.get("number")
            elif property_type == NotionProperties.SELECT:
                # Extract the name from select
                entry[property_name] = property_data.get("select", {}).get("name")

        # Only append entries with at least one property value
        if entry:
            results.append(entry)

    return results


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


class NotionManager:
    def __init__(self) -> None:
        self.notion_token = os.getenv("NOTION_TOKEN")
        self.headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        self.page_url = "https://api.notion.com/v1/pages"
        self.exchange_rate = ExchangeRate()
        self.today_iso = datetime.now().date().isoformat()

    def calculate_usd_equivalent(self, amount: float, currency: str) -> float:
        rates = self.exchange_rate.fetch_data()

        currency_pair = f"{currency.upper()}/USD"
        currency_rate = rates.get(currency_pair)

        if currency_rate is None:
            raise ValueError(f"No exchange rate found for currency: {currency}")

        return amount / currency_rate

    def get_data(self, database_id: str, properties: dict, filter_body: dict) -> list:
        """
        Fetches data from a specified Notion database with a filter.

        Args:
            database_id (str): The ID of the Notion database to query.
            properties (dict): The properties to retrieve, with their types.
            filter_body (dict): The filter body for the query.

        Returns:
            list: A list of dictionaries with the specified properties.
        """
        url = f"https://api.notion.com/v1/databases/{database_id}/query"
        response = requests.post(url, headers=self.headers, json=filter_body)

        if response.status_code == 200:
            data = response.json()
            return map_properties_from_notion_response(data, properties)
        else:
            raise Exception(f"Failed to fetch data from database {database_id}")

    def update_page(self, entry_id: str, properties: dict):
        """
        Updates properties for a specific Notion page.

        Args:
            entry_id (str): The ID of the Notion page to update.
            properties (dict): The properties and their values to update.
        """
        url = f"{self.page_url}/{entry_id}"
        update_body = {"properties": properties}

        response = requests.patch(url, headers=self.headers, json=update_body)
        if response.status_code != 200:
            raise Exception(f"Failed to update page {entry_id}: {response.text}")

    def update_pages(
        self,
        database_id: str,
        properties_to_retrieve: dict,
        filter_body: dict,
        update_field: str,
    ):
        """
        Fetches data from a Notion database, calculates USD equivalent, and updates pages.

        Args:
            database_id (str): The ID of the Notion database.
            properties_to_retrieve (dict): The properties to retrieve, with their types.
            filter_body (dict): The filter body for querying.
            update_field (str): The name of the field to update with the calculated value.
        """
        pages = self.get_data(database_id, properties_to_retrieve, filter_body)

        for page in pages:
            amount = page.get("Local Amount")
            currency = page.get("Currencies")

            if amount is not None and currency:
                if currency and "USD" in currency:
                    # If the currency is in USD, use the amount directly
                    usd_equivalent = amount
                else:
                    usd_equivalent = self.calculate_usd_equivalent(amount, currency)

                update_properties = {update_field: {"number": usd_equivalent}}
                self.update_page(page["id"], update_properties)
