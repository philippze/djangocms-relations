from django.db import models

from cms.models import CMSPlugin
from djangocms_relations import (
    M2MPluginField,
    PluginWithRelationsMixin
)


class FKModel(models.Model):
    title = models.CharField(max_length=50)
    fk_field = models.ForeignKey('SimplePluginModel')


class M2MTargetModel(models.Model):
    title = models.CharField(max_length=50)


class SimplePluginModel(CMSPlugin):
    title = models.CharField(max_length=50)


class PluginModelWithM2MToModel(CMSPlugin):
    title = models.CharField(max_length=50)
    m2m_field = models.ManyToManyField(M2MTargetModel)


class FKPluginModel(PluginWithRelationsMixin, CMSPlugin):
    title = models.CharField(max_length=50)
    fk_field = models.ForeignKey('SimplePluginModel')


class M2MTargetPluginModel(CMSPlugin):
    title = models.CharField(max_length=50)


class PluginModelWithM2MToPlugin(CMSPlugin):
    title = models.CharField(max_length=50)
    m2m_field = M2MPluginField(SimplePluginModel)


class CustomThroughModel(models.Model):
    plugin_1_draft = models.ForeignKey(SimplePluginModel)
    plugin_1_public = models.ForeignKey(
        SimplePluginModel,
        related_name='custom_through_for_public'
    )
    plugin_2_draft = models.ForeignKey('CustomThroughPluginModel')
    plugin_2_public = models.ForeignKey(
        'CustomThroughPluginModel',
        related_name='custom_through_for_public'
    )


class CustomThroughPluginModel(CMSPlugin):
    title = models.CharField(max_length=50)
    m2m_field = M2MPluginField(SimplePluginModel)
