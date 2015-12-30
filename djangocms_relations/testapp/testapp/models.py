from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from cms.models import CMSPlugin
from djangocms_relations.models import (
    AutocopyRelationsCMSPlugin
)


class SimplePluginModel(AutocopyRelationsCMSPlugin):
    title = models.CharField(max_length=50)


class ExplicitFKCopyPlugin(AutocopyRelationsCMSPlugin):
    autocopy_fields = ['modelwithrelations1_set']


class ImplicitFKCopyPlugin(AutocopyRelationsCMSPlugin):
    pass


class ExplicitM2MCopyPlugin(AutocopyRelationsCMSPlugin):
    autocopy_fields = ['ModelWithRelations1_set']


class ImplicitM2MCopyPlugin(AutocopyRelationsCMSPlugin):
    pass


class ExplicitPluginFKCopyPlugin(AutocopyRelationsCMSPlugin):
    autocopy_fields = ['PluginWithRelations1_set']


class ImplicitPluginFKCopyPlugin(AutocopyRelationsCMSPlugin):
    pass


class ExplicitPluginM2MCopyPlugin(AutocopyRelationsCMSPlugin):
    autocopy_fields = ['PluginWithRelations1_set']


class ImplicitPluginM2MCopyPlugin(AutocopyRelationsCMSPlugin):
    pass


class ModelWithRelations1(models.Model):
    title = models.CharField(max_length=50)
    fk1 = models.ForeignKey(
        ExplicitFKCopyPlugin,
        null=True
    )
    fk2 = models.ForeignKey(
        ImplicitFKCopyPlugin,
        null=True
    )
    m2m1 = models.ManyToManyField(
        ExplicitM2MCopyPlugin,
        null=True
    )
    m2m2 = models.ManyToManyField(
        ImplicitM2MCopyPlugin,
        null=True
    )


class ModelWithRelations2(models.Model):
    fk1 = models.ForeignKey(
        ExplicitFKCopyPlugin,
        null=True
    )
    fk2 = models.ForeignKey(
        ImplicitFKCopyPlugin,
        null=True
    )
    m2m1 = models.ManyToManyField(
        ExplicitM2MCopyPlugin,
        null=True
    )
    m2m2 = models.ManyToManyField(
        ImplicitM2MCopyPlugin,
        null=True
    )


class PluginWithRelations1(AutocopyRelationsCMSPlugin):
    fk1 = models.ForeignKey(
        ExplicitFKCopyPlugin,
        null=True
    )
    fk2 = models.ForeignKey(
        ImplicitFKCopyPlugin,
        null=True
    )
    m2m1 = models.ManyToManyField(
        ExplicitM2MCopyPlugin,
        null=True
    )
    m2m2 = models.ManyToManyField(
        ImplicitM2MCopyPlugin,
        null=True
    )


class PluginWithRelations2(AutocopyRelationsCMSPlugin):
    fk1 = models.ForeignKey(
        ExplicitFKCopyPlugin,
        null=True
    )
    fk2 = models.ForeignKey(
        ImplicitFKCopyPlugin,
        null=True
    )
    m2m1 = models.ManyToManyField(
        ExplicitM2MCopyPlugin,
        null=True
    )
    m2m2 = models.ManyToManyField(
        ImplicitM2MCopyPlugin,
        null=True
    )
