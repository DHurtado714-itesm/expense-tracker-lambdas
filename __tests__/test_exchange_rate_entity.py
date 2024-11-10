import pytest
from datetime import datetime
from decimal import Decimal
from src.entity.exchange_rate_entity import ExchangeRateEntity


@pytest.fixture
def test_rates():
    return {"COP/USD": 3890.5, "EUR/USD": 0.94, "MXN/USD": 18.7}


def test_entity_creation_with_default_date(test_rates):
    """
    Test creation of ExchangeRateEntity with default date.
    """
    # Arrange
    today = datetime.now().date().isoformat()

    # Act
    entity = ExchangeRateEntity(rates=test_rates)

    # Assert
    assert entity.date == today
    assert entity.base_currency == "USD"
    assert entity.rates == test_rates


def test_entity_creation_with_custom_date_and_currency(test_rates):
    """
    Test creation of ExchangeRateEntity with custom date and base currency.
    """
    # Arrange
    custom_date = "2024-11-10"

    # Act
    entity = ExchangeRateEntity(date=custom_date, base_currency="EUR", rates=test_rates)

    # Assert
    assert entity.date == custom_date
    assert entity.base_currency == "EUR"
    assert entity.rates == test_rates


def test_entity_to_dict(test_rates):
    """
    Test that the to_dict method produces the correct dictionary format.
    """
    # Arrange
    entity = ExchangeRateEntity(rates=test_rates)
    expected_dict = {
        "Date": entity.date,
        "BaseCurrency": "USD",
        "Rates": {k: Decimal(str(v)) for k, v in test_rates.items()},
    }

    # Act
    entity_dict = entity.to_dict()

    # Assert
    assert entity_dict == expected_dict


def test_entity_creation_from_dict():
    """
    Test creation of ExchangeRateEntity from a dictionary.
    """
    # Arrange
    data = {
        "Date": "2024-11-10",
        "BaseCurrency": "USD",
        "Rates": {"COP/USD": 3890.5, "EUR/USD": 0.94, "MXN/USD": 18.7},
    }

    # Act
    entity = ExchangeRateEntity.from_dict(data)

    # Assert
    assert entity.date == "2024-11-10"
    assert entity.base_currency == "USD"
    assert entity.rates == data["Rates"]
