from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class MessageApiTestCase(APITestCase):
    def setUp(self):
        self.test_user1 = User.objects.create(username='u1')
        self.test_user1.set_password('u1')
        self.test_user1.save()
        self.test_user2 = User.objects.create(username='u2', password='u2')
        self.test_user2.set_password('u2')
        self.test_user2.save()
        self.test_user3 = User.objects.create(username='u3', password='u3')
        self.test_user3.set_password('u3')
        self.test_user3.save()

    def test_list_request(self):
        self.login_user1()
        response = self.client.get(reverse('message-api-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logout()

    def test_send_message_unauth(self):
        url = reverse('message-api-list')
        message = {'recipient': 'u1', 'body': 'No auth!'}
        response = self.client.post(url, message, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_send_message(self):
        self.login_user1()
        url = reverse('message-api-list')
        message = {'recipient': 'u2', 'body': 'hello'}
        response = self.client.post(url, message, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.logout()

    def test_read_message(self):
        self.login_user1()
        url = reverse('message-api-list')
        message = {'recipient': 'u2', 'body': 'hello'}
        response = self.client.post(url, message, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.logout()
        # Change user
        self.login_user2()
        url = reverse('message-api-detail', kwargs={'pk': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['body'], 'hello')
        self.logout()
        # Change to another user (not in conversation)
        self.login_user3()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.logout()

    def login_user1(self):
        self.login('u1', 'u1')

    def login_user2(self):
        self.login('u2', 'u2')

    def login_user3(self):
        self.login('u3', 'u3')

    def login(self, username, password):
        self.assertTrue(self.client.login(username=username, password=password))

    def logout(self):
        self.client.logout()
