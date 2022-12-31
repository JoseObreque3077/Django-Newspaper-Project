from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from django.test import TestCase
from django.urls import reverse

from accounts.forms import CustomUserCreationForm


class SignupPageTests(TestCase):
    """
    Unit test case for the 'SignUpView' class that handles user signup in the
    'Accounts' application. It tests the signup form rendering, the submission
    of the form, and the redirection after successful form submission.
    """
    # URLs
    SIGNUP_URL = reverse('signup')
    LOGIN_URL = reverse('login')

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
            email='test@example.net',
            age=18
        )
        # Use of non-encrypted password
        cls.user.set_password('test_pass')
        cls.user.save()

    def test_signup_form_render_user_authenticated(self):
        """
        Checks that an authenticated user cannot access the signup form.
        """
        self.client.login(
            username='test_user',
            password='test_pass'
        )

        # HTTP Response
        response = self.client.get(path=self.SIGNUP_URL)

        # Checks that an HTTP 403: Forbidden status code is returned.
        self.assertEqual(
            first=response.status_code,
            second=403
        )

    def test_signup_form_render_user_not_authenticated(self):
        """
        Checks that a non-authenticated user can access the registration form.
        """
        # HTTP Response
        response = self.client.get(path=self.SIGNUP_URL)

        # Checks that an HTTP 200 (OK) status code is returned.
        self.assertEqual(
            first=response.status_code,
            second=200
        )

        # Verify that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='registration/signup.html'
        )

        # Checks that the view sends a form of the correct class in the context.
        self.assertIsInstance(
            obj=response.context['form'],
            cls=CustomUserCreationForm
        )

    def test_signup_form_submit_user_authenticated(self):
        """
        Checks that an authenticated user cannot submit the user signup form.
        """
        self.client.login(
            username='test_user',
            password='test_pass'
        )

        # New user data
        form_data = {
            'username': 'test_user_2',
            'email': 'test_2@example.com',
            'age': 21,
            'password1': 'user12345',
            'password2': 'user12345'
        }

        # HTTP Response
        response = self.client.post(
            path=self.SIGNUP_URL,
            data=form_data
        )

        # Checks that an HTTP 403 (Forbidden) status code is returned
        self.assertEqual(
            first=response.status_code,
            second=403
        )

    def test_signup_form_submit_user_not_authenticated(self):
        """
        Checks that a non-authenticated user can submit the user signup form.
        """
        # Custom user model used by this project
        user_model = get_user_model()

        # New user data
        form_data = {
            'username': 'test_user_2',
            'email': 'test_2@example.com',
            'age': 21,
            'password1': 'user12345',
            'password2': 'user12345'
        }

        # HTTP Response
        response = self.client.post(
            path=self.SIGNUP_URL,
            data=form_data,
            follow=True
        )

        # Checks that the form submit adds a new user to the test database.
        self.assertEqual(
            first=user_model.objects.count(),
            second=2
        )

        # Checks if the new user has the correct info.
        new_user = user_model.objects.get(pk=2)
        new_user_partial_data = model_to_dict(
            instance=new_user,
            fields=['username', 'email', 'age']
        )
        self.assertEqual(
            first={key: form_data[key] for key in ['username', 'email', 'age']},
            second=new_user_partial_data
        )

        # Verifies that there is a redirect to the login page after
        # the new user is registered.
        self.assertRedirects(
            response=response,
            expected_url=self.LOGIN_URL,
            status_code=302,
            target_status_code=200
        )

        # Verify that the view renders the correct template.
        self.assertTemplateUsed(
            response=response,
            template_name='registration/login.html'
        )
