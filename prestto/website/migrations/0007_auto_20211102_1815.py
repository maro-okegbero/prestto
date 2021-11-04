# Generated by Django 3.2.8 on 2021-11-02 18:15

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_auto_20211102_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessname',
            name='corporate_owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.corporateowner'),
        ),
        migrations.AlterField(
            model_name='businessname',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 2, 18, 15, 0, 172645, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='businessname',
            name='individual_owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.individualowner'),
        ),
        migrations.AlterField(
            model_name='businessname',
            name='last_created',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 2, 18, 15, 0, 172665, tzinfo=utc)),
        ),
    ]
