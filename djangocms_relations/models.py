from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from cms.models import CMSPlugin


class AutocopyRelationsCMSPlugin(CMSPlugin):
    original_instance = models.ForeignKey('self', null=True)

    def copy_relations(self, oldinstance):
        self.original_instance_id = oldinstance.pk
        self.save()
        for field in self.get_autocopy_fields():
            objects = getattr(oldinstance, field)
            self.copy_objects(oldinstance, objects)

    def get_autocopy_fields(self):
        try:
            return self.autocopy_fields
        except AttributeError:
            return []
        # Should be extended to use some automatism

    def copy_objects(self, oldinstance, objects):
        for associated_item in objects.all():
            associated_item.pk = None
            associated_item.fk1 = self
            associated_item.save()
