# Generated by Django 4.0.6 on 2022-07-22 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_add_slug_to_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='zip_code',
            field=models.CharField(default='zip', max_length=255),
            preserve_default=False,
        ),
    ]