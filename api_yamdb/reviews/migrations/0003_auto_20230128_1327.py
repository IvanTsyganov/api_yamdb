# Generated by Django 3.2 on 2023-01-28 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ('-pub_date', 'score')},
        ),
        migrations.RemoveConstraint(
            model_name='review',
            name='unique_review',
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('title', 'author'), name='unique review'),
        ),
    ]
