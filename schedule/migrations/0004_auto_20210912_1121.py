# Generated by Django 2.2.2 on 2021-09-12 02:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_auto_20210912_1118'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mstscheduletype',
            old_name='sisp_order',
            new_name='disp_order',
        ),
        migrations.RenameField(
            model_name='trnschedulemmember',
            old_name='sisp_order',
            new_name='disp_order',
        ),
        migrations.RenameField(
            model_name='trnschedulemmembernormal',
            old_name='sisp_order',
            new_name='disp_order',
        ),
        migrations.RenameField(
            model_name='trnschedulemmemberrepeat',
            old_name='sisp_order',
            new_name='disp_order',
        ),
        migrations.RenameField(
            model_name='trnschedulemmemberspan',
            old_name='sisp_order',
            new_name='disp_order',
        ),
    ]
