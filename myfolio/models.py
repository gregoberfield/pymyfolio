from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now


class Portfolio(models.Model):
    name = models.CharField(max_length=32, default="Default Portfolio", null=False, unique=True)
    description = models.TextField(default="")

    class Meta:
        verbose_name_plural = "Portfolios"


class Strategy(models.Model):
    name = models.CharField(max_length=32)
    short_name = models.CharField(max_length=8)
    description = models.TextField(max_length=4096)

    class Meta:
        verbose_name_plural = 'Strategies'


class Equity(models.Model):
    symbol = models.CharField(max_length=5, null=False, primary_key=True)
    name = models.CharField(max_length=32)
    exchange = models.CharField(max_length=16)
    industry = models.CharField(max_length=64)
    sector = models.CharField(max_length=64)
    sic = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Equities"


class Price(models.Model):
    equity = models.ForeignKey(Equity, on_delete=models.CASCADE)
    open = models.FloatField(default=0.0)
    high = models.FloatField(default=0.0)
    low = models.FloatField(default=0.0)
    close = models.FloatField(default=0.0)
    volume = models.IntegerField(default=0)
    date = models.DateField()

    class Meta:
        verbose_name_plural = "Prices"


class Transaction(models.Model):

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
    date = models.DateField(null=False)
    strategy = models.ForeignKey(Strategy, on_delete=models.SET_NULL, null=True)
    # do I need commission / fee / broker / etc?

    class Meta:
        verbose_name_plural = "Transactions"


class Holding(models.Model):
    equity = models.ForeignKey(Equity, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    open_date = models.DateField(null=False)
    close_date = models.DateField(default=None)

    class Meta:
        verbose_name_plural = 'Holdings'
        unique_together = (('equity', 'portfolio'),)


class Dividend(models.Model):

    class Frequency(models.TextChoices):
        QUARTERLY = 'QTR', _('Quarterly')
        MONTHLY = 'MTH', _('Monthly')
        YEARLY = 'YR', _('Yearly')
        SPECIAL = 'SPC', _('Special')
        MISC = 'MISC', _('Miscellaneous')

    equity = models.ForeignKey(Equity, on_delete=models.CASCADE)
    ex_date = models.DateField(default=None)
    payment_date = models.DateField(default=None)
    record_date = models.DateField(default=None)
    declared_date = models.DateField(default=None)
    amount = models.FloatField(default=0.0)
    flag = models.CharField(max_length=64)
    currency = models.CharField(max_length=16)
    description = models.CharField(max_length=128)
    frequency = models.CharField(
        max_length=4,
        choices=Frequency.choices,
        default=Frequency.QUARTERLY
    )

    class Meta:
        verbose_name_plural = 'Dividends'
