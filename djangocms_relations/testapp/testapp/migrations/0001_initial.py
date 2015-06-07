# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djangocms_relations.mixins
import djangocms_relations.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0011_auto_20150419_1006'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomThroughModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomThroughPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='FKModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FKPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=(djangocms_relations.mixins.PluginWithRelationsMixin, 'cms.cmsplugin'),
        ),
        migrations.CreateModel(
            name='M2MTargetModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='M2MTargetPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='PluginModelWithM2MToModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=50)),
                ('m2m_field', models.ManyToManyField(to='testapp.M2MTargetModel')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='PluginModelWithM2MToPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='SimplePluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.AddField(
            model_name='pluginmodelwithm2mtoplugin',
            name='m2m_field',
            field=djangocms_relations.fields.M2MPluginField(to='testapp.SimplePluginModel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fkpluginmodel',
            name='fk_field',
            field=models.ForeignKey(to='testapp.SimplePluginModel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fkmodel',
            name='fk_field',
            field=models.ForeignKey(to='testapp.SimplePluginModel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customthroughpluginmodel',
            name='m2m_field',
            field=djangocms_relations.fields.M2MPluginField(to='testapp.SimplePluginModel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customthroughmodel',
            name='plugin_1_draft',
            field=models.ForeignKey(to='testapp.SimplePluginModel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customthroughmodel',
            name='plugin_1_public',
            field=models.ForeignKey(related_name='custom_through_for_public', to='testapp.SimplePluginModel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customthroughmodel',
            name='plugin_2_draft',
            field=models.ForeignKey(to='testapp.CustomThroughPluginModel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customthroughmodel',
            name='plugin_2_public',
            field=models.ForeignKey(related_name='custom_through_for_public', to='testapp.CustomThroughPluginModel'),
            preserve_default=True,
        ),
    ]
