import pytest
from decimal import Decimal
from src.entity.exchange_rate_entity import ExchangeRateEntity
from src.repository.exchange_rate_repository import ExchangeRateRepository
from src.config.dynamodb_test_container_config import DynamoDBTestContainerConfig


# Fixture to start and stop the DynamoDB container
@pytest.fixture(scope="module")
def dynamodb_container():
    config = DynamoDBTestContainerConfig().start()
    yield config
    config.stop()


# Fixture to create the ExchangeRates table and provide the repository instance
@pytest.fixture(scope="module")
def exchange_rate_repository(dynamodb_container):
    dynamodb_client = dynamodb_container.create_dynamodb_client()
    dynamodb_container.create_test_table(table_name="ExchangeRates")
    return ExchangeRateRepository(table_name="ExchangeRates")


# Test case to add a new exchange rate entry
def test_post_exchange_rate(exchange_rate_repository):
    exchange_rate = ExchangeRateEntity(
        date="2021-09-01", rates={"EUR/USD": 1.2, "JPY/USD": 0.009}
    )
    result = exchange_rate_repository.post_exchange_rate(exchange_rate)
    assert result is True


# Test case to retrieve an exchange rate by date
def test_get_exchange_rate_by_date(exchange_rate_repository):
    result = exchange_rate_repository.get_exchange_rate_by_date("2021-09-01")
    assert result is not None
    assert result["Date"] == "2021-09-01"
    assert result["Rates"]["EUR/USD"] == Decimal("1.2")


# Test case to retrieve an exchange rate by currency
def test_get_exchange_rate_by_currency(exchange_rate_repository):
    rate = exchange_rate_repository.get_exchange_rate_by_currency("2021-09-01", "EUR")
    assert rate == Decimal("1.2")


# Test case to retrieve exchange rates for multiple currencies
def test_get_exchange_rate_by_currencies(exchange_rate_repository):
    rates = exchange_rate_repository.get_exchange_rate_by_currencies(
        "2021-09-01", ["EUR", "JPY"]
    )
    assert rates["EUR"] == Decimal("1.2")
    assert rates["JPY"] == Decimal("0.009")


# Test case to delete a specific currency exchange rate
def test_delete_exchange_rate(exchange_rate_repository):
    result = exchange_rate_repository.delete_exchange_rate("2021-09-01", "JPY")
    assert result is True

    # Verify that the JPY rate is deleted
    rate = exchange_rate_repository.get_exchange_rate_by_currency("2021-09-01", "JPY")
    assert rate is None
