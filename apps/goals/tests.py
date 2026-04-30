from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.goals.models import Goal

User = get_user_model()


class GoalViewsTests(TestCase):
    # Create two users so we can test user-specific access and data isolation
    def setUp(self):
        self.user = User.objects.create_user(
            username="goaluser",
            email="goal@example.com",
            password="Testpass123!"
        )

        self.other_user = User.objects.create_user(
            username="othergoaluser",
            email="othergoal@example.com",
            password="Testpass123!"
        )

        self.goal = Goal.objects.create(
            user=self.user,
            title="Emergency Fund",
            target_amount=Decimal("1000.00"),
            saved_amount=Decimal("250.00"),
            note="Build savings"
        )

        self.other_goal = Goal.objects.create(
            user=self.other_user,
            title="Other User Goal",
            target_amount=Decimal("5000.00"),
            saved_amount=Decimal("1000.00"),
            note="Private goal"
        )

    # Test that the goals page requires authentication
    def test_goals_page_requires_login(self):
        response = self.client.get(reverse("goals:page"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    # Test that an authenticated user can view the goals page
    def test_goals_page_loads_for_authenticated_user(self):
        self.client.login(username="goaluser", password="Testpass123!")

        response = self.client.get(reverse("goals:page"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "goals/goals.html")

    # Test that the goals page only shows goals owned by the logged-in user
    def test_goals_page_only_shows_user_goals(self):
        self.client.login(username="goaluser", password="Testpass123!")

        response = self.client.get(reverse("goals:page"))

        goals = list(response.context["goals"])

        self.assertIn(self.goal, goals)
        self.assertNotIn(self.other_goal, goals)

    # Test that the add goal page loads correctly
    def test_goal_create_page_loads(self):
        self.client.login(username="goaluser", password="Testpass123!")

        response = self.client.get(reverse("goals:add"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "goals/goal_form.html")
        self.assertEqual(response.context["page_title"], "Add Goal")

    # Test that a user can create a goal
    def test_user_can_create_goal(self):
        self.client.login(username="goaluser", password="Testpass123!")

        response = self.client.post(reverse("goals:add"), {
            "title": "Vacation Fund",
            "target_amount": "2000.00",
            "saved_amount": "300.00",
            "note": "Summer trip"
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("goals:page"))

        self.assertTrue(
            Goal.objects.filter(user=self.user, title="Vacation Fund").exists()
        )

    # Test that goal creation does not happen when required fields are missing
    def test_goal_create_fails_with_invalid_data(self):
        self.client.login(username="goaluser", password="Testpass123!")

        response = self.client.post(reverse("goals:add"), {
            "title": "",
            "target_amount": "",
            "saved_amount": "100.00",
            "note": "Missing required fields"
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Goal.objects.filter(user=self.user, note="Missing required fields").exists()
        )

    # Test that the edit goal page loads for the goal owner
    def test_goal_update_page_loads_for_owner(self):
        self.client.login(username="goaluser", password="Testpass123!")

        response = self.client.get(reverse("goals:edit", args=[self.goal.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "goals/goal_form.html")
        self.assertEqual(response.context["page_title"], "Edit Goal")

    # Test that a user can update their own goal
    def test_user_can_update_own_goal(self):
        self.client.login(username="goaluser", password="Testpass123!")

        response = self.client.post(reverse("goals:edit", args=[self.goal.pk]), {
            "title": "Updated Emergency Fund",
            "target_amount": "1500.00",
            "saved_amount": "500.00",
            "note": "Updated savings goal"
        })

        self.goal.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("goals:page"))
        self.assertEqual(self.goal.title, "Updated Emergency Fund")
        self.assertEqual(self.goal.target_amount, Decimal("1500.00"))
        self.assertEqual(self.goal.saved_amount, Decimal("500.00"))

    # Test that a user cannot edit another user's goal
    def test_user_cannot_update_other_users_goal(self):
        self.client.login(username="goaluser", password="Testpass123!")

        response = self.client.post(reverse("goals:edit", args=[self.other_goal.pk]), {
            "title": "Hacked Goal",
            "target_amount": "1.00",
            "saved_amount": "1.00",
            "note": "Should not work"
        })

        self.other_goal.refresh_from_db()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.other_goal.title, "Other User Goal")

    # Test that delete confirmation page loads for the owner
    def test_goal_delete_confirmation_loads_for_owner(self):
        self.client.login(username="goaluser", password="Testpass123!")

        response = self.client.get(reverse("goals:delete", args=[self.goal.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "goals/goal_confirm_delete.html")

    # Test that a user can delete their own goal
    def test_user_can_delete_own_goal(self):
        self.client.login(username="goaluser", password="Testpass123!")

        response = self.client.post(reverse("goals:delete", args=[self.goal.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("goals:page"))
        self.assertFalse(Goal.objects.filter(pk=self.goal.pk).exists())

    # Test that a user cannot delete another user's goal
    def test_user_cannot_delete_other_users_goal(self):
        self.client.login(username="goaluser", password="Testpass123!")

        response = self.client.post(reverse("goals:delete", args=[self.other_goal.pk]))

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Goal.objects.filter(pk=self.other_goal.pk).exists())


class GoalModelTests(TestCase):
    # Test the string representation of a goal
    def test_goal_string_representation(self):
        user = User.objects.create_user(
            username="modeluser",
            password="Testpass123!"
        )

        goal = Goal.objects.create(
            user=user,
            title="Laptop Fund",
            target_amount=Decimal("1200.00"),
            saved_amount=Decimal("300.00")
        )

        self.assertEqual(str(goal), "Laptop Fund")

    # Test that progress percentage is calculated correctly
    def test_progress_percentage_calculates_correctly(self):
        user = User.objects.create_user(
            username="progressuser",
            password="Testpass123!"
        )

        goal = Goal.objects.create(
            user=user,
            title="Car Fund",
            target_amount=Decimal("1000.00"),
            saved_amount=Decimal("250.00")
        )

        self.assertEqual(goal.progress_percentage, Decimal("25.00"))

    # Test that progress percentage does not exceed 100
    def test_progress_percentage_is_capped_at_100(self):
        user = User.objects.create_user(
            username="capuser",
            password="Testpass123!"
        )

        goal = Goal.objects.create(
            user=user,
            title="Completed Goal",
            target_amount=Decimal("1000.00"),
            saved_amount=Decimal("1500.00")
        )

        self.assertEqual(goal.progress_percentage, 100)

    # Test that progress percentage returns 0 when target amount is 0
    def test_progress_percentage_returns_zero_for_zero_target(self):
        user = User.objects.create_user(
            username="zerouser",
            password="Testpass123!"
        )

        goal = Goal.objects.create(
            user=user,
            title="Zero Target Goal",
            target_amount=Decimal("0.00"),
            saved_amount=Decimal("100.00")
        )

        self.assertEqual(goal.progress_percentage, 0)