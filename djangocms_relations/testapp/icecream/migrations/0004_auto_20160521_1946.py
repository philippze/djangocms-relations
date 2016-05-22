# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icecream', '0003_auto_20160521_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='photographer',
            field=models.ForeignKey(related_name='pictures', to='icecream.Photographer', null=True),
        ),
        migrations.AlterField(
            model_name='sundea',
            name='flavors',
            field=models.ManyToManyField(related_name='sundeas', to='icecream.Flavor'),
        ),
        migrations.AlterField(
            model_name='sundea',
            name='sauces',
            field=models.ManyToManyField(related_name='sundeas', to='icecream.Sauce'),
        ),
    ]
