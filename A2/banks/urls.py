from django.contrib import admin
from django.urls import path , include
from .views import *

urlpatterns = [
    path('add/', add_bank_view , name='add_bank'),
    path('<int:bank_id>/details/' , bank_details_view , name='bank_details'),
    path('<int:bank_id>/add_branch/' , add_branch_view , name='add_branch'),
    path('branch/<int:branch_id>/details/', branch_details_view, name='branch_details'),
    path('',list_banks_view,name='list_banks'),
]