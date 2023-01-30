# Generated by Django 3.2 on 2023-01-28 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20230128_1327'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={},
        ),
        migrations.RemoveConstraint(
            model_name='review',
            name='unique review',
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('title', 'author'), name='unique_review'),
        ),
    ]
