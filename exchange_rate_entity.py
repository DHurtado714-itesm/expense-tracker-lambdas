from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict


@dataclass
class ExchangeRateEntity:
    date: str = field(default_factory=lambda: datetime.now().date().isoformat())
    base_currency: str = "USD"
    rates: Dict[str, float] = field(default_factory=dict)

    @classmethod
    def new(
        cls, date: str, base_currency: str, rates: Dict[str, float]
    ) -> "ExchangeRateEntity":
        """
        Creates a new ExchangeRateEntity instance.

        Args:
            date (str): The date of the exchange rate.
            base_currency (str): The base currency.
            rates (Dict[str, float]): The exchange rates for each currency.
        """
        return cls(date=date, base_currency=base_currency, rates=rates)

    @classmethod
    def from_dict(cls, data: dict) -> "ExchangeRateEntity":
        """
        Creates an ExchangeRateEntity instance from a dictionary.

        Args:
            data (dict): The dictionary containing the exchange rate data.
        """
        return cls(
            date=data.get("Date"),
            base_currency=data.get("BaseCurrency"),
            rates=data.get("Rates"),
        )

    def to_dict(self) -> dict:
        """
        Converts the ExchangeRateEntity instance to a dictionary format suitable for DynamoDB.
        """
        return {
            "Date": self.date,
            "BaseCurrency": self.base_currency,
            "Rates": self.rates
        }
