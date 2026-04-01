from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Transaction
from .forms import TransactionForm


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