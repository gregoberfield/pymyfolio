from django.urls import path
from . import views


urlpatterns = [
    path('add-equity/', views.add_equity_form, name='Add Equity'),
    path('indextest/', views.displaytest, name='Index Test'),
    path('indextest2/', views.displaytest2, name='Index Test'),
]
