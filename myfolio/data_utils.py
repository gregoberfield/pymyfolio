from .models import *
import pyEX as p
import quandl
from django.conf import settings

# set a global var for the client
iex_client = p.Client(api_token=settings.IEX_TOKEN, version='v1')

# TODO: Need to add better error handling


def get_company_data(symbol):
    try:
        data = iex_client.company(symbol=symbol)
        if data:
            return Equity(symbol=data['symbol'], name=data['companyName'],
                          exchange=data['exchange'], industry=data['industry'],
                          sector=data['sector'], sic=data['primarySicCode'])
    except Exception as e:
        print("Exception: ", e.args[1])

    return None
