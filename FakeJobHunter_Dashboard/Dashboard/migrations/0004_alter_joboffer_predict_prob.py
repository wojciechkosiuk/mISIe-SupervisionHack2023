# Generated by Django 4.1 on 2023-05-21 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0003_alter_joboffer_explain_alter_joboffer_lokalizacja_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joboffer',
            name='Predict_Prob',
            field=models.FloatField(null=True),
        ),
    ]