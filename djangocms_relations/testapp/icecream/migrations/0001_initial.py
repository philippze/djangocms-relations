# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_relations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flavor',
            fields=[
                ('relationscmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='djangocms_relations.RelationsCMSPlugin')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=('djangocms_relations.relationscmsplugin',),
        ),
        migrations.CreateModel(
            name='Photographer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('favorite', models.ForeignKey(related_name='fans', to='icecream.Flavor', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('relationscmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='djangocms_relations.RelationsCMSPlugin')),
                ('name', models.CharField(max_length=50)),
                ('photographer', models.ForeignKey(related_name='pictures', to='icecream.Photographer')),
            ],
            options={
                'abstract': False,
            },
            bases=('djangocms_relations.relationscmsplugin',),
        ),
        migrations.CreateModel(
            name='Sauce',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Sundea',
            fields=[
                ('relationscmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='djangocms_relations.RelationsCMSPlugin')),
                ('name', models.CharField(max_length=50)),
                ('flavors', models.ManyToManyField(related_name='sundeas', null=True, to='icecream.Flavor')),
                ('sauces', models.ManyToManyField(related_name='sundeas', null=True, to='icecream.Sauce')),
            ],
            options={
                'abstract': False,
            },
            bases=('djangocms_relations.relationscmsplugin',),
        ),
        migrations.AddField(
            model_name='picture',
            name='sundea',
            field=models.ForeignKey(related_name='pictures', to='icecream.Sundea', null=True),
        ),
    ]
