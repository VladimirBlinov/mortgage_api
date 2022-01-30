import dataclasses
from dataclasses import dataclass
from abc import ABC, abstractmethod


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


class Builder(ABC):
    """Abstract class of calculator Builder"""
    @abstractmethod
    def payment_calendar(self):
        pass

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
    def get_payments_calendar(self):
        """Calculates payments calendar"""
        pass
