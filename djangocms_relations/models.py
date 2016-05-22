import inspect

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from cms.models import CMSPlugin


class RelationsCMSPlugin(CMSPlugin):
    autocopy_draft = models.OneToOneField(
        'self',
        null=True,
        related_name='autocopy_public'
    )

    def is_draft(self):
        try:
            return self.autocopy_public is not None
        except ObjectDoesNotExist:
            return True

    def is_public(self):
        return not self.is_draft()

    def get_public_version(self):
        if self.is_public():
            return self
        else:
            # Return proper model instance, not a RelationsCMSPlugin
            model = self.__class__
            try:
                return model.objects.get(pk=self.autocopy_public.pk)
            except ObjectDoesNotExist:
                return None

    def get_draft_version(self):
        if self.is_draft():
            return self
        else:
            # Return proper model instance, not a RelationsCMSPlugin
            model = self.__class__
            return model.objects.get(pk=self.autocopy_draft.pk)

    def copy_relations(self, oldinstance):
        self.autocopy_draft = oldinstance
        for field in self.get_fk_fields():
            self.copy_fk(oldinstance, field)
        for field in self.get_m2m_fields():
            self.copy_m2m(oldinstance, field)
        for field in self.get_plugin_fk_fields():
            self.copy_plugin_fk(oldinstance, field)
        for field in self.get_plugin_m2m_fields():
            self.copy_plugin_m2m(oldinstance, field)
        self.save()

    def get_fk_fields(self):
        return self.autocopy_fields.get('fk', [])

    def get_m2m_fields(self):
        return self.autocopy_fields.get('m2m', [])

    def get_plugin_fk_fields(self):
        return self.autocopy_fields.get('plugin_fk', [])

    def get_plugin_m2m_fields(self):
        return self.autocopy_fields.get('plugin_m2m', [])

    def copy_fk(self, oldinstance, field):
        # TODO: When fk from CMSPlugin: dont create a new instance but use the already published version or so...
        # get name of the original field, on the other model:
        field_name = self._meta.get_field(field).field.name
        objects = getattr(oldinstance, field)
        for associated_item in objects.all():
            associated_item.pk = None
            setattr(
                associated_item,
                field_name,
                self
            )
            associated_item.save()

    def copy_m2m(self, oldinstance, field):
        related_manager = getattr(oldinstance, field)
        value = related_manager.all()
        setattr(self, field, value)

    def copy_plugin_fk(self, oldinstance, field):
        field_name = self._meta.get_field(field).field.name
        objects = getattr(oldinstance, field)
        for associated_item in objects.all():
            draft = associated_item.get_draft_version()
            public = associated_item.get_public_version()
            try:
                setattr(
                    draft,
                    field_name,
                    oldinstance
                )
            except AttributeError:
                pass
            else:
                draft.save()
            try:
                setattr(
                    public,
                    field_name,
                    self
                )
            except AttributeError:
                pass
            else:
                public.save()

    def copy_plugin_m2m(self, oldinstance, field):
        objects = getattr(oldinstance, field)
        draft_objects = []
        public_objects = []
        for associated_item in objects.all():
            draft = associated_item.get_draft_version()
            public = associated_item.get_public_version()
            if draft:
                draft_objects.append(draft)
            if public:
                public_objects.append(public)
        setattr(
            oldinstance,
            field,
            draft_objects
        )
        setattr(
            self,
            field,
            public_objects
        )
