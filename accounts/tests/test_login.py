from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone


class LoginTestCase(TestCase):
    """
    A Unit test case for the Django login and logout default behavior include
    in the 'auth' package. It checks the login/logout logic, the error messages,
    and the correct handling of user sessions.
    """
    LOGIN_URL = reverse('login')
    HOMEPAGE_URL = reverse('home')

    @classmethod
    def setUpTestData(cls):
        """
        This method creates objects in a test database that are available to
        all unit tests. It is called only once for this test case, and the
        created objects are shared among all unit tests in this test case.
        """
        # Custom user model used by this project
        user_model = get_user_model()

        # Test user
        cls.user = user_model.objects.create(
            username='test_user',
            password='some_password',
            email='test@example.net',
            age=18
        )

        cls.user_2 = user_model.objects.create(
            username='test_user_2',
            password='some_password',
            email='test_2@example.net',
            age=18
        )

        # Use of non-encrypted password
        cls.user.set_password('test_pass')
        cls.user_2.set_password('test_pass')

        cls.user.save()
        cls.user_2.save()

    def test_login_form_render_user_not_authenticated(self):
        """
        Checks that the login form renders are correct for a non-authenticated
        user.
        """
        # HTTP Response
        response = self.client.get(self.LOGIN_URL)

        # Checks that an HTTP 200 (OK) status code is returned.
        self.assertEqual(
            first=response.status_code,
            second=200
        )

        # Verify that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='registration/login.html'
        )

    def test_login_form_render_user_authenticated(self):
        """
        Checks that the login form renders are correct for an authenticated
        user (example: for change accounts).
        """
        self.client.login(
            username='test_user',
            password='test_pass'
        )

        # HTTP Response
        response = self.client.get(self.LOGIN_URL)

        # Checks that an HTTP 200 (OK) status code is returned.
        self.assertEqual(
            first=response.status_code,
            second=200
        )

        # Verify that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='registration/login.html'
        )

    def test_valid_login_form_submit_user_not_authenticated(self):
        """
        Checks that a non-authenticated user can submit the login form
        with valid data.
        """
        login_data = {
            'username': 'test_user',
            'password': 'test_pass'
        }

        # HTTP Response
        response = self.client.post(
            path=self.LOGIN_URL,
            data=login_data,
            follow=True
        )

        # Verifies that there is a redirect to the website homepage
        self.assertRedirects(
            response=response,
            expected_url=self.HOMEPAGE_URL,
            status_code=302,
            target_status_code=200
        )

        # Verify that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='home.html'
        )

    def test_invalid_login_form_submit_user_not_authenticated(self):
        """
        Checks that a non-authenticated user cannot submit the login form
        with invalid data.
        """
        login_data = {
            'username': 'invalid_user',
            'password': 'test_pass'
        }

        # HTTP Response
        response = self.client.post(
            path=self.LOGIN_URL,
            data=login_data,
            follow=True
        )

        # Checks that an HTTP 200 (OK) status code is returned
        self.assertEqual(
            first=response.status_code,
            second=200
        )

        # Verify that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='registration/login.html'
        )

        # Checks that the form in the context has errors
        self.assertTrue(response.context['form'].errors)

    def test_valid_login_form_submit_user_authenticated(self):
        """
        Checks that an authenticated user can submit the login form
        with valid data, for change to another account.
        """
        self.client.login(
            username='test_user',
            password='test_pass'
        )

        login_data = {
            'username': 'test_user_2',
            'password': 'test_pass'
        }

        # HTTP Response
        response = self.client.post(
            path=self.LOGIN_URL,
            data=login_data,
            follow=True
        )

        # Verifies that there is a redirect to the website homepage
        self.assertRedirects(
            response=response,
            expected_url=self.HOMEPAGE_URL,
            status_code=302,
            target_status_code=200
        )

        # Verify that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='home.html'
        )

        # Check that only are one session active
        active_sessions = Session.objects.filter(
            expire_date__gte=timezone.now()
        )
        self.assertEqual(
            first=active_sessions.count(),
            second=1
        )
