from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import *
import pyEX as p
from django.conf import settings


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
                company = iex_client.company(form.cleaned_data['symbol'])
            # redirect to a new URL:
            # return HttpResponseRedirect(request.path_info)
            return render(request, 'add_equity_form.html', {'form': form, 'data': company})
        else:
            print("Something wrong with the form")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddEquityForm()

    return render(request, 'add_equity_form.html', {'form': form})

