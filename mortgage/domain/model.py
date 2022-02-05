import dataclasses
from dataclasses import dataclass


@dataclass
class BaseMortgage:
    """Base class with initial data"""
    price: float
    initial_payment: float
    period: float
    loan_rate: float
    month_loan_rate: float = 0
    total_loan_amount: float = 0
    common_rate: float = 0
    monthly_payment: float = 0
    residual_loan: float = 0
    monthly_percent_part: float = 0
    monthly_main_part: float = 0
    overpayment: float = 0
    avg_percent_part: float = 0
    avg_monthly_payment: float = 0
    additional_payments: float = 0
    total_period: int = 0

    def to_dict(self):
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, d):
        if 'price' not in d:
            raise TypeError
        if 'initial_payment' not in d:
            raise TypeError
        if 'period' not in d:
            raise TypeError
        if 'loan_rate' not in d:
            raise TypeError
        for k, v in d.items():
            d[k] = float(v)
        return cls(**d)


@dataclass
class Mortgage(BaseMortgage):
    """Class Mortgage without early payments"""
    pass


@dataclass
class MortgageEP(BaseMortgage):
    """Class Mortgage with early payments"""
    first_month: int = 0
    frequency_months: int = 0
    early_payment_amount: int = 0

# todo: override from_dict method for EP
