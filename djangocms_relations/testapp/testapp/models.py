from django.db import models

from cms.models import CMSPlugin
from djangocms_relations import (
    AutocopyRelationsMixin
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


class FKPluginModel(CMSPlugin):
    title = models.CharField(max_length=50)
    fk_field = models.ForeignKey('SimplePluginModel')


class M2MTargetPluginModel(CMSPlugin):
    title = models.CharField(max_length=50)


class PluginModelWithM2MToPlugin(CMSPlugin):
    title = models.CharField(max_length=50)
    m2m_field = models.ManyToManyField(SimplePluginModel)
