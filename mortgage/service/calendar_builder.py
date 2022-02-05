from abc import ABC, abstractmethod
from mortgage.domain.model import Mortgage


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
    def get_payments_calendar(self):
        """Calculates payments calendar"""
        pass


class MortgageBuilder(Builder):
    """ Mortgage calendar builder without early payment"""

    def __init__(self, data_dict) -> None:
        """Create new instance of Mortgage calendar"""
        self.calendar = Mortgage.from_dict(data_dict)
