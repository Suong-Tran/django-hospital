from audioop import reverse
from django.test import TestCase
from django.shortcuts import reverse

class LandingPageTest(TestCase):
    def test_get(self):
        response = self.client.get(reverse("landing-page"))
        #print(response.status_code)
        #compare with the status code, if not 200, give error
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, "landing.html")
   