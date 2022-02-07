from abc import ABC, abstractmethod
from mortgage.domain.model import BaseMortgage


class Builder(ABC):
    """Abstract class of calculator Builder"""

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


class BaseBuilder(Builder):
    """Base Mortgage calendar builder"""

    def __init__(self, data_dict: dict) -> None:
        """Create new instance of Mortgage calendar"""
        self.calendar = BaseMortgage.from_dict(data_dict)

    def prepare_data(self) -> None:
        """Make transformation of input parameters"""
        self.calendar.price *= self.calendar.MLN_MULTIPLIER
        self.calendar.initial_payment *= self.calendar.MLN_MULTIPLIER
        self.calendar.period *= self.calendar.MONTH_PER_YEAR
        self.calendar.period = int(self.calendar.period)
        self.calendar.month_loan_rate = self.calendar.loan_rate / self.calendar.MONTH_PER_YEAR / 100
        self.calendar.total_loan_amount = self.calendar.price - self.calendar.initial_payment

    def common_rate(self) -> None:
        """# ОБЩАЯ_СТАВКА = (1 + ЕЖЕМЕСЯЧНАЯ_СТАВКА) ^ СРОК_ИПОТЕКИ_МЕСЯЦЕВ"""
        self.calendar.common_rate = (1 + self.calendar.month_loan_rate) ** self.calendar.period

    def monthly_payment(self):
        """# ЕЖЕМЕСЯЧНЫЙ_ПЛАТЕЖ = СУММА_КРЕДИТА * ЕЖЕМЕСЯЧНАЯ_СТАВКА * ОБЩАЯ_СТАВКА / (ОБЩАЯ_СТАВКА - 1)"""
        pass

    def residual_loan(self):
        """# ОСТАТОК ДОЛГА"""
        pass

    def monthly_percent_part(self):
        """# ПРОЦЕНТНАЯ_ЧАСТЬ = ОСТАТОК_ДОЛГА * ЕЖЕМЕСЯЧНАЯ_СТАВКА"""
        pass

    def monthly_main_part(self):
        """# ОСНОВНАЯ_ЧАСТЬ = ЕЖЕМЕСЯЧНЫЙ_ПЛАТЕЖ - ПРОЦЕНТНАЯ_ЧАСТЬ"""
        pass

    def overpayment(self):
        """# ПЕРЕПЛАТА = ЕЖЕМЕСЯЧНЫЙ_ПЛАТЕЖ * СРОК_ИПОТЕКИ_МЕСЯЦЕВ - СУММА_КРЕДИТА"""
        pass

    def calculate_first_month(self):
        """Calculate attributes after first month"""
        pass

    def get_calendar(self):
        """Calculates payments calendar"""
        pass
