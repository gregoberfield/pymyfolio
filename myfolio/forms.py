from django import forms


class AddEquityForm(forms.Form):
    symbol = forms.CharField(max_length=4, label='symbol')
