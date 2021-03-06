# Generated by Django 2.2.2 on 2021-09-12 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_auto_20210909_0000'),
    ]

    operations = [
        migrations.AddField(
            model_name='trnschedulemmember',
            name='sisp_order',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='表示順'),
        ),
        migrations.AddField(
            model_name='trnschedulemmembernormal',
            name='sisp_order',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='表示順'),
        ),
        migrations.AddField(
            model_name='trnschedulemmemberrepeat',
            name='sisp_order',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='表示順'),
        ),
        migrations.AddField(
            model_name='trnschedulemmemberspan',
            name='sisp_order',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='表示順'),
        ),
    ]
