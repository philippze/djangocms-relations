from django.conf import settings
from django.contrib.auth.models import User

from cms import api
from cms.models import Page
from cms.test_utils.testcases import CMSTestCase



class BaseRelationsTest(CMSTestCase):
    
    def setUp(self):
        self.super_user = self._create_user("test", True, True)
        self._login_context = self.login_user_context(self.super_user)
        self._login_context.__enter__()
        self.FIRST_LANG = settings.LANGUAGES[0][0]
        page_data1 = self.get_new_page_data_dbfields()
        page_data1['template'] = 'cms_page.html'
        page_data1['published'] = False
        self.page1 = api.create_page(**page_data1)
        page_data2 = self.get_new_page_data_dbfields()
        page_data2['template'] = 'cms_page.html'
        page_data2['published'] = False
        self.page2 = api.create_page(**page_data2)
    
    def tearDown(self):
        User.objects.all().delete()
        Page.objects.all().delete()
    
    def get_draft_placeholder_1(self):
        if not self.page1.publisher_is_draft == True:
            return self.page1.placeholders.get(slot='body')
        try:
            return self.page1.publisher_draft.placeholders.get(slot='body')
        except Page.DoesNotExist:
            return self.page1.placeholders.get(slot='body')
    
    def get_draft_placeholder_2(self):
        if not self.page2.publisher_is_draft == True:
            return self.page2.placeholders.get(slot='body')
        try:
            return self.page2.publisher_draft.placeholders.get(slot='body')
        except Page.DoesNotExist:
            return self.page2.placeholders.get(slot='body')
    
    def get_public_placeholder_1(self):
        return self.page1.publisher_public.placeholders.get(slog='body')
    
    def get_public_placeholder_2(self):
        return self.page2.publisher_public.placeholders.get(slog='body')

    def get_draft_plugin_1(self):
        placeholder = self.get_draft_placeholder_1()
        return placeholder.cmsplugin_set.get()
