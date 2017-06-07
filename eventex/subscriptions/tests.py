from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm

class SubscribeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/inscricao/')

    def test_get(self):
        """Get /inscricao/ must return status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """Html must contain input tags"""
        self.assertContains(self.resp, '<form')             #UM FORM NO HTML
        self.assertContains(self.resp, '<input', 6)         #5 INPUTS NESSE FORMULARIO
        self.assertContains(self.resp, 'type="text"', 3)    #3 DSSES 5 INPUTS SENDO TEXTO
        self.assertContains(self.resp, 'type="email"')      #UM DELES EMAIL
        self.assertContains(self.resp, 'type="submit"')     #UM BOTAO DE SUBMIT

    def test_csrf(self):
        """Html must contain CSRF"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """Form must have 4 fields"""
        form = self.resp.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))

class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name='Paulo Bueno Bruno', cpf='36926776857',
                    email='paulob.bruno@gmail.com', phone='11-98305-1993')
        self.resp = self.client.post('/inscricao/', data)

    def test_post(self):
        """Valid POST must redirect to /inscricao/"""
        self.assertEqual(302, self.resp.status_code)

    def test_send_subscribe_email(self):
        """Email field must contain value"""
        # no processo de requisicao, o django nao manda emails, mas guarda quantos foram enviados
        self.assertEqual(1, len(mail.outbox))

    def test_subsciption_email_subject(self):
        """Subject must contain value"""
        email = mail.outbox[0]
        expect = 'Confirmacao de Inscricao'
        self.assertEqual(expect, email.subject)

    def test_subscription_email_from(self):
        """Verify email from"""
        email = mail.outbox[0]
        expected = 'contato@eventex.com.br'
        self.assertEqual(expected, email.from_email)

    def test_subscription_email_to(self):
        """Verify emails to"""
        email = mail.outbox[0]
        expected = ['contato@eventex.com.br', 'paulob.bruno@gmail.com']
        self.assertEqual(expected, email.to)

    def test_subscription_email_body(self):
        email = mail.outbox[0]

        self.assertIn('Paulo Bueno Bruno', email.body)
        self.assertIn('36926776857', email.body)
        self.assertIn('paulob.bruno@gmail.com', email.body)
        self.assertIn('11-98305-1993', email.body)

class SubscribeInvalidPost(TestCase):
    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})

    def test_post(self):
        """Invalid post should not redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)


class SubscribeSuccessMessage(TestCase):
    def test_message(self):
        data = dict(name='Paulo Bueno Bruno', cpf='36521452145',
                    email='paulob.bruno@gmail.com', phone='896547854')

        response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(response, 'Inscrição realizada com sucesso!')