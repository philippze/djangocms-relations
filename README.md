# djangocms-relations

Handling relations for custom cmsplugins


## Installation

`$ git clone git@github.com:philippze/djangocms-relations.git <yourfolder>`

`$ pip install -r test_requirements/django-1.7.txt`


## Running tests (Currently: Error)

`cd <yourfolder>` 

`./TEST`


## Roadmap

1. Create a working ManyToManyField to another CMSPlugin
2. Create little helpers as an alternative to defining `copy_relations` for every relation field.
3. Think about a solution for ForeignKeys
4. Ideas about optimizing relations between CMSPlugins and usual models might appear.


## The problem with relations

In the Django CMS,
as soon as a page is published every CMSPlugin exists in two versions.
A public and a draft version.
There is no direct link between them.

When we publish changes on a page,
the CMSPlugins of the public version will be deleted
and replaced by copys of the draft version's plugins.


## Standard-Solution: ForeignKey from model to CMSPlugin

If there is a foreign key from a model to a CMSPlugin,
we have to create a copy of the model instance
when publishing the CMSPluigin.

The new copy of the original instance will be related
to the public version of the CMSPlugin
while the model instance we edit should have a relation
with the draft version of the CMSPlugin.

This graphic shows what happens.

![](readme-fk.png "Foreign Key between model and CMSPlugin")



## The problem with relations between two CMSPlugins

Creating a copy of the model instance where the ForeignKey comes from
conflicts with the concept of one draft and one publich version of a CMSPlugin.

Applying the usual copying mechanism will result in two draft versions as the following graphics shows.

![](readme-fk-cmsplugin.png "Foreign Key between two CMSPlugins")



## New roadmap

- Simply create a connection between the published and the unpublished version of the CMSPlugin.
- Take care that it won't disturb CMSPlugins without a publishing mechanism, e.g. in model fields.
- The connection is added to the CMSPlugin class with the mixin `AutocopyRelationsMixin`. Both, classes involved in the relationship must inherit from this mixin.
- The mixin comes with a generic `copy_relations` method that are a useful default for ForeignKeyFields and ManyToManyFields.
- Provide the option `autocopy_relations` to customize for which fields the default copy mechanism will be used.
