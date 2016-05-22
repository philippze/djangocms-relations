# djangocms-relations


## Handling relations for custom CMSPlugins

This plugin should do two things (and do them well):

1. Provide a mechanism to deal with relations **between** CMSPlugins.
2. Simplify dealing with relations in custom CMSPlugins in general.


## Usage

- Let all your CMSPlugins involved in relations inherit from `djangocms_relations.models.RelationsCMSPlugin`.
- Tell the plugin about the relations it has using the property `autocopy_fields`, like this:

`autocopy_fields = {  
    'fk': [],  
    'm2m': ['sauces'],  
    'plugin_fk': ['pictures'],  
    'plugin_m2m': ['flavors']  
}
`

- Then, writing your own `copy_relations` methods is no more necessary. Everything will be copied automatically.
- When you have relations between plugins and publish an involved page, their relations are renewed such that afterwards the published plugins have only relations with published plugins and draft plugins, too, have only relations between each other.


## Requirements

- Django 1.8
- DjangoCMS 3.2
- Python 2.7


## Running tests

To execute the tests, after installing the `test_requirements/django-1.8.txt`
you can use the simple `TEST` shell script:

`./TEST`


## Still to do

### Mandatory

- Check what happens when CMSPlugins with relations are deleted
- Check that test on "Publish an involved page" cover all scenarios.

### Enhancements

- Provide a `PluginField` and a `ManyPluginsField` for relations between plugins. They should have only draft versions in their querysets.
- Build an automatism for detecting the relations a CMSPlugin has and skip the `autocopy_fields` property.
- Add some model validation.
- Support Python 3.
