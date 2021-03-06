# Generated by Django 3.2.8 on 2021-10-31 15:30

import cloudinary.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attestee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=200)),
                ('first_name', models.CharField(blank=True, max_length=200)),
                ('other_name', models.CharField(blank=True, max_length=200)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(max_length=100)),
                ('nationality', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=12)),
                ('email', models.EmailField(max_length=12)),
                ('residential_address', models.CharField(max_length=1000)),
                ('means_of_identification', models.CharField(max_length=100)),
                ('identification_number', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ExtraDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', cloudinary.models.CloudinaryField(max_length=255, verbose_name='pdf')),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='business_email',
        ),
        migrations.CreateModel(
            name='IndividualOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=200)),
                ('first_name', models.CharField(blank=True, max_length=200)),
                ('other_name', models.CharField(blank=True, max_length=200)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(max_length=100)),
                ('nationality', models.CharField(max_length=100)),
                ('occupation', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=12)),
                ('email', models.EmailField(max_length=12)),
                ('residential_address', models.CharField(max_length=1000)),
                ('means_of_identification', models.CharField(max_length=100)),
                ('identification', cloudinary.models.CloudinaryField(max_length=255, verbose_name='pdf')),
                ('signature', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('photograph', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('other_documents', models.ManyToManyField(to='website.ExtraDocument')),
            ],
        ),
        migrations.CreateModel(
            name='CorporateOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_number', models.CharField(max_length=200)),
                ('name_of_authorized_signatory', models.CharField(max_length=200)),
                ('residential_address', models.CharField(max_length=1000)),
                ('gender', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=12)),
                ('phone_number', models.CharField(max_length=12)),
                ('means_of_identification', models.CharField(max_length=100)),
                ('identification', cloudinary.models.CloudinaryField(max_length=255, verbose_name='pdf')),
                ('signature', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('photograph', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('other_documents', models.ManyToManyField(to='website.ExtraDocument')),
            ],
        ),
        migrations.CreateModel(
            name='BusinessName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proposed_business_name', models.CharField(max_length=500)),
                ('proposed_company_name', models.CharField(max_length=500)),
                ('business_phone_number', models.CharField(max_length=12)),
                ('business_email', models.EmailField(max_length=12)),
                ('business_address', models.CharField(max_length=1000)),
                ('state', models.CharField(max_length=100)),
                ('nature_of_business', models.TextField(max_length=1000)),
                ('business_commencement_date', models.DateTimeField()),
                ('is_individual_owner', models.BooleanField()),
                ('is_corporate_owner', models.BooleanField()),
                ('date_created', models.DateTimeField(default=datetime.datetime(2021, 10, 31, 15, 30, 43, 113276))),
                ('last_created', models.DateTimeField(default=datetime.datetime(2021, 10, 31, 15, 30, 43, 113289))),
                ('attestee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.attestee')),
                ('corporate_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.corporateowner')),
                ('individual_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.individualowner')),
            ],
        ),
    ]
