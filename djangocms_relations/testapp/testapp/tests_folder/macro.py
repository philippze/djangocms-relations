import unittest

from cms import api

from .base import BaseRelationsTest

from testapp.models import (
    FKModel,
    FKPluginModel,
    M2MTargetModel,
    PluginModelWithM2MToModel,
    M2MTargetPluginModel,
    PluginModelWithM2MToPlugin,
    SimplePluginModel
)


class TestFKFromModel(BaseRelationsTest):
    
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
