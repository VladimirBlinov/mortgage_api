
import dataclasses
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar

import pandas as pd
import base64
from io import BytesIO

from matplotlib import rcParams
from matplotlib.figure import Figure


@dataclass
class IMortgage(ABC):
    MONTH_PER_YEAR: ClassVar[int]
    MLN_MULTIPLIER: ClassVar[int]
    price: float
    initial_payment: float
    period: float
    loan_rate: float
    first_month: int
    frequency: int
    early_pay_amount: int
    start_monthly_payment: int
    period_month: int
    month_loan_rate: float
    total_loan_amount: float
    common_rate: float
    monthly_payment: float
    residual_loan: float
    monthly_percent_part: float
    monthly_main_part: float
    overpayment: float
    avg_percent_part: float
    avg_monthly_payment: float
    additional_payments: float
    total_period: int
    total_payment: int


    @abstractmethod
    def to_dict(self):
        pass


@dataclass
class BaseMortgage(IMortgage):
    """Base class with initial data"""
    MONTH_PER_YEAR: ClassVar[int] = 12
    MLN_MULTIPLIER: ClassVar[int] = 1000000
    price: float
    initial_payment: float
    period: float
    loan_rate: float
    period_month: int = 0
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
    start_monthly_payment: int = 0
    total_payment: int = 0
    first_month: int = 0
    frequency: int = 0
    early_pay_amount: int = 0

    def to_dict(self):
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, d):
        new_dict = {}
        if 'price' not in d:
            raise TypeError
        if 'initial_payment' not in d:
            raise TypeError
        if 'period' not in d:
            raise TypeError
        if 'loan_rate' not in d:
            raise TypeError
        for k, v in d.items():
            if cls.__dataclass_fields__.get(k) is not None:
                new_dict[k] = float(v)
        return cls(**new_dict)


@dataclass
class Mortgage(BaseMortgage):
    """Class Mortgage without early payments"""
    pass


@dataclass
class MortgageEP(BaseMortgage):
    """Class Mortgage with early payments"""
    first_month: int = 0
    frequency: int = 0
    early_pay_amount: int = 0

# todo: override from_dict method for EP


class ICalculator(ABC):
    """Abstract class of calculator Builder"""

    def __init__(self):
        self.mortgage = None
        self.calendar = None
        self.calendar_as_dict = None
        self.avg_percent_part = None
        self.avg_monthly_payment = None
        self.total_payment = None
        self.overpayment = None

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
    def get_overpayment(self):
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

    @abstractmethod
    def format_calendar(self):
        """Format numbers in calendar dict and return them as a string"""
        pass

    def get_averages(self):
        """Gets averages values"""
        pass

    def get_total_payment(self):
        """Get total payment"""
        pass


class BaseCalculator(ICalculator):
    """Base Mortgage calendar builder"""

    def __init__(self, mortgage: IMortgage) -> None:
        """Create new instance of Mortgage calendar"""
        super().__init__()
        self.mortgage = mortgage
        self.calendar = pd.DataFrame()
        self.calendar_as_dict = {}
        self.avg_percent_part: float = 0
        self.avg_monthly_payment: float = 0
        self.total_payment: float = 0
        self.overpayment: float = 0

    def prepare_data(self) -> None:
        """Make transformation of input parameters"""
        self.mortgage.price *= self.mortgage.MLN_MULTIPLIER
        self.mortgage.initial_payment *= self.mortgage.MLN_MULTIPLIER
        self.mortgage.period_month = int(self.mortgage.period * self.mortgage.MONTH_PER_YEAR)
        self.mortgage.month_loan_rate = self.mortgage.loan_rate / self.mortgage.MONTH_PER_YEAR / 100
        self.mortgage.total_loan_amount = int(self.mortgage.price - self.mortgage.initial_payment)

    def common_rate(self) -> None:
        """# ОБЩАЯ_СТАВКА = (1 + ЕЖЕМЕСЯЧНАЯ_СТАВКА) ^ СРОК_ИПОТЕКИ_МЕСЯЦЕВ"""
        self.mortgage.common_rate = (1 + self.mortgage.month_loan_rate) ** self.mortgage.period_month

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

    def get_total_payment(self):
        self.total_payment = self.calendar.monthly_payment.sum() # + additional payments

    def get_overpayment(self):
        """# ПЕРЕПЛАТА = ОБЩАЯ СУММА - СУММА_КРЕДИТА"""
        self.overpayment = self.total_payment - self.mortgage.total_loan_amount

    def calculate_first_month(self):
        """Calculate attributes after first month"""
        self.mortgage.residual_loan = self.mortgage.residual_loan - self.mortgage.monthly_main_part
        _data_dict = {'monthly_payment': self.mortgage.monthly_payment,
                      'main_part': self.mortgage.monthly_main_part,
                      'percent_part': self.mortgage.monthly_percent_part,
                      'percent_cum': self.mortgage.monthly_percent_part,
                      'residual_loan_amount': self.mortgage.residual_loan,
                      }
        self.calendar = pd.DataFrame(data=_data_dict, index=[1])
        self.calendar.index.name = 'month'

    def get_calendar(self):
        """Calculates payments calendar"""
        for month in range(2, self.mortgage.period_month + 1):
            self.mortgage.monthly_percent_part = self.mortgage.residual_loan * self.mortgage.month_loan_rate
            self.mortgage.monthly_main_part = self.mortgage.monthly_payment - self.mortgage.monthly_percent_part
            self.mortgage.residual_loan = self.mortgage.residual_loan - self.mortgage.monthly_main_part
            if self.mortgage.residual_loan < 0:
                self.mortgage.residual_loan = 0
            _data_dict = {'monthly_payment': self.mortgage.monthly_payment,
                          'main_part': self.mortgage.monthly_main_part,
                          'percent_part': self.mortgage.monthly_percent_part,
                          'percent_cum': self.calendar['percent_part'].sum() + self.mortgage.monthly_percent_part,
                          'residual_loan_amount': self.mortgage.residual_loan
                          }
            self.calendar = pd.concat([self.calendar, pd.DataFrame(data=_data_dict, index=[month])], ignore_index=False)

    def get_averages(self):
        self.avg_percent_part = int(self.calendar.percent_part[self.calendar.percent_part != 0].mean())
        self.avg_monthly_payment = int(self.calendar.monthly_payment[self.calendar.monthly_payment != 0].mean())

    def format_calendar(self):
        self.calendar_as_dict = self.calendar.to_dict('index')
        for key, value in self.calendar_as_dict.items():
            for k, v in value.items():
                self.calendar_as_dict[key][k] = '{:,}'.format(int(v)).replace(',', ' ')
        return self.calendar_as_dict


class Calculator(BaseCalculator):
    def __init__(self, mortgage: Mortgage) -> None:
        """Create new instance of Mortgage calendar"""
        super().__init__(mortgage)


class CalculatorEP(BaseCalculator):
    def __init__(self, mortgage_ep: IMortgage) -> None:
        """Create new instance of Mortgage calendar"""
        super().__init__(mortgage_ep)

    def get_calendar(self):
        """Calculates payments calendar"""
        # TODO: check residual loan calculation
        self.mortgage.start_monthly_payment = self.mortgage.monthly_payment
        for month in range(2, self.mortgage.period_month + 1):
            if self.mortgage.residual_loan > 0:
                self.mortgage.monthly_percent_part = self.mortgage.residual_loan * self.mortgage.month_loan_rate
                if self.mortgage.residual_loan <= 0:
                    self.mortgage.residual_loan = 0
                    self.mortgage.monthly_payment = 0

                self.mortgage.monthly_payment = self.mortgage.residual_loan * self.mortgage.month_loan_rate * \
                                                self.mortgage.common_rate / (self.mortgage.common_rate - 1)
                self.mortgage.monthly_main_part = self.mortgage.monthly_payment - self.mortgage.monthly_percent_part
                self.mortgage.residual_loan = self.mortgage.residual_loan - self.mortgage.monthly_main_part

                if month >= self.mortgage.first_month and month % self.mortgage.frequency == 0:
                    if self.mortgage.residual_loan - (self.mortgage.early_pay_amount +
                                                      (self.mortgage.start_monthly_payment -
                                                       self.mortgage.monthly_payment)) > 0:
                        self.mortgage.additional_payments += \
                            (self.mortgage.early_pay_amount + (self.mortgage.start_monthly_payment -
                                                               self.mortgage.monthly_payment))
                        self.mortgage.residual_loan = self.mortgage.residual_loan - (self.mortgage.early_pay_amount +
                                                                                     (self.mortgage.start_monthly_payment -
                                                                                      self.mortgage.monthly_payment))
                        if self.mortgage.period_month > month:
                            self.mortgage.common_rate = (1 + self.mortgage.month_loan_rate) ** \
                                                        (self.mortgage.period_month - month)
                    else:
                        self.mortgage.additional_payments += self.mortgage.residual_loan
                        self.mortgage.residual_loan = self.mortgage.residual_loan - self.mortgage.residual_loan

                _data_dict = {'monthly_payment': self.mortgage.monthly_payment,
                              'percent_part': self.mortgage.monthly_percent_part,
                              'percent_cum': self.calendar['percent_part'].sum() + self.mortgage.monthly_percent_part,
                              'main_part': self.mortgage.monthly_main_part,
                              'residual_loan_amount': self.mortgage.residual_loan
                              }
                self.calendar = pd.concat([self.calendar, pd.DataFrame(data=_data_dict, index=[month])], ignore_index=False)

    def get_total_payment(self):
        self.total_payment = self.calendar.monthly_payment.sum() + self.mortgage.additional_payments


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
        self.calculator.calculate_first_month()
        self.calculator.get_calendar()
        self.calculator.get_total_payment()
        self.calculator.get_overpayment()
        self.calculator.get_averages()
        self.calculator.format_calendar()
        return self.calculator.calendar_as_dict


class Chart:
    PLOT_MONTH_TICKS: ClassVar[int] = 6
    PLOT_PAYMENTS_TICKS: ClassVar[int] = 5000

    def __init__(self, calculator: ICalculator):
        self.calculator = calculator
        self.fig = Figure()
        self.ax = self.fig.subplots()
        _xticks = [x for x in range(0, self.calculator.calendar.shape[0], self.PLOT_MONTH_TICKS)]
        _yticks = [y for y in range(0, (int(round(self.calculator.calendar.monthly_payment[1], 0)) +
                                        2 * self.PLOT_PAYMENTS_TICKS), self.PLOT_PAYMENTS_TICKS)]
        _ytickslabels = ['{:,.0f}'.format(y).replace(",", " ") for y in _yticks]
        self.ax.set_xlim(left=0, right=self.calculator.calendar.shape[0])
        self.ax.set_ylim(bottom=0, top=max(_yticks))
        self.ax.set_xticks(ticks=_xticks)
        self.ax.set_yticks(ticks=_yticks, labels=_ytickslabels)
        self.ax.tick_params(axis='both', labelsize=3)
        self.ax.set_xlabel(xlabel=f'Month', fontdict={'fontsize': 'x-small'})
        self.ax.set_ylabel(ylabel=f'RUB', fontdict={'fontsize': 'x-small'})
        self.ax.grid()

    def draw_chart(self):
        rcParams['axes.titlesize'] = 'x-small'
        rcParams['lines.linewidth'] = 1
        self.ax.plot([float(x) for x in self.calculator.calendar.percent_part.values], label='Percent part', color='r')
        self.ax.plot([float(x) for x in self.calculator.calendar.main_part.values], label='Main part', color='g')
        self.ax.hlines(self.calculator.avg_percent_part, xmin=self.calculator.calendar.index[0],
                       xmax=self.calculator.calendar.index[-1],
                       label=f'Average percent payment {round(self.calculator.avg_percent_part, 2):,}'
                             f' RUB'.replace(',', ' '),
                       color='y')
        self.ax.hlines(self.calculator.avg_monthly_payment, xmin=self.calculator.calendar.index[0],
                       xmax=self.calculator.calendar.index[-1],
                       label=f'Average monthly payment {int(self.calculator.avg_monthly_payment):,} RUB'.replace(',', ' '),
                       color='b')
        self.ax.set_title(label=(f'Period: {int(self.calculator.mortgage.period):,} years; '
                                 f'Price: {int(self.calculator.mortgage.price):,} RUB; '
                                 f'Loan rate: {self.calculator.mortgage.loan_rate}%;\n'
                                 f'Initial payment: {int(self.calculator.mortgage.initial_payment):,} RUB; '
                                 f'Total loan amount: {int(self.calculator.mortgage.total_loan_amount):,} RUB; '
                                 f'Total payment: {int(self.calculator.total_payment):,} RUB;\n'
                                 f'Average monthly payment: {int(self.calculator.avg_monthly_payment):,} RUB; '
                                 f'Overpayment: {int(self.calculator.overpayment):,} RUB'.replace(',', ' ')),
                          fontdict={'fontsize': rcParams['axes.titlesize']})

        self.ax.legend(fontsize='x-small')
        # Save it to a temporary buffer.
        buf = BytesIO()
        self.fig.savefig(buf, format="png", dpi=500)
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return f"data:image/png;base64,{data}"
