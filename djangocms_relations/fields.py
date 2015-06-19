import six

from django.apps import apps
from django.db.models import ManyToManyField
from django.db.models.fields.related import (
    add_lazy_relation,
    RECURSIVE_RELATIONSHIP_CONSTANT,
    ReverseManyRelatedObjectsDescriptor
)
from django.utils.functional import curry


def create_many_to_many_intermediary_model(field, klass):
    """Copy & Paste from django.db.models.fields. Class Construction differs."""
    from django.db import models
    managed = True
    if isinstance(field.rel.to, six.string_types) and field.rel.to != RECURSIVE_RELATIONSHIP_CONSTANT:
        to_model = field.rel.to
        to = to_model.split('.')[-1]

        def set_managed(field, model, cls):
            field.rel.through._meta.managed = model._meta.managed or cls._meta.managed
        add_lazy_relation(klass, field, to_model, set_managed)
    elif isinstance(field.rel.to, six.string_types):
        to = klass._meta.object_name
        to_model = klass
        managed = klass._meta.managed
    else:
        to = field.rel.to._meta.object_name
        to_model = field.rel.to
        managed = klass._meta.managed or to_model._meta.managed
    name = '%s_%s' % (klass._meta.object_name, field.name)
    if field.rel.to == RECURSIVE_RELATIONSHIP_CONSTANT or to == klass._meta.object_name:
        from_ = 'from_%s' % to.lower()
        to = 'to_%s' % to.lower()
    else:
        from_ = klass._meta.model_name
        to = to.lower()
    meta = type(str('Meta'), (object,), {
        'db_table': field._get_m2m_db_table(klass._meta),
        'managed': managed,
        'auto_created': klass,
        'app_label': klass._meta.app_label,
        'db_tablespace': klass._meta.db_tablespace,
        'unique_together': (from_, to),
        'verbose_name': '%(from)s-%(to)s relationship' % {'from': from_, 'to': to},
        'verbose_name_plural': '%(from)s-%(to)s relationships' % {'from': from_, 'to': to},
        'apps': field.model._meta.apps,
    })
    # Construct and return the new class.
    return type(str(name), (models.Model,), {
        'Meta': meta,
        '__module__': klass.__module__,
        'draft_%s' % from_: models.ForeignKey(klass, related_name='_draft_%s+' % name, db_tablespace=field.db_tablespace, db_constraint=field.rel.db_constraint),
        'pub_%s' % from_: models.ForeignKey(klass, related_name='_pub_%s+' % name, db_tablespace=field.db_tablespace, db_constraint=field.rel.db_constraint),
        'draft_%s' % to: models.ForeignKey(to_model, related_name='_draft_%s+' % name, db_tablespace=field.db_tablespace, db_constraint=field.rel.db_constraint),
        'pub_%s' % to: models.ForeignKey(to_model, related_name='_pub_%s+' % name, db_tablespace=field.db_tablespace, db_constraint=field.rel.db_constraint),
    })


class M2MPluginField(ManyToManyField):
    
    
    def _check_relationship_model(self, from_model=None, **kwargs):
        """
            Copy & Paste from Djano,
            omitting the intermediate model checks
        """
        if hasattr(self.rel.through, '_meta'):
            qualified_model_name = "%s.%s" % (
                self.rel.through._meta.app_label, self.rel.through.__name__)
        else:
            qualified_model_name = self.rel.through

        errors = []

        if self.rel.through not in apps.get_models(include_auto_created=True):
            # The relationship model is not installed.
            errors.append(
                checks.Error(
                    ("Field specifies a many-to-many relation through model "
                     "'%s', which has not been installed.") %
                    qualified_model_name,
                    hint=None,
                    obj=self,
                    id='fields.E331',
                )
            )

        else:

            assert from_model is not None, \
                "ManyToManyField with intermediate " \
                "tables cannot be checked if you don't pass the model " \
                "where the field is attached to."

            # Set some useful local variables
            to_model = self.rel.to
            from_model_name = from_model._meta.object_name
            if isinstance(to_model, six.string_types):
                to_model_name = to_model
            else:
                to_model_name = to_model._meta.object_name
            relationship_model_name = self.rel.through._meta.object_name
            self_referential = from_model == to_model

            # Check symmetrical attribute.
            if (self_referential and self.rel.symmetrical and
                    not self.rel.through._meta.auto_created):
                errors.append(
                    checks.Error(
                        'Many-to-many fields with intermediate tables must not be symmetrical.',
                        hint=None,
                        obj=self,
                        id='fields.E332',
                    )
                )
        return errors

    
    def contribute_to_class(self, cls, name):
        """
            Copy & Paste from Django.
            Just `create_many_to_many_intermediary_model`
            was defined differently in this file.
        """
        # To support multiple relations to self, it's useful to have a non-None
        # related name on symmetrical relations for internal reasons. The
        # concept doesn't make a lot of sense externally ("you want me to
        # specify *what* on my non-reversible relation?!"), so we set it up
        # automatically. The funky name reduces the chance of an accidental
        # clash.
        if self.rel.symmetrical and (self.rel.to == "self" or self.rel.to == cls._meta.object_name):
            self.rel.related_name = "%s_rel_+" % name

        super(ManyToManyField, self).contribute_to_class(cls, name)

        # The intermediate m2m model is not auto created if:
        #  1) There is a manually specified intermediate, or
        #  2) The class owning the m2m field is abstract.
        #  3) The class owning the m2m field has been swapped out.
        if not self.rel.through and not cls._meta.abstract and not cls._meta.swapped:
            self.rel.through = create_many_to_many_intermediary_model(self, cls)

        # Add the descriptor for the m2m relation
        setattr(cls, self.name, ReverseManyRelatedObjectsDescriptor(self))

        # Set up the accessor for the m2m table name for the relation
        self.m2m_db_table = curry(self._get_m2m_db_table, cls._meta)

        # Populate some necessary rel arguments so that cross-app relations
        # work correctly.
        if isinstance(self.rel.through, six.string_types):
            def resolve_through_model(field, model, cls):
                field.rel.through = model
            add_lazy_relation(cls, self, self.rel.through, resolve_through_model)
        
