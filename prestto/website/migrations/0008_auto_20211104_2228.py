# Generated by Django 3.2.8 on 2021-11-04 22:28

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_auto_20211102_1815'),
    ]

    operations = [
        migrations.CreateModel(
            name='LimitedLiability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='businessname',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 4, 22, 28, 36, 474805, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='businessname',
            name='last_created',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 4, 22, 28, 36, 474822, tzinfo=utc)),
        ),
    ]
