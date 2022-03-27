import dataclasses
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar
import pandas as pd


@dataclass
class BaseMortgage:
    """Base class with initial data"""
    MONTH_PER_YEAR: ClassVar[int] = 12
    MLN_MULTIPLIER: ClassVar[int] = 1000000
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


class ICalculator(ABC):
    """Abstract class of calculator Builder"""
    def __init__(self):
        self.calendar = {}
        self._calendar_df = pd.DataFrame()

    @abstractmethod
    def prepare_data(self):
        """Make transformation of input parameters"""
        pass

    @abstractmethod
    def common_rate(self):
        """# ОБЩАЯ_СТАВКА = (1 + ЕЖЕМЕСЯЧНАЯ_СТАВКА) ^ СРОК_ИПОТЕКИ_МЕСЯЦЕВ"""
        pass

    @abstractmethod
    def monthly_payment(self):
        """# ЕЖЕМЕСЯЧНЫЙ_ПЛАТЕЖ = СУММА_КРЕДИТА * ЕЖЕМЕСЯЧНАЯ_СТАВКА * ОБЩАЯ_СТАВКА / (ОБЩАЯ_СТАВКА - 1)"""
        pass

    @abstractmethod
    def residual_loan(self):
        """# ОСТАТОК ДОЛГА"""
        pass

    @abstractmethod
    def monthly_percent_part(self):
        """# ПРОЦЕНТНАЯ_ЧАСТЬ = ОСТАТОК_ДОЛГА * ЕЖЕМЕСЯЧНАЯ_СТАВКА"""
        pass

    @abstractmethod
    def monthly_main_part(self):
        """# ОСНОВНАЯ_ЧАСТЬ = ЕЖЕМЕСЯЧНЫЙ_ПЛАТЕЖ - ПРОЦЕНТНАЯ_ЧАСТЬ"""
        pass

    @abstractmethod
    def overpayment(self):
        """# ПЕРЕПЛАТА = ЕЖЕМЕСЯЧНЫЙ_ПЛАТЕЖ * СРОК_ИПОТЕКИ_МЕСЯЦЕВ - СУММА_КРЕДИТА"""
        pass

    @abstractmethod
    def calculate_first_month(self):
        """Calculate attributes after first month"""
        pass

    @abstractmethod
    def get_calendar(self):
        """Calculates payments calendar"""
        pass


class Calculator(ICalculator):
    """Base Mortgage calendar builder"""

    def __init__(self, mortgage: Mortgage) -> None:
        """Create new instance of Mortgage calendar"""
        super().__init__()
        self.mortgage = mortgage

    def prepare_data(self) -> None:
        """Make transformation of input parameters"""
        self.mortgage.price *= self.mortgage.MLN_MULTIPLIER
        self.mortgage.initial_payment *= self.mortgage.MLN_MULTIPLIER
        self.mortgage.period *= self.mortgage.MONTH_PER_YEAR
        self.mortgage.period = int(self.mortgage.period)
        self.mortgage.month_loan_rate = self.mortgage.loan_rate / self.mortgage.MONTH_PER_YEAR / 100
        self.mortgage.total_loan_amount = self.mortgage.price - self.mortgage.initial_payment

    def common_rate(self) -> None:
        """# ОБЩАЯ_СТАВКА = (1 + ЕЖЕМЕСЯЧНАЯ_СТАВКА) ^ СРОК_ИПОТЕКИ_МЕСЯЦЕВ"""
        self.mortgage.common_rate = (1 + self.mortgage.month_loan_rate) ** self.mortgage.period

    def monthly_payment(self):
        """# ЕЖЕМЕСЯЧНЫЙ_ПЛАТЕЖ = СУММА_КРЕДИТА * ЕЖЕМЕСЯЧНАЯ_СТАВКА * ОБЩАЯ_СТАВКА / (ОБЩАЯ_СТАВКА - 1)"""
        self.mortgage.monthly_payment = self.mortgage.total_loan_amount * self.mortgage.month_loan_rate *\
            self.mortgage.common_rate / (self.mortgage.common_rate - 1)

    def residual_loan(self):
        """# ОСТАТОК ДОЛГА"""
        self.mortgage.residual_loan = self.mortgage.total_loan_amount

    def monthly_percent_part(self):
        """# ПРОЦЕНТНАЯ_ЧАСТЬ = ОСТАТОК_ДОЛГА * ЕЖЕМЕСЯЧНАЯ_СТАВКА"""
        self.mortgage.monthly_percent_part = self.mortgage.residual_loan * self.mortgage.month_loan_rate

    def monthly_main_part(self):
        """# ОСНОВНАЯ_ЧАСТЬ = ЕЖЕМЕСЯЧНЫЙ_ПЛАТЕЖ - ПРОЦЕНТНАЯ_ЧАСТЬ"""
        self.mortgage.monthly_main_part = self.mortgage.monthly_payment - self.mortgage.monthly_percent_part

    def overpayment(self):
        """# ПЕРЕПЛАТА = ЕЖЕМЕСЯЧНЫЙ_ПЛАТЕЖ * СРОК_ИПОТЕКИ_МЕСЯЦЕВ - СУММА_КРЕДИТА"""
        self.mortgage.overpayment = self.mortgage.monthly_payment * self.mortgage.period -\
            self.mortgage.total_loan_amount

    def calculate_first_month(self):
        """Calculate attributes after first month"""
        self.mortgage.residual_loan = self.mortgage.residual_loan - self.mortgage.monthly_main_part
        _data_dict = {'Percent_part': self.mortgage.monthly_percent_part,
                      'Main_part': self.mortgage.monthly_main_part,
                      'Monthly_payment': self.mortgage.monthly_payment,
                      'Residual_loan_amount': self.mortgage.residual_loan,
                      }
        self._calendar_df = pd.DataFrame(data=_data_dict, index=[1])

    def get_calendar(self):
        """Calculates payments calendar"""
        pass


class ICalculatorBuilder(ABC):
    @abstractmethod
    def build_calculator(self):
        pass


class CalculatorBuilder(ICalculatorBuilder):
    def __init__(self, calculator: ICalculator):
        self.calculator = calculator

    def build_calculator(self):
        self.calculator.prepare_data()
        self.calculator.common_rate()
        self.calculator.monthly_payment()
        self.calculator.residual_loan()
        self.calculator.monthly_percent_part()
        self.calculator.monthly_main_part()
        self.calculator.overpayment()
        self.calculator.calculate_first_month()
        self.calculator.get_calendar()
