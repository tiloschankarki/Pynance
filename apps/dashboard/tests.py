from datetime import date

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.transactions.models import Transaction

User = get_user_model()


class DashboardViewTests(TestCase):
    # Create two users so we can confirm the dashboard only shows the logged-in user's data
    def setUp(self):
        self.user = User.objects.create_user(
            username="dashboarduser",
            email="dashboard@example.com",
            password="Testpass123!"
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="Testpass123!"
        )

        # Transactions for the logged-in user
        Transaction.objects.create(
            user=self.user,
            date=date(2026, 4, 1),
            amount=500,
            type="income",
            category="income",
            description="Salary"
        )

        Transaction.objects.create(
            user=self.user,
            date=date(2026, 4, 12),
            amount=179,
            type="expense",
            category="variable",
            description="Groceries"
        )

        # Transaction for another user; this should never appear in this user's dashboard totals
        Transaction.objects.create(
            user=self.other_user,
            date=date(2026, 4, 15),
            amount=999,
            type="income",
            category="income",
            description="Other user income"
        )

    # Test that anonymous users are redirected to login
    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    # Test that an authenticated user can load the dashboard page
    def test_dashboard_loads_for_authenticated_user(self):
        self.client.login(username="dashboarduser", password="Testpass123!")

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/dashboard.html")

    # Test that total income, expenses, and balance are calculated correctly
    def test_dashboard_totals_are_correct(self):
        self.client.login(username="dashboarduser", password="Testpass123!")

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.context["total_income"], 500)
        self.assertEqual(response.context["total_expenses"], 179)
        self.assertEqual(response.context["balance"], 321)

    # Test that only the logged-in user's transactions are shown as recent transactions
    def test_recent_transactions_are_user_specific(self):
        self.client.login(username="dashboarduser", password="Testpass123!")

        response = self.client.get(reverse("dashboard"))

        recent_transactions = list(response.context["recent_transactions"])

        self.assertEqual(len(recent_transactions), 2)

        for transaction in recent_transactions:
            self.assertEqual(transaction.user, self.user)

    # Test that chart labels and datasets are included in the dashboard context
    def test_dashboard_chart_data_exists(self):
        self.client.login(username="dashboarduser", password="Testpass123!")

        response = self.client.get(reverse("dashboard"))

        self.assertIn("chart_labels", response.context)
        self.assertIn("income_data", response.context)
        self.assertIn("expense_data", response.context)

    # Test that the chart data contains the user's monthly income and expense totals
    def test_dashboard_chart_data_is_correct(self):
        self.client.login(username="dashboarduser", password="Testpass123!")

        response = self.client.get(reverse("dashboard"))

        self.assertIn("Apr 2026", response.context["chart_labels"])
        self.assertIn(500.0, response.context["income_data"])
        self.assertIn(179.0, response.context["expense_data"])