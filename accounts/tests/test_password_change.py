from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.test import TestCase
from django.urls import reverse


class PasswordChangeTestCase(TestCase):
    """
    A unit test case for the default password change behavior in Django,
    that is included in the 'auth' package.
    """
    LOGIN_URL = reverse('login')
    PASSWORD_CHANGE_URL = reverse('password_change')
    PASSWORD_CHANGE_DONE_URL = reverse('password_change_done')

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

        # Use of non-encrypted password
        cls.user.set_password('test_pass')
        cls.user.save()

    def test_password_change_form_render_user_not_authenticated(self):
        """
        Checks that an attempt to access the password change form for a
        non-authenticated user results in a redirect to the login page.
        """
        # HTTP Response
        response = self.client.get(
            path=self.PASSWORD_CHANGE_URL,
            follow=True
        )

        # Checks that there is a redirect to the login page
        redirect_url = f'{self.LOGIN_URL}?next={self.PASSWORD_CHANGE_URL}'
        self.assertRedirects(
            response=response,
            expected_url=redirect_url,
            status_code=302,
            target_status_code=200
        )

        # Checks that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='registration/login.html'
        )

    def test_password_change_form_render_user_authenticated(self):
        """
        Checks that an authenticated user can access the password
        change form.
        """
        self.client.login(
            username='test_user',
            password='test_pass'
        )

        # HTTP Response
        response = self.client.get(path=self.PASSWORD_CHANGE_URL)

        # Checks that an HTTP 200 (OK) status code is returned.
        self.assertEqual(
            first=response.status_code,
            second=200
        )

        # Checks that the view sends a form of the correct class in the context.
        self.assertIsInstance(
            obj=response.context['form'],
            cls=PasswordChangeForm
        )

        # Checks that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='registration/password_change_form.html'
        )

    def test_password_change_form_submit_user_not_authenticated(self):
        """
        Checks that a not-authenticated user cannot send data for password
        change and is redirected to the login page.
        """
        form_data = {
            'password1': 'NewPass123',
            'password2': 'NewPass123'
        }

        # HTTP Response
        response = self.client.post(
            path=self.PASSWORD_CHANGE_URL,
            data=form_data,
            follow=True
        )

        # Checks that there is a redirect to the login page
        redirect_url = f'{self.LOGIN_URL}?next={self.PASSWORD_CHANGE_URL}'
        self.assertRedirects(
            response=response,
            expected_url=redirect_url,
            status_code=302,
            target_status_code=200
        )

        # Checks that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='registration/login.html'
        )

    def test_password_change_form_submit_user_authenticated(self):
        """
        Check that an authenticated user can send data for password change.
        """
        self.client.login(
            username='test_user',
            password='test_pass'
        )

        form_data = {
            'old_password': 'test_pass',
            'new_password1': 'New_Pass_123',
            'new_password2': 'New_Pass_123'
        }

        # HTTP Response
        response = self.client.post(
            path=self.PASSWORD_CHANGE_URL,
            data=form_data,
            follow=True
        )

        # Checks that an HTTP 200 (OK) status code is returned
        self.assertEqual(
            first=response.status_code,
            second=200
        )

        # Checks that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='registration/password_change_done.html'
        )
        
    def test_invalid_password_change_form_submit_user_authenticated(self):
        """
        Check that an authenticated user cannot send invalid
        data for password change.
        """
        self.client.login(
            username='test_user',
            password='test_pass'
        )

        form_data = {
            'old_password': 'wrong_old_password',
            'new_password1': 'New_Pass_123',
            'new_password2': 'New_Pass_123'
        }

        # HTTP Response
        response = self.client.post(
            path=self.PASSWORD_CHANGE_URL,
            data=form_data,
            follow=True
        )

        # Checks that an HTTP 200 (OK) status code is returned
        self.assertEqual(
            first=response.status_code,
            second=200
        )

        # Checks that the form has errors
        self.assertTrue(
            expr=response.context['form'].errors
        )

        # Checks that the form has an error in the 'old_password' field
        self.assertIn(
            member='old_password',
            container=response.context['form'].errors
        )

        # Checks that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='registration/password_change_form.html'
        )
