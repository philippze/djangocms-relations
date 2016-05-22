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
    autocopy_fields = ['modelwithrelations1_set']


class ImplicitM2MCopyPlugin(AutocopyRelationsCMSPlugin):
    pass


class ExplicitPluginFKCopyPlugin(AutocopyRelationsCMSPlugin):
    title = models.CharField(max_length=50)
    autocopy_fields = ['pluginwithrelations1_set']


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
    )
    m2m2 = models.ManyToManyField(
        ImplicitM2MCopyPlugin,
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
    )
    m2m2 = models.ManyToManyField(
        ImplicitM2MCopyPlugin,
    )


class PluginWithRelations1(AutocopyRelationsCMSPlugin):
    title = models.CharField(max_length=50)
    fk1 = models.ForeignKey(
        ExplicitPluginFKCopyPlugin,
        null=True
    )
    fk2 = models.ForeignKey(
        ImplicitFKCopyPlugin,
        null=True
    )
    m2m1 = models.ManyToManyField(
        ExplicitM2MCopyPlugin,
    )
    m2m2 = models.ManyToManyField(
        ImplicitM2MCopyPlugin,
    )

    autocopy_fields = ['fk1', 'fk2', 'm2m1', 'm2m2']


class PluginWithRelations2(AutocopyRelationsCMSPlugin):
    fk1 = models.ForeignKey(
        ExplicitPluginFKCopyPlugin,
        null=True
    )
    fk2 = models.ForeignKey(
        ImplicitFKCopyPlugin,
        null=True
    )
    m2m1 = models.ManyToManyField(
        ExplicitM2MCopyPlugin,
    )
    m2m2 = models.ManyToManyField(
        ImplicitM2MCopyPlugin,
    )



## For utils tests


class A(models.Model):
    pass


class B(A):
    pass


class C(B):
    pass
