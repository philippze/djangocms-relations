import unittest

from django.conf import settings
from django.db import connection

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


class ClassCreation(BaseRelationsTest):
    
    def test_through_model_has_draft_fields(self):
        model = PluginModelWithM2MToPlugin
        fields = model.m2m_field.through._meta.fields
        draft_fields = [
            field for field in fields
            if 'draft' in field.name
        ]
        self.assertGreater(len(draft_fields), 0)
