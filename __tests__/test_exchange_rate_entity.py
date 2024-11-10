import unittest
from datetime import datetime

from exchange_rate_entity import ExchangeRateEntity


class TestExchangeRateEntity(unittest.TestCase):
    def setUp(self):
        # Initialize some test data
        self.test_rates = {"COP/USD": 3890.5, "EUR/USD": 0.94, "MXN/USD": 18.7}

    def test_entity_creation_with_default_date(self):
        """
        Test creation of ExchangeRateEntity with default date.
        """

        # Arrange
        today = datetime.now().date().isoformat()

        # Act
        entity = ExchangeRateEntity(rates=self.test_rates)

        # Assert
        self.assertEqual(entity.date, today)
        self.assertEqual(entity.base_currency, "USD")
        self.assertEqual(entity.rates, self.test_rates)

    def test_entity_creation_with_custom_date_and_currency(self):
        """
        Test creation of ExchangeRateEntity with custom date and base currency.
        """
        # Arrange
        custom_date = "2024-11-10"

        # Act
        entity = ExchangeRateEntity(
            date=custom_date, base_currency="EUR", rates=self.test_rates
        )

        # Assert
        self.assertEqual(entity.date, custom_date)
        self.assertEqual(entity.base_currency, "EUR")
        self.assertEqual(entity.rates, self.test_rates)

    def test_entity_to_dict(self):
        """
        Test that the to_dict method produces the correct dictionary format.
        """

        # Arrange
        entity = ExchangeRateEntity(rates=self.test_rates)
        expected_dict = {
            "Date": entity.date,
            "BaseCurrency": "USD",
            "Rates": self.test_rates,
        }

        # Act
        entity_dict = entity.to_dict()

        # Assert
        self.assertEqual(entity_dict, expected_dict)


if __name__ == "__main__":
    unittest.main()
