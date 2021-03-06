# Generated by Django 2.2.2 on 2021-09-08 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trnschedulecontinue',
            name='continue_schedule_chg',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='更新者'),
        ),
        migrations.AddField(
            model_name='trnschedulecontinue',
            name='continue_schedule_chg_dt',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='更新日時'),
        ),
        migrations.AddField(
            model_name='trnschedulenormal',
            name='normal_schedule_chg',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='更新者'),
        ),
        migrations.AddField(
            model_name='trnschedulenormal',
            name='normal_schedule_chg_dt',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='更新日時'),
        ),
        migrations.AddField(
            model_name='trnschedulerepeat',
            name='repeat_schedule_chg',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='更新者'),
        ),
        migrations.AddField(
            model_name='trnschedulerepeat',
            name='repeat_schedule_chg_dt',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='更新日時'),
        ),
        migrations.AddField(
            model_name='trnschedulespan',
            name='span_schedule_chg',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='更新者'),
        ),
        migrations.AddField(
            model_name='trnschedulespan',
            name='span_schedule_chg_dt',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='更新日時'),
        ),
    ]
