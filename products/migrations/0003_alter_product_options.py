# Generated by Django 3.2.20 on 2023-08-20 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20230818_1217'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['title']},
        ),
    ]