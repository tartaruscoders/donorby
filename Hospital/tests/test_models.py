from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTestCase(TestCase):
    
    # camelcase because of builtin unittesting
    def setUp(self):
        user_a = User(username='test_account', email='test@example.com')
        user_a_pw = ('@test_password')
        self.user_a_pw = user_a_pw
        user_a.is_staff = True
        user_a.save()
        user_a.set_password(user_a_pw)
        self.user_a = user_a

    def test_user_exists(self):
        user_count = User.objects.all().count()
        # asserEqual is built in the Testcase
        self.assertEquals(user_count, 1)

    def test_user_password(self):
        self.assertTrue(
            self.user_a.check_password(self.user_a_pw)
        )
    