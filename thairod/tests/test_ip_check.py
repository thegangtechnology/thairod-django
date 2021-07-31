from django.urls import reverse

from thairod.utils.test_util import APITestCase


class TestIPCheck(APITestCase):
    def test_ip_check(self):
        res = self.client.get(reverse('ip-check'))
        self.assertTrue('ip' in res.data)
        self.assertTrue(len(res.data['ip']) >= 7)
