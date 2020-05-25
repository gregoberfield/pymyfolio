from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import *
import pyEX as p
from django.conf import settings
from .models import Equity, Dividend


def add_equity_form(request):
    iex_client = p.Client(api_token=settings.IEX_TOKEN, version='v1')
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddEquityForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            if '_add' in request.POST:
                iex_data = iex_client.company(form.cleaned_data['symbol'])
                company = Equity(symbol=iex_data['symbol'], name=iex_data['companyName'],
                                 exchange=iex_data['exchange'], industry=iex_data['industry'],
                                 sector=iex_data['sector'], sic=iex_data['primarySicCode'])

                iex_data = iex_client.dividends(form.cleaned_data['symbol'], timeframe='next')
                if iex_data:
                    frequency = Dividend.Frequency.QUARTERLY
                    if iex_data['frequency'] == 'monthly':
                        frequency = Dividend.Frequency.MONTHLY

                    dividend = Dividend(equity=company,
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

                    company.save()
                    dividend.save()

            # redirect to a new URL:
            # return HttpResponseRedirect(request.path_info)
            return render(request, 'add_equity_form.html', {'form': form})
        else:
            print("Something wrong with the form")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddEquityForm()

    return render(request, 'add_equity_form.html', {'form': form})

