import unittest

from cms import api
from cms.models import Page

from .base import BaseRelationsTest

from testapp.models import (
    SimplePluginModel,
    ExplicitFKCopyPlugin,
    ImplicitFKCopyPlugin,
    ModelWithRelations1,
)


class TestFKFromModel(BaseRelationsTest):

    def test_plugin_has_old_instance_property(self):
        placeholder = self.get_draft_placeholder_1()
        plugin = api.add_plugin(
            placeholder=placeholder,
            plugin_type="SimplePlugin",
            language=self.FIRST_LANG,
        )
        try:
            plugin.original_instance
        except AttributeError:
            self.fail('Plugin has no property `old_instance`.')

    def test_old_instance_reachable_after_copy(self):
        placeholder = self.get_draft_placeholder_1()
        old_plugin = api.add_plugin(
            placeholder=placeholder,
            plugin_type="SimplePlugin",
            language=self.FIRST_LANG,
        )
        new_base_plugin = old_plugin.simplepluginmodel.copy_plugin(
            placeholder,
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

    def test_reverse_foreign_key_copied(self):
        plugin = api.add_plugin(
            placeholder=self.get_draft_placeholder_1(),
            plugin_type="FKPlugin",
            language=self.FIRST_LANG,
        )
        model = ModelWithRelations1.objects.create(
            fk1=plugin,
            title='asdf'
        )
        api.publish_page(self.page1, self.super_user, self.FIRST_LANG)
        page_copy = Page.objects.public().get(
            title_set__title=self.page1.get_title(self.FIRST_LANG)
        )
        plugin_copy = ExplicitFKCopyPlugin.objects.get(placeholder__page=page_copy)
        self.assertEqual(
            plugin_copy.explicitfkcopyplugin.modelwithrelations1_set.values_list('title', flat=True)[0],
            plugin.modelwithrelations1_set.values_list('title', flat=True)[0]
        )
        

    @unittest.skip('Not yet working on this')
    def test_publish_plugin_fk_points_to(self):
        models_with_fk_to_page_old_count = FKModel.objects.filter(
            fk_field__placeholder__page=self.page1,
            fk_field__placeholder__page__publisher_is_draft=True
        ).count()
        plugin = api.add_plugin(
            placeholder=self.get_draft_placeholder_1(),
            plugin_type="SimplePlugin",
            language=self.FIRST_LANG,
        )
        model = FKModel.objects.create(
            title='Some title',
            fk_field=plugin
        )
        api.publish_page(self.page1, self.super_user, self.FIRST_LANG)
        models_with_fk_to_page_count = FKModel.objects.filter(
            fk_field__placeholder__page=self.page1,
            fk_field__placeholder__page__publisher_is_draft=True
        ).count()
        self.assertEqual(
            models_with_fk_to_page_count,
            models_with_fk_to_page_old_count + 1
        )
            
        
    
    @unittest.skip('Not yet working on this')
    def test_copy_fk_from_plugin(self):
        plugin = api.add_plugin(
            placeholder=self.placeholder1,
            plugin_type="SimplePlugin",
            language=self.FIRST_LANG,
        )
        api.add_plugin(
            placeholder=self.placeholder2,
            plugin_type='FKPlugin',
            language=self.FIRST_LANG,
            fk_field=plugin
        )
        old_plugin_count = FKPluginModel.objects.filter(
            fk_field__placeholder__page__publisher_is_draft=False
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
        new_plugin_count = FKPluginModel.objects.filter(
            fk_field__placeholder__page__publisher_is_draft=False
        ).count()
        self.assertEqual(
            new_plugin_count,
            old_plugin_count + 1
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
