from datetime import date

from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.db.models.functions import TruncMonth
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

    today = date.today()
    current_month_transactions = transactions.filter(
        date__year=today.year,
        date__month=today.month
    )

    month_income = (
        current_month_transactions.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
    )

    month_expenses = (
        current_month_transactions.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0
    )

    month_balance = month_income - month_expenses

    monthly_summary = (
        Transaction.objects
        .filter(user=request.user)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(
            income=Sum('amount', filter=Q(type='income')),
            expenses=Sum('amount', filter=Q(type='expense')),
        )
        .order_by('month')
    )

    chart_labels = []
    income_data = []
    expense_data = []

    for item in monthly_summary:
        chart_labels.append(item['month'].strftime('%b %Y'))
        income_data.append(float(item['income'] or 0))
        expense_data.append(float(item['expenses'] or 0))

    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,
        'recent_transactions': recent_transactions,
        'month_income': month_income,
        'month_expenses': month_expenses,
        'month_balance': month_balance,
        'chart_labels': chart_labels,
        'income_data': income_data,
        'expense_data': expense_data,
    }

    return render(request, 'dashboard/dashboard.html', context)

