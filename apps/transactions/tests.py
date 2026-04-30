from datetime import date
from decimal import Decimal
from io import BytesIO

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.transactions.models import Transaction

User = get_user_model()


class TransactionViewsTests(TestCase):
    # Create two users so we can test user-specific transaction access
    def setUp(self):
        self.user = User.objects.create_user(
            username="transactionuser",
            email="transaction@example.com",
            password="Testpass123!"
        )

        self.other_user = User.objects.create_user(
            username="othertransactionuser",
            email="othertransaction@example.com",
            password="Testpass123!"
        )

        self.transaction = Transaction.objects.create(
            user=self.user,
            amount=Decimal("100.00"),
            type="income",
            category="income",
            date=date(2026, 4, 1),
            description="Salary"
        )

        self.expense = Transaction.objects.create(
            user=self.user,
            amount=Decimal("40.00"),
            type="expense",
            category="variable",
            date=date(2026, 4, 3),
            description="Groceries"
        )

        self.other_transaction = Transaction.objects.create(
            user=self.other_user,
            amount=Decimal("999.00"),
            type="income",
            category="income",
            date=date(2026, 4, 5),
            description="Other user's transaction"
        )

    # Test that the transactions page requires login
    def test_transactions_page_requires_login(self):
        response = self.client.get(reverse("transactions:page"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    # Test that the transactions page loads for authenticated users
    def test_transactions_page_loads_for_authenticated_user(self):
        self.client.login(username="transactionuser", password="Testpass123!")

        response = self.client.get(reverse("transactions:page"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "transactions/transactions.html")

    # Test that users only see their own transactions
    def test_transactions_page_only_shows_user_transactions(self):
        self.client.login(username="transactionuser", password="Testpass123!")

        response = self.client.get(reverse("transactions:page"))

        transactions = list(response.context["transactions"])

        self.assertIn(self.transaction, transactions)
        self.assertIn(self.expense, transactions)
        self.assertNotIn(self.other_transaction, transactions)

    # Test that the add transaction page loads correctly
    def test_transaction_create_page_loads(self):
        self.client.login(username="transactionuser", password="Testpass123!")

        response = self.client.get(reverse("transactions:add"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "transactions/transaction_form.html")
        self.assertEqual(response.context["page_title"], "Add Transaction")

    # Test that a user can create a transaction
    def test_user_can_create_transaction(self):
        self.client.login(username="transactionuser", password="Testpass123!")

        response = self.client.post(reverse("transactions:add"), {
            "amount": "250.00",
            "type": "expense",
            "category": "fixed",
            "date": "2026-04-10",
            "description": "Rent"
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("transactions:page"))

        self.assertTrue(
            Transaction.objects.filter(
                user=self.user,
                amount=Decimal("250.00"),
                description="Rent"
            ).exists()
        )

    # Test that invalid transaction data does not create a transaction
    def test_transaction_create_fails_with_invalid_data(self):
        self.client.login(username="transactionuser", password="Testpass123!")

        response = self.client.post(reverse("transactions:add"), {
            "amount": "",
            "type": "expense",
            "category": "fixed",
            "date": "2026-04-10",
            "description": "Invalid transaction"
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Transaction.objects.filter(description="Invalid transaction").exists()
        )

    # Test that the edit transaction page loads for the transaction owner
    def test_transaction_update_page_loads_for_owner(self):
        self.client.login(username="transactionuser", password="Testpass123!")

        response = self.client.get(reverse("transactions:edit", args=[self.transaction.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "transactions/transaction_form.html")
        self.assertEqual(response.context["page_title"], "Edit Transaction")

    # Test that a user can update their own transaction
    def test_user_can_update_own_transaction(self):
        self.client.login(username="transactionuser", password="Testpass123!")

        response = self.client.post(reverse("transactions:edit", args=[self.transaction.pk]), {
            "amount": "300.00",
            "type": "income",
            "category": "income",
            "date": "2026-04-15",
            "description": "Updated Salary"
        })

        self.transaction.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("transactions:page"))
        self.assertEqual(self.transaction.amount, Decimal("300.00"))
        self.assertEqual(self.transaction.description, "Updated Salary")

    # Test that users cannot update transactions owned by another user
    def test_user_cannot_update_other_users_transaction(self):
        self.client.login(username="transactionuser", password="Testpass123!")

        response = self.client.post(reverse("transactions:edit", args=[self.other_transaction.pk]), {
            "amount": "1.00",
            "type": "income",
            "category": "income",
            "date": "2026-04-20",
            "description": "Should not update"
        })

        self.other_transaction.refresh_from_db()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.other_transaction.amount, Decimal("999.00"))

    # Test that delete confirmation page loads for the transaction owner
    def test_transaction_delete_confirmation_loads_for_owner(self):
        self.client.login(username="transactionuser", password="Testpass123!")

        response = self.client.get(reverse("transactions:delete", args=[self.transaction.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "transactions/transaction_confirm_delete.html")

    # Test that a user can delete their own transaction
    def test_user_can_delete_own_transaction(self):
        self.client.login(username="transactionuser", password="Testpass123!")

        response = self.client.post(reverse("transactions:delete", args=[self.transaction.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("transactions:page"))
        self.assertFalse(Transaction.objects.filter(pk=self.transaction.pk).exists())

    # Test that users cannot delete transactions owned by another user
    def test_user_cannot_delete_other_users_transaction(self):
        self.client.login(username="transactionuser", password="Testpass123!")

        response = self.client.post(reverse("transactions:delete", args=[self.other_transaction.pk]))

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Transaction.objects.filter(pk=self.other_transaction.pk).exists())

    # Test that the visualize page loads for authenticated users
    def test_visualize_page_loads(self):
        self.client.login(username="transactionuser", password="Testpass123!")

        response = self.client.get(reverse("transactions:visualize"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "transactions/visualize.html")

    # Test that visualize page context contains chart data
    def test_visualize_page_contains_chart_data(self):
        self.client.login(username="transactionuser", password="Testpass123!")

        response = self.client.get(reverse("transactions:visualize"))

        self.assertIn("labels", response.context)
        self.assertIn("income_data", response.context)
        self.assertIn("expense_data", response.context)
        self.assertIn("net_data", response.context)

    # Test that visualize page calculates income, expense, and net cash flow correctly
    def test_visualize_chart_data_is_correct(self):
        self.client.login(username="transactionuser", password="Testpass123!")

        response = self.client.get(reverse("transactions:visualize"))

        self.assertIn("Apr 2026", response.context["labels"])
        self.assertIn(100.0, response.context["income_data"])
        self.assertIn(40.0, response.context["expense_data"])
        self.assertIn(60.0, response.context["net_data"])

    # Test that a valid CSV file can import multiple transactions
    def test_csv_upload_creates_transactions(self):
        self.client.login(username="transactionuser", password="Testpass123!")

        csv_content = (
            "date,amount,type,category,description\n"
            "2026-04-20,500.00,income,income,Freelance Payment\n"
            "2026-04-21,75.50,expense,variable,Restaurant\n"
        )

        csv_file = BytesIO(csv_content.encode("utf-8"))
        csv_file.name = "transactions.csv"

        response = self.client.post(reverse("transactions:upload_csv"), {
            "csv_file": csv_file
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("transactions:add"))

        self.assertTrue(
            Transaction.objects.filter(user=self.user, description="Freelance Payment").exists()
        )
        self.assertTrue(
            Transaction.objects.filter(user=self.user, description="Restaurant").exists()
        )

    # Test that upload fails when no CSV file is provided
    def test_csv_upload_fails_without_file(self):
        self.client.login(username="transactionuser", password="Testpass123!")

        response = self.client.post(reverse("transactions:upload_csv"), {})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("transactions:add"))

    # Test that non-CSV files are rejected
    def test_csv_upload_rejects_non_csv_file(self):
        self.client.login(username="transactionuser", password="Testpass123!")

        fake_file = BytesIO(b"not a csv file")
        fake_file.name = "transactions.txt"

        response = self.client.post(reverse("transactions:upload_csv"), {
            "csv_file": fake_file
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("transactions:add"))

        self.assertFalse(
            Transaction.objects.filter(description="not a csv file").exists()
        )


class TransactionModelTests(TestCase):
    # Test the string representation of a transaction
    def test_transaction_string_representation(self):
        user = User.objects.create_user(
            username="modeltransactionuser",
            password="Testpass123!"
        )

        transaction = Transaction.objects.create(
            user=user,
            amount=Decimal("123.45"),
            type="expense",
            category="variable",
            date=date(2026, 4, 30),
            description="Test Transaction"
        )

        expected = "modeltransactionuser | expense | 123.45 | 2026-04-30"

        self.assertEqual(str(transaction), expected)