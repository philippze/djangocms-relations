from cms import api
from cms.models import Page

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from icecream import models


class BaseRelationsTestCase(TestCase):

    LANGUAGE = 'en'
    PASSWORD = 'pw'
    TEMPLATE = 'cms_page.html'

    def setUp(self):
        self.create_superuser()
        self.create_pages()

    def tearDown(self):
        Page.objects.all().delete()

    def create_superuser(self):
        self.superuser = User.objects.create_superuser(
            'superuser',
            'superuser@example.com',
            self.PASSWORD
        )

    def create_pages(self):
        self.flavors_page = api.create_page(
            'Flavors',
            self.TEMPLATE,
            self.LANGUAGE
        )
        self.sundeas_page = api.create_page(
            'Sundeas',
            self.TEMPLATE,
            self.LANGUAGE
        )
        self.pictures_page = api.create_page(
            'Pictures',
            self.TEMPLATE,
            self.LANGUAGE
        )


class FkFromModelToPluginTestCase(BaseRelationsTestCase):

    CHOCOLATE = 'Chocolate'
    JOHN = 'John'

    def test_relation_remains(self):
        self._test_relation(publisher_is_draft=True)

    def test_relation_copied(self):
        self._test_relation(publisher_is_draft=False)

    def _test_relation(self, publisher_is_draft):
        placeholder = self.flavors_page.placeholders.get(slot='body')
        chocolate_plugin = api.add_plugin(
            placeholder,
            'FlavorPlugin',
            self.LANGUAGE,
            name=self.CHOCOLATE
        )
        chocolate = chocolate_plugin.flavor
        John = models.Photographer.objects.create(
            name=self.JOHN,
            favorite=chocolate
        )
        api.publish_page(
            self.flavors_page,
            self.superuser,
            self.LANGUAGE
        )
        chocolate_of_interest = models.Flavor.objects.get(
            name=self.CHOCOLATE,
            placeholder__page__publisher_is_draft=publisher_is_draft
        )
        self.assertEqual(
            chocolate_of_interest.fans.get().name,
            self.JOHN
        )


class M2mFromPluginToModelTestCase(BaseRelationsTestCase):

    SPAGHETTI_ICE_CREAM = 'Spaghetti Ice Cream'
    STRAWBERRY_SAUCE = 'Strawberry'

    def test_relation_remains(self):
        self._test_relation(publisher_is_draft=True)

    def test_relation_copied(self):
        self._test_relation(publisher_is_draft=False)

    def _test_relation(self, publisher_is_draft):
        placeholder = self.sundeas_page.placeholders.get(slot='body')
        strawberry_sauce = models.Sauce.objects.create(
            name=self.STRAWBERRY_SAUCE
        )
        spaghetti_ice_cream_plugin = api.add_plugin(
            placeholder,
            'SundeaPlugin',
            self.LANGUAGE,
            name=self.SPAGHETTI_ICE_CREAM
        )
        spaghetti_ice_cream = spaghetti_ice_cream_plugin.sundea
        spaghetti_ice_cream.sauces.add(strawberry_sauce)
        api.publish_page(
            self.sundeas_page,
            self.superuser,
            self.LANGUAGE
        )
        spaghetti_ice_cream_of_interest = models.Sundea.objects.get(
            name=self.SPAGHETTI_ICE_CREAM,
            placeholder__page__publisher_is_draft=publisher_is_draft
        )
        self.assertEqual(
            spaghetti_ice_cream_of_interest.sauces.get().name,
            self.STRAWBERRY_SAUCE
        )


class FkFromPluginToPluginTestCase(BaseRelationsTestCase):

    COVER_PICTURE = 'Cover Picture'
    BANANA_SPLIT = 'Banana Split'

    def setUp(self):
        super(FkFromPluginToPluginTestCase, self).setUp()
        self._create_plugins()

    def test_relation_remains(self):
        api.publish_page(
            self.sundeas_page,
            self.superuser,
            self.LANGUAGE
        )
        banana_split_of_interest = models.Sundea.objects.get(
            name=self.BANANA_SPLIT,
            placeholder__page__publisher_is_draft=True
        )
        self.assertEqual(
            banana_split_of_interest.pictures.get().name,
            self.COVER_PICTURE
        )

    def test_relation_copied(self):
        api.publish_page(
            self.sundeas_page,
            self.superuser,
            self.LANGUAGE
        )
        banana_split_of_interest = models.Sundea.objects.get(
            name=self.BANANA_SPLIT,
            placeholder__page__publisher_is_draft=True
        )
        self.assertEqual(
            banana_split_of_interest.pictures.get().name,
            self.COVER_PICTURE
        )

    def _create_plugins(self):
        pictures_placeholder = self.pictures_page.placeholders.get(slot='body')
        sundeas_placeholder = self.sundeas_page.placeholders.get(slot='body')
        banana_split_plugin = api.add_plugin(
            sundeas_placeholder,
            'SundeaPlugin',
            self.LANGUAGE,
            name=self.BANANA_SPLIT
        )
        banana_split = banana_split_plugin.sundea
        cover_picture_plugin = api.add_plugin(
            pictures_placeholder,
            'PicturePlugin',
            self.LANGUAGE,
            name=self.COVER_PICTURE,
            sundea=banana_split
        )
        self.cover_picture = cover_picture_plugin.picture


class M2mFromPluginToPluginTestCase(BaseRelationsTestCase):

    BANANA = 'Banana'
    BANANA_SPLIT = 'Banana Split'

    def setUp(self):
        super(M2mFromPluginToPluginTestCase, self).setUp()
        self._create_plugins()

    def test_relation_remains_when_origin_published(self):
        api.publish_page(
            self.sundeas_page,
            self.superuser,
            self.LANGUAGE
        )
        banana_split_of_interest = models.Sundea.objects.get(
            name=self.BANANA_SPLIT,
            placeholder__page__publisher_is_draft=True
        )
        self.assertEqual(
            banana_split_of_interest.flavors.get().name,
            self.BANANA
        )

    def test_relation_not_published_when_target_not_public(self):
        api.publish_page(
            self.sundeas_page,
            self.superuser,
            self.LANGUAGE
        )
        banana_split_of_interest = models.Sundea.objects.get(
            name=self.BANANA_SPLIT,
            placeholder__page__publisher_is_draft=False
        )
        self.assertRaises(
            ObjectDoesNotExist,
            banana_split_of_interest.flavors.get
        )

    def test_relation_not_published_when_origin_not_public(self):
        api.publish_page(
            self.flavors_page,
            self.superuser,
            self.LANGUAGE
        )
        banana_of_interest = models.Flavor.objects.get(
            name=self.BANANA,
            placeholder__page__publisher_is_draft=False
        )
        self.assertRaises(
            ObjectDoesNotExist,
            banana_of_interest.sundeas.get
        )

    def test_relation_copied_when_first_origin_and_then_target_published(self):
        api.publish_page(
            self.sundeas_page,
            self.superuser,
            self.LANGUAGE
        )
        api.publish_page(
            self.flavors_page,
            self.superuser,
            self.LANGUAGE
        )
        banana_split_of_interest = models.Sundea.objects.get(
            name=self.BANANA_SPLIT,
            placeholder__page__publisher_is_draft=False
        )
        self.assertEqual(
            banana_split_of_interest.flavors.get().name,
            self.BANANA
        )


    def _create_plugins(self):
        flavors_placeholder = self.flavors_page.placeholders.get(slot='body')
        sundeas_placeholder = self.sundeas_page.placeholders.get(slot='body')
        banana_plugin = api.add_plugin(
            flavors_placeholder,
            'FlavorPlugin',
            self.LANGUAGE,
            name=self.BANANA
        )
        banana = banana_plugin.flavor
        banana_split_plugin = api.add_plugin(
            sundeas_placeholder,
            'SundeaPlugin',
            self.LANGUAGE,
            name=self.BANANA_SPLIT
        )
        banana_split = banana_split_plugin.sundea
        banana_split.flavors.add(banana)
