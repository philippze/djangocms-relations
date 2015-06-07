from django.db import models

from cms.models import CMSPlugin


class FKModel(models.Model):
    title = models.CharField(max_length=50)
    fk_field = models.ForeignKey('PluginModelWithFKFromModel')


class M2MTargetModel(models.Model):
    title = models.CharField(max_length=50)


class PluginModelWithFKFromModel(CMSPlugin):
    title = models.CharField(max_length=50)


class PluginModelWithM2MToModel(CMSPlugin):
    title = models.CharField(max_length=50)
    m2m_field = models.ManyToManyField(M2MTargetModel)


class FKPluginModel(CMSPlugin):
    title = models.CharField(max_length=50)
    fk_field = models.ForeignKey('PluginModelWithFKFromPlugin')


class M2MTargetPluginModel(CMSPlugin):
    title = models.CharField(max_length=50)


class PluginModelWithFKFromPlugin(CMSPlugin):
    title = models.CharField(max_length=50)


class PluginModelWithM2MToPlugin(CMSPlugin):
    title = models.CharField(max_length=50)
    m2m_field = models.ManyToManyField(M2MTargetPluginModel)
