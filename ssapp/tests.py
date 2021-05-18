from django.test import TestCase
import datetime
from django.db import models
from .models import *
from django.urls import reverse


class UserOpenPage(TestCase):
    def test_open_index(self):
        # Test Opening an index page
        response = self.client.get(reverse('ssapp:index'))
        self.assertContains(response, "Schedule Schemer")

    def test_open_dashboard_without_signin(self):
        response = self.client.get(reverse('ssapp:dashboard'), follow=True)
        self.assertRedirects(response, f"{reverse('login')}?next=%2Fdashboard" , status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        self.assertContains(response, "Sign in")


    def test_open_schedule_page_without_signin(self):
        response = self.client.get(reverse('ssapp:dashboard'))
        self.assertEqual(response.status_code, 302)

class UserSignupTest(TestCase):
    def test_signup_with_all_information(self):
        """
        This testing to see whether the signing up works when all the information is provided
        """
        response = self.client.post(reverse('ssapp:signup'), {"username": "Andreas", "password1": "Asd,car15", "password2": "Asd,car15", "email": "andreas@gmail.com", "first_name": "Andreas", "last_name": "Mambu", "major": "Information Technology" }, follow=True)
        self.assertRedirects(response, reverse('ssapp:signup') , status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

 
