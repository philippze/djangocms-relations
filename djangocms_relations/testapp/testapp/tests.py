from django.test import TestCase

from cms.models import Page


from testapp import (
    FKModel,
    M2MTargetModel,
    PluginModelWithFKFromModel,
    PluginModelWithM2MToModel,
    M2MTargetPluginModel,
    PluginModelWithFKFromPlugin,
    PluginModelWithM2MToPlugin
)


class TestFKFromModel(TestCase):
    
    def setUp(self):
        self.super_user = self._create_user("test", True, True)
        self.FIRST_LANG = settings.LANGUAGES[0][0]
        page_data1 = self.get_new_page_data_dbfields()
        page_data1['published'] = False
        self.page1 = api.create_page(**page_data1)
        page_data2 = self.get_new_page_data_dbfields()
        page_data2['published'] = False
        self.page2 = api.create_page(**page_data2)
        self.placeholder1 = self.page1.placeholders.get(slot='body')
        self.placeholder2 = self.page2.placeholders.get(slot='body')
    
    def tearDown(self):
        User.objects.all().delete()
        Page.objects.all().delete()
    
    def test_publishing(self):
        self.assertEqual(1, 2)
    
    
