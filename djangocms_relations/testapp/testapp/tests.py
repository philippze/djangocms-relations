import unittest

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase

from cms import api
from cms.models import Page
from cms.test_utils.testcases import CMSTestCase


from testapp.models import (
    FKModel,
    FKPluginModel,
    M2MTargetModel,
    PluginModelWithFKFromModel,
    PluginModelWithM2MToModel,
    M2MTargetPluginModel,
    PluginModelWithFKFromPlugin,
    PluginModelWithM2MToPlugin
)


class TestFKFromModel(CMSTestCase):
    
    def setUp(self):
        self.super_user = self._create_user("test", True, True)
        self.FIRST_LANG = settings.LANGUAGES[0][0]
        page_data1 = self.get_new_page_data_dbfields()
        page_data1['template'] = 'cms_page.html'
        page_data1['published'] = False
        self.page1 = api.create_page(**page_data1)
        page_data2 = self.get_new_page_data_dbfields()
        page_data2['template'] = 'cms_page.html'
        page_data2['published'] = False
        self.page2 = api.create_page(**page_data2)
        self.placeholder1 = self.page1.placeholders.get(slot='body')
        self.placeholder2 = self.page2.placeholders.get(slot='body')
    
    def tearDown(self):
        User.objects.all().delete()
        Page.objects.all().delete()
    
    @unittest.skip('Not yet working on this')
    def test_copy_fk_from_plugin(self):
        plugin = api.add_plugin(
            placeholder=self.placeholder1,
            plugin_type="PluginWithFKFromPlugin",
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
            plugin_type='M2MTargetPlugin',
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
