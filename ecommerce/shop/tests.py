from django.test import TestCase
from django.urls import reverse
from .models import Product

class ShopTests(TestCase):
    def setUp(self):
        self.p1 = Product.objects.create(name='Kalem', price='2.50', stock=10)
        self.p2 = Product.objects.create(name='Defter', price='15.00', stock=5)

    def test_product_list(self):
        resp = self.client.get(reverse('product_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Kalem')

    def test_add_to_cart_and_checkout(self):
        add_url = reverse('add_to_cart', args=[self.p1.id])
        resp = self.client.post(add_url, {'quantity': 2}, follow=True)
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(reverse('cart'))
        self.assertContains(resp, 'Kalem')
        resp = self.client.post(reverse('checkout'))
        self.assertEqual(resp.status_code, 200)
        self.assertJSONEqual(resp.content, {'status': 'success', 'message': 'Payment mocked, order placed'})
