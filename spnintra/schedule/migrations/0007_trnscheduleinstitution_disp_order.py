# Generated by Django 2.2.2 on 2021-09-26 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0006_auto_20210926_0841'),
    ]

    operations = [
        migrations.AddField(
            model_name='trnscheduleinstitution',
            name='disp_order',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='表示順'),
        ),
    ]
