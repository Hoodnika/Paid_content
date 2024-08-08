from django.test import TestCase, LiveServerTestCase, TransactionTestCase
from django.urls import reverse

from config.settings import SUPPORT_EMAIL
from main_app.models import Publication, Subscription
from user_app.models import User


class PublicationListViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            phone_number=88005553535,
            email='hoodnika213@yandex.ru',
            first_name='Test',
            last_name='Testov'
        )
        self.user.set_password('testpassword')
        self.publication1 = Publication.objects.create(title='Publication 1', owner=self.user, slug='publication-1')
        self.publication2 = Publication.objects.create(title='Publication 2', owner=self.user, slug='publication-2')
        self.publication3 = Publication.objects.create(title='Publication 3', owner=self.user, slug='publication-3')

    def test_get_queryset_without_subscription(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('main_app:main'))
        self.assertEqual(list(response.context['publications']),
                         [self.publication3, self.publication2, self.publication1])

    def test_get_context_data_without_subscription(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('main_app:main'))
        self.assertEqual(response.context['support_email'], SUPPORT_EMAIL)
        self.assertEqual(response.context['carousel_middle_text'],
                         'Оформите подписку, для доступа к большей библиотеке публикаций')
        self.assertFalse(response.context['carousel_middle_text_hide'])


class PublicationSearchViewTestCase(LiveServerTestCase):

    def setUp(self):
        self.user = User.objects.create(
            phone_number=88005553535,
            email='hoodnika213@yandex.ru',
            first_name='Test',
            last_name='Testov'
        )
        self.user.set_password('testpassword')
        self.publication1 = Publication.objects.create(title='Publication 1', owner=self.user, slug='publication-1')
        self.publication2 = Publication.objects.create(title='Publication 2', owner=self.user, slug='publication-2')
        self.publication3 = Publication.objects.create(title='Publication 3', owner=self.user, slug='publication-3')

    def test_get_queryset_without_subscription(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('main_app:search') + '?q=Publication')
        self.assertEqual(list(response.context['publications']),
                         [self.publication3, self.publication2, self.publication1])
        self.assertEqual(response.context['p'], 'Publication')
        self.assertEqual(response.context['support_email'], SUPPORT_EMAIL)


class PublicationAuthorListViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            phone_number=88005553535,
            email='hoodnika213@yandex.ru',
            first_name='Test',
            last_name='Testov'
        )
        self.author = User.objects.create(
            phone_number=1111111111,
            email='test@yandex.ru',
            first_name='NeTest',
            last_name='NeTestov'
        )
        self.publication1 = Publication.objects.create(title='Publication 1', owner=self.author, slug='publication-1')
        self.publication2 = Publication.objects.create(title='Publication 2', owner=self.user, slug='publication-2')
        self.publication3 = Publication.objects.create(title='Publication 3', owner=self.author, slug='publication-3')
        self.client.force_login(user=self.user)

    def test_get_queryset(self):
        response = self.client.get(reverse('main_app:publication_owner', kwargs={'pk': self.author.pk}))
        self.assertEqual(list(response.context['publications']), [self.publication3, self.publication1])

    def test_get_context_data(self):
        response = self.client.get(reverse('main_app:publication_owner', kwargs={'pk': self.author.pk}))
        self.assertEqual(response.context['support_email'], SUPPORT_EMAIL)


class PublicationDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            phone_number=88005553535,
            email='hoodnika213@yandex.ru',
            first_name='Test',
            last_name='Testov'
        )
        self.publication = Publication.objects.create(title='Test Publication', content='Test content', owner=self.user,
                                                      slug='test-publication')

    def test_get_publication_detail(self):
        url = reverse('main_app:publication_detail', kwargs={'slug': self.publication.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.publication.title)
        self.assertContains(response, self.publication.content)


class PublicationCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            phone_number=88005553535,
            email='hoodnika213@yandex.ru',
            first_name='Test',
            last_name='Testov'
        )
        self.client.force_login(user=self.user)

    def test_create_publication(self):
        form_data = {
            'title': 'Test Publication',
            'content': 'Test content',
            'slug': 'test publication',
            'description': 'Test description'
        }
        url = reverse('main_app:publication_create')
        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertEqual(Publication.objects.count(), 1)
        publication = Publication.objects.first()
        self.assertEqual(publication.title, form_data['title'])
        self.assertEqual(publication.content, form_data['content'])
        self.assertEqual(publication.owner, self.user)


class PublicationUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            phone_number=88005553535,
            email='hoodnika213@yandex.ru',
            first_name='Test',
            last_name='Testov'
        )
        self.client.force_login(user=self.user)
        self.publication = Publication.objects.create(title='Test Publication', content='Test content', owner=self.user, slug='test_publication')

    def test_update_publication(self):
        form_data = {
            'title': 'Updated Test Publication',
            'content': 'Updated content',
            'btn_save': 'save'
        }
        url = reverse('main_app:publication_update', kwargs={'pk': self.publication.pk})
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 200)


class PublicationDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            phone_number=88005553535,
            email='hoodnika213@yandex.ru',
            first_name='Test',
            last_name='Testov'
        )
        self.client.force_login(user=self.user)
        self.publication = Publication.objects.create(title='Test Publication', content='Test content', owner=self.user, slug='test_publication')

    def test_delete_publication(self):
        url = reverse('main_app:publication_delete', kwargs={'pk': self.publication.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertEqual(Publication.objects.count(), 0)
