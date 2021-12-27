from bitcoin_bot_investor import *
import pytest


def test_default():
    result = estimate_strategy_returns()
    assert pytest.approx(0.0146, result, 0.0001)


def test_decrease_10_increase_5():
    result = estimate_strategy_returns(lower_threshold=-0.1)
    assert pytest.approx(0.0043, result, 0.0001)


def test_increase_1_increase_5():
    result = estimate_strategy_returns(lower_threshold=0.01)
    assert pytest.approx(0.0082, result, 0.0001)


def test_error():
    with pytest.raises(ValueError) as e_info:
        result = estimate_strategy_returns(upper_threshold=-1.0, lower_threshold=1.0)
    assert True
