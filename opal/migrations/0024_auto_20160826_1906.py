# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opal', '0023_auto_20160630_1340'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tagging',
            unique_together=set([('value', 'episode', 'user')]),
        ),
    ]
