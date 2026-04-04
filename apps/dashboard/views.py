from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render

from apps.transactions.models import Transaction


@login_required
def dashboard_home(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    total_income = (
        transactions.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
    )

    total_expenses = (
        transactions.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0
    )

    balance = total_income - total_expenses

    recent_transactions = transactions[:5]

    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,
        'recent_transactions': recent_transactions,
    }

    return render(request, 'dashboard/dashboard.html', context)

