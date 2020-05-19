from django.db import models
import datetime
from django.utils.translation import gettext_lazy as _


class Portfolio(models.model):
    name = models.CharField(max_length=32, default="Default Portfolio", null=False, unique=True)
    description = models.TextField(default="")

    class Meta:
        verbose_name_plural = "Portfolios"


class Equity(models.model):
    ticker = models.CharField(max_length=5, null=False, primary_key=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Equities"


class Price(models.model):
    equity = models.ForeignKey(Equity, on_delete=models.CASCADE)
    open = models.FloatField(default=0.0)
    high = models.FloatField(default=0.0)
    low = models.FloatField(default=0.0)
    close = models.FloatField(default=0.0)
    volume = models.IntegerField(default=0)
    date = models.DateField(default=datetime.datetime.now())

    class Meta:
        verbose_name_plural = "Prices"


class Transaction(models.model):

    class Type(models.TextChoices):
        BUY = 'BUY', _('Buy')
        SELL = 'SELL', _('Sell')
        DIVIDEND = 'DIV', _('Dividend')
        FEE = 'FEE', _('Fee')
        MISC = 'MISC', _('Miscellaneous')

    type = models.CharField(
        max_length=4,
        choices=Type.choices,
        default=Type.MISC
    )
    quantity = models.IntegerField(default=0)
    amount = models.FloatField(default=0.0)
    equity = models.ForeignKey(Equity, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.datetime.now(), null=False)
    # do I need commission / fee / broker / etc?

    class Meta:
        verbose_name_plural = "Transactions"


class Holding(models.model):
    equity = models.ForeignKey(Equity, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    open_date = models.DateField(default=datetime.datetime.now(), null=False)
    close_date = models.DateField(default=None)

    class Meta:
        verbose_name_plural = 'Holdings'
        unique_together = (('equity', 'portfolio'),)
