from .models import *
import pyEX as p
import quandl
from django.conf import settings

# set a global var for the client
iex_client = p.Client(api_token=settings.IEX_TOKEN, version='v1')

# TODO: Need to add better error handling

'''
Get company data from IEX.  Format it into a model object and return.
'''


def get_equity_data(symbol):
    try:
        data = iex_client.company(symbol=symbol)
        if data:
            return Equity(symbol=data['symbol'], name=data['companyName'],
                          exchange=data['exchange'], industry=data['industry'],
                          sector=data['sector'], sic=data['primarySicCode'])
    except Exception as e:
        print("Exception: ", e.args[1])

    return None


def get_equity_dividend(equity):
    try:
        iex_data = iex_client.dividends(symbol=equity.symbol, timeframe='next')
        if iex_data:
            frequency = Dividend.Frequency.QUARTERLY
            if iex_data['frequency'] == 'monthly':
                frequency = Dividend.Frequency.MONTHLY

            return Dividend(equity=equity,
                            ex_date=iex_data['exDate'],
                            payment_date=iex_data['paymentDate'],
                            record_date=iex_data['recordDate'],
                            declared_date=iex_data['declaredDate'],
                            amount=iex_data['amount'],
                            flag=iex_data['flag'],
                            currency=iex_data['currency'],
                            description=iex_data['description'],
                            frequency=frequency
                            )
    except Exception as e:
        print("Exception: ", e.args[1])

    return None
