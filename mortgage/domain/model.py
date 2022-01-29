from dataclasses import dataclass


@dataclass
class BaseMortgage:
    price_mn: float
    initial_payment_mn: float
    period: float
    loan_rate: float


@dataclass
class Mortgage(BaseMortgage):
    pass


@dataclass
class MortgageEP(BaseMortgage):
    first_month: int
    frequency_months: int
    early_payment_amount: int
