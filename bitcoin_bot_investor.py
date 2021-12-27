import yfinance as yf
from logging import Logger


lcl_logger = Logger(name='btc_logger')


def parameter_quality(time_span_years: int,
                      lower_threshold: float,
                      upper_threshold: float):
    """
    Check that parameters make sense
    """
    # Threshold different to zero
    if lower_threshold == 0.0:
        lcl_logger.error('lower_threshold must be different to 0.')
        raise ValueError('lower_threshold must be different to 0.')
    if upper_threshold == 0.0:
        lcl_logger.error('upper_threshold must be different to 0.')
        raise ValueError('upper_threshold must be different to 0.')
    # Positive time span
    if time_span_years <= 0:
        lcl_logger.error(f'time_span_years be positive. Provided value is: {time_span_years}.')
        raise ValueError(f'time_span_years be positive. Provided value is: {time_span_years}.')
    # Lower threshold must be strictly higher to upper threshold.
    if lower_threshold >= upper_threshold:
        lcl_logger.error(f'lower_threshold must be strictly higher to upper_threshold.')
        raise ValueError(f'lower_threshold must be strictly higher to upper_threshold.')
    # Checking signs of thresholds
    if lower_threshold > 0:
        lcl_logger.warning('lower_threshold is positive.')
    if upper_threshold < 0:
        lcl_logger.warning('upper_threshold is negative.')
    lcl_logger.info('Parameter checks has been completed successfully.')


def estimate_strategy_returns(time_span_years: int = 1,
                              lower_threshold: float = -0.05,
                              upper_threshold: float = 0.05) -> float:
    """
    Computes the realized returns in Euros if a bitcoin (BTC-EUR) is invested following a naive approach of selling one
    when bitcoin price surge by upper_threshold in a single day (close rate) and buying when daily price variation is
    lower to lower_threshold.
    :param time_span_years: Number of years the strategy is going to be applied.
    :param lower_threshold: buying call. The bot buys btc when price changes lower to this threshold.
    :param upper_threshold: selling call. Sell for any daily variation higher to this threshold.
    :return: Float representing the return of following this strategy.
    """
    lcl_logger.info('Checking Data Quality.')
    parameter_quality(time_span_years=time_span_years,
                      lower_threshold=lower_threshold,
                      upper_threshold=upper_threshold)
    lcl_logger.info('Downloading data.')
    asset_info = yf.Ticker('BTC-EUR')
    df = asset_info.history(period=f'{time_span_years}y', interval="1d")[['Close']].dropna()
    df.rename({'Close': 'price'}, axis=1, inplace=True)
    df_pct = df.pct_change()
    lcl_logger.debug('Instantiating local variables.')
    investment = 0.0
    value_of_sell = 0.0
    current_price = 0
    buy_prices = list()
    lcl_logger.info('Performing selling and buying options.')
    for price_date, price_change in df_pct.dropna().iterrows():
        current_price = df.loc[price_date, 'price']
        if price_change[0] <= lower_threshold:
            buy_prices.append(current_price)
            investment += 100.0
        if price_change[0] >= upper_threshold:
            value_of_sell += sum([100*current_price/item for item in buy_prices])
            buy_prices = list()
    lcl_logger.info('Correcting remainder')
    if len(buy_prices) > 0:
        value_of_sell += sum([100 * current_price / item for item in buy_prices])
    return (value_of_sell-investment)/investment
