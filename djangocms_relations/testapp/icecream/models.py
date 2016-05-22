from cms.models.pluginmodel import CMSPlugin

from django.db import models

from djangocms_relations.models import RelationsCMSPlugin


class Flavor(RelationsCMSPlugin):
    name = models.CharField(max_length=50)

    autocopy_fields = {
        'fk': ['fans'],
        'plugin_m2m': ['sundeas']
    }


class Sundea(RelationsCMSPlugin):
    name = models.CharField(max_length=50)
    flavors = models.ManyToManyField(
        Flavor,
        related_name='sundeas'
    )
    sauces = models.ManyToManyField(
        'Sauce',
        related_name='sundeas'
    )

    autocopy_fields = {
        'plugin_fk': ['pictures'],
        'm2m': ['sauces'],
        'plugin_m2m': ['flavors']
    }


class Picture(RelationsCMSPlugin):
    name = models.CharField(max_length=50)
    sundea = models.ForeignKey(
        Sundea,
        related_name='pictures',
        null=True
    )
    photographer = models.ForeignKey(
        'Photographer',
        related_name='pictures',
        null=True
    )

    autocopy_fields = {
    }


class Photographer(models.Model):
    name = models.CharField(max_length=50)
    favorite = models.ForeignKey(
        'Flavor',
        related_name='fans',
        null=True
    )


class Sauce(models.Model):
    name = models.CharField(max_length=50)
