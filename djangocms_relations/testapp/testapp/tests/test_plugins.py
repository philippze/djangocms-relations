import unittest

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
)


class TestFKFromModel(BaseRelationsTest):

    def test_plugin_has_old_instance_property(self):
        plugin = self.add_plugin('SimplePlugin', self.page1)
        try:
            plugin.original_instance
        except AttributeError:
            self.fail('Plugin has no property `old_instance`.')

    def test_old_instance_reachable_after_copy(self):
        old_plugin = self.add_plugin('SimplePlugin', self.page1)
        new_base_plugin = old_plugin.simplepluginmodel.copy_plugin(
            self.placeholder(self.page1),
            self.FIRST_LANG,
            {}
        )
        new_plugin = SimplePluginModel.objects.get(pk=new_base_plugin.pk)
        self.assertEqual(
            old_plugin.pk,
            new_plugin.original_instance.pk
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

    ##

    def test_copy_fk_from_plugin(self):
        plugin = self.add_plugin('PluginFKPlugin', self.page1)
        plugin_with_fk = self.add_plugin('PluginWithRelations', self.page2)
        self.publish_page(self.page2)
        page_copy = self.publish_page(self.page1)
        # TODO: Also write test where page1 is published first.
        plugin_copy = ExplicitPluginFKCopyPlugin.objects.get(placeholder__page=page_copy)
        self.assertEqual(
            list(plugin_copy.pluginwithrelations1_set.values_list('title', flat=True)),
            list(plugin.pluginwithrelations1_set.values_list('title', flat=True))
        )


    @unittest.skip('Not yet working on this')
    def test_copy_m2m_to_plugin(self):
        plugin = api.add_plugin(
            placeholder=self.placeholder1,
            plugin_type="PluginWithM2MToPlugin",
            language=self.FIRST_LANG,
        )
        m2m_target = api.add_plugin(
            placeholder=self.placeholder2,
            plugin_type='SimplePlugin',
            language=self.FIRST_LANG
        )
        plugin.m2m_field.add(m2m_target)
        old_public_count = PluginModelWithM2MToPlugin.objects.filter(
            m2m_field__placeholder__page__publisher_is_draft=False
        ).count()
        api.publish_page(
            self.page1,
            self.super_user,
            self.FIRST_LANG
        )
        api.publish_page(
            self.page2,
            self.super_user,
            self.FIRST_LANG
        )
        new_public_count = PluginModelWithM2MToPlugin.objects.filter(
            m2m_field__placeholder__page__publisher_is_draft=False
        ).count()
        self.assertEqual(
            new_public_count,
            old_public_count + 1
        )
