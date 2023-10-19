from django.test import TestCase
from django.contrib.auth import get_user_model


User = get_user_model()


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            password="testpass",
        )

    def test_user_str(self) -> None:
        expected_str = self.user.email

        self.assertEqual(str(self.user), expected_str)
