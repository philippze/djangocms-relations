# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_relations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExplicitFKCopyPlugin',
            fields=[
                ('autocopyrelationscmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='djangocms_relations.AutocopyRelationsCMSPlugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('djangocms_relations.autocopyrelationscmsplugin',),
        ),
        migrations.CreateModel(
            name='ExplicitM2MCopyPlugin',
            fields=[
                ('autocopyrelationscmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='djangocms_relations.AutocopyRelationsCMSPlugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('djangocms_relations.autocopyrelationscmsplugin',),
        ),
        migrations.CreateModel(
            name='ExplicitPluginFKCopyPlugin',
            fields=[
                ('autocopyrelationscmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='djangocms_relations.AutocopyRelationsCMSPlugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('djangocms_relations.autocopyrelationscmsplugin',),
        ),
        migrations.CreateModel(
            name='ExplicitPluginM2MCopyPlugin',
            fields=[
                ('autocopyrelationscmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='djangocms_relations.AutocopyRelationsCMSPlugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('djangocms_relations.autocopyrelationscmsplugin',),
        ),
        migrations.CreateModel(
            name='ImplicitFKCopyPlugin',
            fields=[
                ('autocopyrelationscmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='djangocms_relations.AutocopyRelationsCMSPlugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('djangocms_relations.autocopyrelationscmsplugin',),
        ),
        migrations.CreateModel(
            name='ImplicitM2MCopyPlugin',
            fields=[
                ('autocopyrelationscmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='djangocms_relations.AutocopyRelationsCMSPlugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('djangocms_relations.autocopyrelationscmsplugin',),
        ),
        migrations.CreateModel(
            name='ImplicitPluginFKCopyPlugin',
            fields=[
                ('autocopyrelationscmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='djangocms_relations.AutocopyRelationsCMSPlugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('djangocms_relations.autocopyrelationscmsplugin',),
        ),
        migrations.CreateModel(
            name='ImplicitPluginM2MCopyPlugin',
            fields=[
                ('autocopyrelationscmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='djangocms_relations.AutocopyRelationsCMSPlugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('djangocms_relations.autocopyrelationscmsplugin',),
        ),
        migrations.CreateModel(
            name='ModelWithRelations1',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('fk1', models.ForeignKey(to='testapp.ExplicitFKCopyPlugin', null=True)),
                ('fk2', models.ForeignKey(to='testapp.ImplicitFKCopyPlugin', null=True)),
                ('m2m1', models.ManyToManyField(to='testapp.ExplicitM2MCopyPlugin')),
                ('m2m2', models.ManyToManyField(to='testapp.ImplicitM2MCopyPlugin')),
            ],
        ),
        migrations.CreateModel(
            name='ModelWithRelations2',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fk1', models.ForeignKey(to='testapp.ExplicitFKCopyPlugin', null=True)),
                ('fk2', models.ForeignKey(to='testapp.ImplicitFKCopyPlugin', null=True)),
                ('m2m1', models.ManyToManyField(to='testapp.ExplicitM2MCopyPlugin')),
                ('m2m2', models.ManyToManyField(to='testapp.ImplicitM2MCopyPlugin')),
            ],
        ),
        migrations.CreateModel(
            name='PluginWithRelations1',
            fields=[
                ('autocopyrelationscmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='djangocms_relations.AutocopyRelationsCMSPlugin')),
                ('title', models.CharField(max_length=50)),
                ('fk1', models.ForeignKey(to='testapp.ExplicitPluginFKCopyPlugin', null=True)),
                ('fk2', models.ForeignKey(to='testapp.ImplicitFKCopyPlugin', null=True)),
                ('m2m1', models.ManyToManyField(to='testapp.ExplicitM2MCopyPlugin')),
                ('m2m2', models.ManyToManyField(to='testapp.ImplicitM2MCopyPlugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('djangocms_relations.autocopyrelationscmsplugin',),
        ),
        migrations.CreateModel(
            name='PluginWithRelations2',
            fields=[
                ('autocopyrelationscmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='djangocms_relations.AutocopyRelationsCMSPlugin')),
                ('fk1', models.ForeignKey(to='testapp.ExplicitPluginFKCopyPlugin', null=True)),
                ('fk2', models.ForeignKey(to='testapp.ImplicitFKCopyPlugin', null=True)),
                ('m2m1', models.ManyToManyField(to='testapp.ExplicitM2MCopyPlugin')),
                ('m2m2', models.ManyToManyField(to='testapp.ImplicitM2MCopyPlugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('djangocms_relations.autocopyrelationscmsplugin',),
        ),
        migrations.CreateModel(
            name='SimplePluginModel',
            fields=[
                ('autocopyrelationscmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='djangocms_relations.AutocopyRelationsCMSPlugin')),
                ('title', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=('djangocms_relations.autocopyrelationscmsplugin',),
        ),
    ]
