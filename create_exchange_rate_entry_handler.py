import os

from src.entity.exchange_rate_entity import ExchangeRateEntity
from src.libs.exchange_rate_provider import ExchangeRate
from src.repository.exchange_rate_repository import ExchangeRateRepository


def create_exchange_rate_entry_handler(event, context):
    table_name = os.getenv("EXCHANGE_RATE_TABLE_NAME", "ExchangeRates")

    repository = ExchangeRateRepository(table_name=table_name)
    exchange_rate = ExchangeRate()

    try:
        rates = exchange_rate.fetch_data()

        exchange_rate_entity = ExchangeRateEntity(rates=rates)

        result = repository.post_exchange_rate(exchange_rate_entity)

        if result:
            return {
                "statusCode": 200,
                "body": "Exchange rate entry created successfully.",
            }
        else:
            return {"statusCode": 500, "body": "Failed to create exchange rate entry."}
    except Exception as e:
        return {"statusCode": 500, "body": f"An error occurred: {str(e)}"}
