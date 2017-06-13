# COMENTARIOS
#
# O ideal eh que tenhamos apenas um assert para cada funcao
# cada funcao que comeca com 'test_' eh chamada de test method
# cada funcao dentro de uma classe eh chamada de instancia


from django.test import TestCase

class HomeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/')

    def test_get(self):
        """ GET / must return status code 200 """
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """ Must use index.html """
        self.assertTemplateUsed(self.response, 'index.html')

    def test_subscription_link(self):
        self.assertContains(self.response, 'href="/inscricao/"')