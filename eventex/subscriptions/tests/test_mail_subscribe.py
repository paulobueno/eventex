from django.core import mail
from django.test import TestCase


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Paulo Bueno Bruno', cpf='36926776857',
                    email='paulob.bruno@gmail.com', phone='11-98305-1993')
        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_subsciption_email_subject(self):
        """Subject must contain value"""
        expect = 'Confirmacao de Inscricao'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        """Verify email from"""
        expected = 'contato@eventex.com.br'
        self.assertEqual(expected, self.email.from_email)

    def test_subscription_email_to(self):
        """Verify emails to"""
        expected = ['contato@eventex.com.br', 'paulob.bruno@gmail.com']
        self.assertEqual(expected, self.email.to)

    def test_subscription_email_body(self):

        contents = [
            'Paulo Bueno Bruno',
            '36926776857',
            'paulob.bruno@gmail.com',
            '11-98305-1993',
        ]

        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)