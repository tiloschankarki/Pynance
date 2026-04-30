from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountsViewsTests(TestCase):
    # Set up a reusable test user for login, logout, and settings tests
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="Testpass123!"
        )

    # Test that the login page loads successfully for anonymous users
    def test_login_page_loads(self):
        response = self.client.get(reverse("accounts:login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    # Test that a valid user can log in and is redirected to the home page
    def test_user_can_login_with_valid_credentials(self):
        response = self.client.post(reverse("accounts:login"), {
            "username": "testuser",
            "password": "Testpass123!",
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    # Test that invalid login credentials do not authenticate the user
    def test_login_fails_with_invalid_credentials(self):
        response = self.client.post(reverse("accounts:login"), {
            "username": "testuser",
            "password": "wrongpassword",
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    # Test that an authenticated user is redirected away from the login page
    def test_authenticated_user_redirected_from_login(self):
        self.client.login(username="testuser", password="Testpass123!")

        response = self.client.get(reverse("accounts:login"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    # Test that the registration page loads successfully
    def test_register_page_loads(self):
        response = self.client.get(reverse("accounts:register"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    # Test that a new user can register successfully
    def test_user_can_register(self):
        response = self.client.post(reverse("accounts:register"), {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "Strongpass123!",
            "password2": "Strongpass123!",
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")
        self.assertTrue(User.objects.filter(username="newuser").exists())

    # Test that registration fails when passwords do not match
    def test_register_fails_when_passwords_do_not_match(self):
        response = self.client.post(reverse("accounts:register"), {
            "username": "baduser",
            "email": "bad@example.com",
            "password1": "Strongpass123!",
            "password2": "Differentpass123!",
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="baduser").exists())

    # Test that logout redirects the user back to the login page
    def test_user_can_logout(self):
        self.client.login(username="testuser", password="Testpass123!")

        response = self.client.post(reverse("accounts:logout"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("accounts:login"))

    # Test that settings page requires login
    def test_settings_requires_login(self):
        response = self.client.get(reverse("accounts:settings"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    # Test that authenticated users can access the settings page
    def test_settings_page_loads_for_authenticated_user(self):
        self.client.login(username="testuser", password="Testpass123!")

        response = self.client.get(reverse("accounts:settings"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/settings.html")

    # Test that a user can update their username from the settings page
    def test_user_can_update_username(self):
        self.client.login(username="testuser", password="Testpass123!")

        response = self.client.post(reverse("accounts:settings"), {
            "username": "updateduser",
            "update_username": "1",
        })

        self.user.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.username, "updateduser")

    # Test that a user can update their password from the settings page
    def test_user_can_update_password(self):
        self.client.login(username="testuser", password="Testpass123!")

        response = self.client.post(reverse("accounts:settings"), {
            "old_password": "Testpass123!",
            "new_password1": "Newstrongpass123!",
            "new_password2": "Newstrongpass123!",
            "update_password": "1",
        })

        self.assertEqual(response.status_code, 302)

        # Confirm the password was actually changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("Newstrongpass123!"))

    # Test that password update fails when the old password is incorrect
    def test_password_update_fails_with_wrong_old_password(self):
        self.client.login(username="testuser", password="Testpass123!")

        response = self.client.post(reverse("accounts:settings"), {
            "old_password": "Wrongpass123!",
            "new_password1": "Newstrongpass123!",
            "new_password2": "Newstrongpass123!",
            "update_password": "1",
        })

        self.user.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user.check_password("Newstrongpass123!"))