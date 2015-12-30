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
            self.copy_objects(oldinstance, field)

    def get_autocopy_fields(self):
        try:
            return self.autocopy_fields
        except AttributeError:
            return []
        # Should be extended to use some automatism

    def copy_objects(self, oldinstance, field):
        objects = getattr(oldinstance, field)
        if objects.__class__.__name__ == 'ManyRelatedManager':
            self.copy_m2m(oldinstance, field)
        else:
            self.copy_fk(oldinstance, field)

    def copy_fk(self, oldinstance, field):
        rel = self._meta.get_field(field.replace('_set', ''))
        objects = getattr(oldinstance, field)
        for associated_item in objects.all():
            associated_item.pk = None
            setattr(
                associated_item,
                rel.field.name,
                self
            )
            associated_item.save()

    def copy_m2m(self, oldinstance, field):
        related_manager = getattr(oldinstance, field)
        value = related_manager.all()
        setattr(self, field, value)
