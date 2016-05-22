import unittest

from django.core.exceptions import ObjectDoesNotExist

from cms import api
from cms.models import Page

from .base import BaseRelationsTest

from testapp.models import (
    SimplePluginModel,
    ExplicitFKCopyPlugin,
    ImplicitFKCopyPlugin,
    ModelWithRelations1,
    ExplicitM2MCopyPlugin,
    ExplicitPluginFKCopyPlugin,
    PluginWithRelations1,
)


class TestFKFromModel(BaseRelationsTest):

    def test_plugin_has_autocopy_draft_property(self):
        plugin = self.add_plugin('SimplePlugin', self.page1)
        try:
            plugin.autocopy_draft
        except AttributeError:
            self.fail('Plugin has no property `draft`.')

    def skip_test_old_instance_reachable_after_copy(self):
        old_plugin = self.add_plugin('SimplePlugin', self.page1)
        new_base_plugin = old_plugin.simplepluginmodel.copy_plugin(
            self.placeholder(self.page1),
            self.FIRST_LANG,
            {}
        )
        new_plugin = SimplePluginModel.objects.get(pk=new_base_plugin.pk)
        self.assertEqual(
            old_plugin.pk,
            new_plugin.draft.pk
        )

    def test_explicit_autocopy_fields_found(self):
        self.assertListEqual(
            ExplicitFKCopyPlugin().get_autocopy_fields(),
            ['modelwithrelations1_set']
        )

    ##

    def test_reverse_foreign_key_copied(self):
        plugin = self.add_plugin('FKPlugin', self.page1)
        model = ModelWithRelations1.objects.create(
            fk1=plugin,
            title='asdf'
        )
        self.publish_page(self.page1)
        page_copy = Page.objects.public().get(
            title_set__title=self.page1.get_title(self.FIRST_LANG)
        )
        plugin_copy = ExplicitFKCopyPlugin.objects.get(placeholder__page=page_copy)
        self.assertSequenceEqual(
            list(plugin_copy.explicitfkcopyplugin.modelwithrelations1_set.values_list('title', flat=True)),
            list(plugin.modelwithrelations1_set.values_list('title', flat=True))
        )

    def test_many_to_many_copied(self):
        plugin = self.add_plugin('M2MPlugin', self.page1)
        model = ModelWithRelations1.objects.create(
            title='qwerty'
        )
        model.m2m1.add(plugin)
        page_copy = self.publish_page(self.page1)
        plugin_copy = ExplicitM2MCopyPlugin.objects.get(placeholder__page=page_copy)
        self.assertSequenceEqual(
            list(plugin_copy.explicitm2mcopyplugin.modelwithrelations1_set.values_list('title', flat=True)),
            list(plugin.modelwithrelations1_set.values_list('title', flat=True))
        )



class FKBetweenPluginsTestCase(BaseRelationsTest):

    @property
    def target_page(self):
        return self.page1

    @property
    def origin_page(self):
        return self.page2

    def get_target_plugin(self, page):
        return ExplicitPluginFKCopyPlugin.objects.get(placeholder__page=page)

    def get_origin_plugin(self, page):
        return PluginWithRelations1.objects.get(placeholder__page=page)

    def setUp(self):
        super(FKBetweenPluginsTestCase, self).setUp()
        self.fk_target = self.add_plugin('PluginFKPlugin', self.target_page)
        self.fk_target = ExplicitPluginFKCopyPlugin.objects.get(pk=self.fk_target.pk)
        self.fk_origin = self.add_plugin('PluginWithRelations', self.origin_page, title='zxcvb', fk1=self.fk_target)
        # Fetch new from database to see reverse foreign key:
        self.fk_target = ExplicitPluginFKCopyPlugin.objects.get(pk=self.fk_target.pk)

    def test_public_origin_has_correct_class(self):
        draft_origin = PluginWithRelations1.objects.get()
        self.publish_page(self.origin_page)
        self.assertEqual(
            draft_origin.public.__class__.__name__,
            'PluginWithRelations1'
        )

    def ttest_relation_survives_origin_publishing(self):
        target_before = self.fk_origin.fk1
        self.publish_page(self.origin_page)
        target_after = self.fk_origin.fk1
        self.assertEqual(
            target_after,
            target_before
        )

    def ttest_relation_survives_target_publishing(self):
        target_before = self.fk_origin.fk1
        self.publish_page(self.target_page)
        target_after = self.fk_origin.fk1
        self.assertEqual(
            target_after,
            target_before
        )

    def ttest_published_origin_has_no_relation_with_draft(self):
        public_origin_page = self.publish_page(self.origin_page)
        public_origin_plugin = self.get_origin_plugin(public_origin_page)
        with self.assertRaises(ObjectDoesNotExist):
            public_origin_plugin.fk1

    def ttest_published_target_has_no_relation_with_draft(self):
        public_target_page = self.publish_page(self.target_page)
        public_target_plugin = self.get_target_plugin(public_target_page)
        with self.assertRaises(ObjectDoesNotExist):
            public_target_plugin.pluginwithrelations1

    def test_relation_between_published_when_origin_published_first(self):
        public_origin_page = self.publish_page(self.origin_page)
        public_target_page = self.publish_page(self.target_page)
        public_origin_plugin = self.get_origin_plugin(public_origin_page)
        public_target_plugin = self.get_target_plugin(public_target_page)
        self.assertEqual(
            public_target_plugin.pluginwithrelations1_set.get(),
            public_origin_plugin
        )

    def test_relation_between_published_when_target_published_first(self):
        public_target_page = self.publish_page(self.target_page)
        public_origin_page = self.publish_page(self.origin_page)
        public_origin_plugin = self.get_origin_plugin(public_origin_page)
        public_target_plugin = self.get_target_plugin(public_target_page)
        print self.get_target_plugin(self.target_page).pluginwithrelations1_set.all()
        print public_target_plugin.pluginwithrelations1_set.all()
        self.assertEqual(
            public_target_plugin.pluginwithrelations1_set.get(),
            public_origin_plugin
        )
