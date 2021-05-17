from django.test import TestCase
import datetime
from django.db import models
from .models import *
from django.urls import reverse

class userSignupTest(TestCase):
    def test_signup_with_all_information(self):
        """
        This testing to see whether the signing up works when all the information is provided
        """
        response = self.client.post(reverse('ssapp:signup'), {"username": "Andreas", "password1": "Asd,car15", "password2": "Asd,car15", "email": "andreas@gmail.com", "first_name": "Andreas", "last_name": "Mambu", "major": "Information Technology" }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your account has been created successfully, please login!")

    def test_signup_bypass_username(self):
        """
        This testing is checking the response of the backend when the required part of the username is bypass. To see whether the system will
        accept with the blank username or not.
        """
        response = self.client.post(reverse('ssapp:signup'), {"username": "", "password1": "Asd,car15", "password2": "Asd,car15", "email": "andreas@gmail.com", "first_name": "Andreas", "last_name": "Mambu", "major": "Information Technology" }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContaints(response, "Please select an appropriate information"   )

    def test_signup_bypass_password(self):
        """
        Like the previous test, but this one is to check the password.
        """
        response = self.client.post(reverse('ssapp:signup'), {"username": "Andreas", "password1": "", "password2": "Asd,car15", "email": "andreas@gmail.com", "first_name": "Andreas", "last_name": "Mambu", "major": "Information Technology"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContaints(response, "Please select an appropriate information")

    def test_signup_bypass_confirm_password(self):
        """
        Like the previous test, but this one is to check the confirm password.
        """
        response = self.client.post(reverse('ssapp:signup'), {"username": "Andreas", "password1": "Asd,car15", "password2": "", "email": "andreas@gmail.com", "first_name": "Andreas", "last_name": "Mambu", "major": "Information Technology"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContaints(response, "Please select an appropriate information")

    def test_signup_bypass_email(self):
        """
        Like the previous test, but this one is to check the email.
        """
        response = self.client.post(reverse('ssapp:signup'), {"username": "Andreas", "password1": "Asd,car15", "password2": "Asd,car15", "email": "", "first_name": "Andreas", "last_name": "Mambu", "major": "Information Technology"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContaints(response, "Please select an appropriate information")

    def test_signup_bypass_first_name(self):
        """
        Like the previous test, but this one is to check the first name.
        """
        response = self.client.post(reverse('ssapp:signup'), {"username": "Andreas", "password1": "Asd,car15", "password2": "Asd,car15", "email": "andreas@gmail.com", "first_name": "", "last_name": "Mambu", "major": "Information Technology"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContaints(response, "Please select an appropriate information")

    def test_signup_bypass_last_name(self):
        """
        Like the previous test, but this one is to check the last name.
        """
        response = self.client.post(reverse('ssapp:signup'), {"username": "Andreas", "password1": "Asd,car15", "password2": "Asd,car15", "email": "andreas@gmail.com", "first_name": "Andreas", "last_name": "", "major": "Information Technology"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContaints(response, "Please select an appropriate information")

    def test_signup_bypass_major(self):
        """
        Like the previous test, but this one is to check the major.
        """
        response = self.client.post(reverse('ssapp:signup'), {"username": "Andreas", "password1": "Asd,car15", "password2": "Asd,car15", "email": "andreas@gmail.com", "first_name": "Andreas", "last_name": "Mambu", "major": ""}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContaints(response, "Please select an appropriate information")

    def test_signup_bypass_all_information(self):
        """
        Like the previous test, but this one is bypassing all information form.
        """
        response = self.client.post(reverse('ssapp:signup'), {"username": "", "password1": "", "password2": "", "email": "", "first_name": "", "last_name": "", "major": ""}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContaints(response, "Please select an appropriate information")

class userUpdateProfileTest(TestCase):
    def test_update_with_change_first_name(self):
        """
        This testing is to make sure change the first name works well.
        """
        response = self.client.post(reverse('ssapp:signup'), {"username": "Andreas", "password1": "Asd,car15", "password2": "Asd,car15", "email": "andreas@gmail.com", "first_name": "Andreas", "last_name": "Mambu", "major": "Information Technology"}, follow=True)
        response = self.client.post(reverse('ssapp:update'), {"fname": "Christian", "lname": "Mambu", "major": "Information Technology"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ssapp.objects.filter(pk=))

    def test_update_with_change_last_name(self):
        """
        This testing is to make sure change the first name works well.
        """
        response = self.client.post(reverse('ssapp:signup'), {"username": "Andreas", "password1": "Asd,car15", "password2": "Asd,car15", "email": "andreas@gmail.com", "first_name": "Andreas", "last_name": "Mambu", "major": "Information Technology"}, follow=True)
        response = self.client.post(reverse('ssapp:update'), {"fname": "Andreas", "lname": "Christian", "major": "Information Technology"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ssapp.objects.filter(pk=))

    def test_update_with_change_major(self):
        """
        This testing is to make sure change the first name works well.
        """
        response = self.client.post(reverse('ssapp:signup'), {"username": "Andreas", "password1": "Asd,car15", "password2": "Asd,car15", "email": "andreas@gmail.com", "first_name": "Andreas", "last_name": "Mambu", "major": "Information Technology"}, follow=True)
        response = self.client.post(reverse('ssapp:update'), {"fname": "Andreas", "lname": "Mambu", "major": "Science"}, follow=True)
        self.assertEqual(response.status_code, 200)
