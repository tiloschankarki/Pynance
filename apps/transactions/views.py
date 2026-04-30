from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
import csv
from io import TextIOWrapper
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction
from .forms import TransactionForm
import json
from django.db.models import Sum
from django.db.models.functions import TruncMonth

@login_required
def transactions_page(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, "transactions/transactions.html", {
        "transactions": transactions
    })


@login_required
def transaction_create(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect("transactions:page")
    else:
        form = TransactionForm()

    return render(request, "transactions/transaction_form.html", {
        "form": form,
        "page_title": "Add Transaction",
    })


@login_required
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)

    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect("transactions:page")
    else:
        form = TransactionForm(instance=transaction)

    return render(request, "transactions/transaction_form.html", {
        "form": form,
        "page_title": "Edit Transaction",
    })


@login_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)

    if request.method == "POST":
        transaction.delete()
        return redirect("transactions:page")

    return render(request, "transactions/transaction_confirm_delete.html", {
        "transaction": transaction,
    })

@login_required
def visualize_transactions(request):
    transactions = Transaction.objects.filter(user=request.user)

    monthly_data = (
        transactions
        .annotate(month=TruncMonth("date"))
        .values("month", "type")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    chart_data = {}

    for item in monthly_data:
        month = item["month"].strftime("%b %Y")

        if month not in chart_data:
            chart_data[month] = {
                "income": 0,
                "expense": 0,
                "net": 0,
            }

        amount = float(item["total"])

        if item["type"].lower() == "income":
            chart_data[month]["income"] = amount
        else:
            chart_data[month]["expense"] = amount

    for month in chart_data:
        chart_data[month]["net"] = (
            chart_data[month]["income"] - chart_data[month]["expense"]
        )

    labels = list(chart_data.keys())
    income_data = [chart_data[month]["income"] for month in labels]
    expense_data = [chart_data[month]["expense"] for month in labels]
    net_data = [chart_data[month]["net"] for month in labels]

    context = {
    "labels": labels,
    "income_data": income_data,
    "expense_data": expense_data,
    "net_data": net_data,
}

    return render(request, "transactions/visualize.html", context)

@login_required
def transaction_csv_upload(request):
    if request.method == "POST":
        csv_file = request.FILES.get("csv_file")

        if not csv_file:
            messages.error(request, "Please select a CSV file.")
            return redirect("transactions:add")

        if not csv_file.name.endswith(".csv"):
            messages.error(request, "Only CSV files are supported.")
            return redirect("transactions:add")

        try:
            file_data = TextIOWrapper(csv_file.file, encoding="utf-8")
            reader = csv.DictReader(file_data)

            created_count = 0

            for row in reader:
                Transaction.objects.create(
                    user=request.user,
                    date=row.get("date"),
                    amount=row.get("amount"),
                    type=row.get("type"),
                    category=row.get("category"),
                    description=row.get("description", ""),
                )
                created_count += 1

            messages.success(request, f"{created_count} transactions imported successfully.")

        except Exception as e:
            messages.error(request, f"CSV upload failed: {e}")

    return redirect("transactions:add")