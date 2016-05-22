# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icecream', '0001_initial'),
    ]

    operations = [
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
