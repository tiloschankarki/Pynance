from django.urls import path
from . import views

app_name = "transactions"

urlpatterns = [
    path("", views.transactions_page, name="page"),
    path("add/", views.transaction_create, name="add"),
    path("<int:pk>/edit/", views.transaction_update, name="edit"),
    path("<int:pk>/delete/", views.transaction_delete, name="delete"),
]