from mortgage.domain.model import Mortgage, MortgageEP


def test_mortgage_model_init():
    mortgage = Mortgage(price_mn=20, initial_payment_mn=2,
                        period=30, loan_rate=7.5)
    assert mortgage.price_mn == 20
    assert mortgage.initial_payment_mn == 2
    assert mortgage.period == 30
    assert mortgage.loan_rate == 7.5


def test_mortgage_model_with_early_payment_init():
    mortgage = MortgageEP(price_mn=20, initial_payment_mn=2,
                          period=30, loan_rate=7.5, first_month=24,
                          frequency_months=1, early_payment_amount=50000)
    assert mortgage.price_mn == 20
    assert mortgage.initial_payment_mn == 2
    assert mortgage.period == 30
    assert mortgage.loan_rate == 7.5
    assert mortgage.first_month == 24
    assert mortgage.frequency_months == 1
    assert mortgage.early_payment_amount == 50000
