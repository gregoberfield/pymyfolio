from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import *
from .data_utils import *


def displaytest(request):
    return render(request, 'index.html')


def add_equity_form(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddEquityForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            if '_add' in request.POST:
                if Equity.objects.filter(symbol=form.cleaned_data['symbol']).exists():
                    print("already in database")
                else:
                    company = get_equity_data(form.cleaned_data['symbol'])

                    if not company:
                        print("error in equity")
                        return render(request, 'add_equity_form.html', {'form': form})
                    dividend = get_equity_dividend(company)

                    company.save()

                    # only save the dividend if it exists
                    if dividend:
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

