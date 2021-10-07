from accounts.models import CustomUser
from django.db import models

#スケジュール(通常)
class TrnScheduleNormal(models.Model):
    normal_schedule_cd = models.CharField(verbose_name='通常スケジュールコード', primary_key=True, unique=True, max_length=8)
    normal_schedule_date = models.DateField(verbose_name='日付', default='1900-01-01')
    normal_schedule_s_time = models.TimeField(verbose_name='開始時刻', null=True, blank=True)
    normal_schedule_e_time = models.TimeField(verbose_name='終了時刻', null=True, blank=True)
    company_cd = models.CharField(verbose_name='会社コード', null=True, blank=True, max_length=5)
    schedule_type_cd = models.CharField(verbose_name='予定コード', null=True, blank=True, max_length=5)
    normal_schedule_name = models.CharField(verbose_name='予定名', null=True, blank=True, max_length=24)
    normal_schedule_memo = models.CharField(verbose_name='メモ', null=True, blank=True, max_length=2048)
    normal_schedule_register = models.CharField(verbose_name='登録者', null=True, blank=True, max_length=5)
    normal_schedule_regist_dt = models.DateTimeField(verbose_name='登録日時', null=True, blank=True)
    normal_schedule_chg = models.CharField(verbose_name='更新者', null=True, blank=True, max_length=5)
    normal_schedule_chg_dt = models.DateTimeField(verbose_name='更新日時', null=True, blank=True)
    is_normal_schedule_release = models.BooleanField(verbose_name='公開/非公開', null=True, blank=True, default=True)

    class Meta:
        verbose_name_plural = 'スケジュール(通常)'

    def __str__(self):
        return self.normal_schedule_cd

#スケジュール(継続)
class TrnScheduleContinue(models.Model):
    continue_schedule_cd = models.CharField(verbose_name='継続スケジュールコード', primary_key=True, unique=True, max_length=8)
    continue_schedule_s_date = models.DateField(verbose_name='開始日', default='1900-01-01')
    continue_schedule_s_time = models.TimeField(verbose_name='開始時刻', null=True, blank=True)
    continue_schedule_e_date = models.DateField(verbose_name='終了日', default='1900-01-01')
    continue_schedule_e_time = models.TimeField(verbose_name='終了時刻', null=True, blank=True)
    company_cd = models.CharField(verbose_name='会社コード', null=True, blank=True, max_length=5)
    schedule_type_cd = models.CharField(verbose_name='予定コード', null=True, blank=True, max_length=5)
    continue_schedule_name = models.CharField(verbose_name='予定名', null=True, blank=True, max_length=24)
    continue_schedule_memo = models.CharField(verbose_name='メモ', null=True, blank=True, max_length=2048)
    continue_schedule_register = models.CharField(verbose_name='登録者', null=True, blank=True, max_length=5)
    continue_schedule_regist_dt = models.DateTimeField(verbose_name='登録日時', null=True, blank=True)
    continue_schedule_chg = models.CharField(verbose_name='更新者', null=True, blank=True, max_length=5)
    continue_schedule_chg_dt = models.DateTimeField(verbose_name='更新日時', null=True, blank=True)
    is_continue_schedule_release = models.BooleanField(verbose_name='公開/非公開', null=True, blank=True, default=True)

    class Meta:
        verbose_name_plural = 'スケジュール(継続)'

    def __str__(self):
        return self.continue_schedule_cd

#スケジュール(期間)
class TrnScheduleSpan(models.Model):
    span_schedule_cd = models.CharField(verbose_name='期間スケジュールコード', primary_key=True, unique=True, max_length=8)
    span_schedule_s_date = models.DateField(verbose_name='開始日', default='1900-01-01')
    span_schedule_e_date = models.DateField(verbose_name='終了日', default='1900-01-01')
    company_cd = models.CharField(verbose_name='会社コード', null=True, blank=True, max_length=5)
    schedulse_type_cd = models.CharField(verbose_name='予定コード', null=True, blank=True, max_length=5)
    span_schedule_name = models.CharField(verbose_name='予定名', null=True, blank=True, max_length=24)
    span_schedule_memo = models.CharField(verbose_name='メモ', null=True, blank=True, max_length=2048)
    span_schedule_register = models.CharField(verbose_name='登録者', null=True, blank=True, max_length=5)
    span_schedule_regist_dt = models.DateTimeField(verbose_name='登録日時', null=True, blank=True)
    span_schedule_chg = models.CharField(verbose_name='更新者', null=True, blank=True, max_length=5)
    span_schedule_chg_dt = models.DateTimeField(verbose_name='更新日時', null=True, blank=True)
    is_span_schedule_release = models.BooleanField(verbose_name='公開/非公開', null=True, blank=True, default=True)

    class Meta:
        verbose_name_plural = 'スケジュール(期間)'

    def __str__(self):
        return self.span_schedule_cd

#スケジュール(リピート)
class TrnScheduleRepeat(models.Model):
    repeat_schedule_cd = models.CharField(verbose_name='リピートスケジュールコード', primary_key=True, unique=True, max_length=8)
    repeat_schedule_type = models.PositiveIntegerField(verbose_name='繰り返し条件種別', default=0)
    repeat_schedule_ditail = models.PositiveIntegerField(verbose_name='繰り返し詳細1', default=0)
    repeat_schedule_ditail2 = models.PositiveIntegerField(verbose_name='繰り返し詳細2', default=0)
    repeat_schedule_businessday = models.PositiveIntegerField(verbose_name='営業日判定', default=0)
    is_repeat_limit = models.BooleanField(verbose_name='期限有無', null=True, blank=True, default=False)
    repeat_limit_date = models.DateField(verbose_name='期限', null=True, blank=True, default='9999-12-31')
    repeat_schedule_s_dt = models.TimeField(verbose_name='開始時刻', null=True, blank=True)
    repeat_schedule_e_dt = models.TimeField(verbose_name='終了時刻', null=True, blank=True)
    company_cd = models.CharField(verbose_name='会社コード', null=True, blank=True, max_length=5)
    schedulse_type_cd = models.CharField(verbose_name='予定コード', null=True, blank=True, max_length=5)
    repeat_schedule_name = models.CharField(verbose_name='予定名', null=True, blank=True, max_length=24)
    repeat_schedule_memo = models.CharField(verbose_name='メモ', null=True, blank=True, max_length=2048)
    repeat_schedule_register = models.CharField(verbose_name='登録者', null=True, blank=True, max_length=5)
    repeat_schedule_regist_dt = models.DateTimeField(verbose_name='登録日時', null=True, blank=True)
    repeat_schedule_chg = models.CharField(verbose_name='更新者', null=True, blank=True, max_length=5)
    repeat_schedule_chg_dt = models.DateTimeField(verbose_name='更新日時', null=True, blank=True)
    is_repeat_schedule_release = models.BooleanField(verbose_name='公開/非公開', null=True, blank=True, default=True)

    class Meta:
        verbose_name_plural = 'スケジュール(リピート)'

    def __str__(self):
        return self.repeat_schedule_cd

#スケジュール参加者(通常)
class TrnScheduleMmemberNormal(models.Model):
    schedule_member_id = models.AutoField(verbose_name='ID', primary_key=True, unique=True)
    normal_schedule_cd = models.ForeignKey(TrnScheduleNormal, null=True, blank=True, on_delete=models.CASCADE)
    account_cd = models.CharField(verbose_name='アカウントコード', default='', max_length=5)
    disp_order = models.PositiveIntegerField(verbose_name='表示順', null=True, blank=True, default=0)

    class Meta:
        verbose_name_plural = 'スケジュール参加者(通常)'

    def __str__(self):
        return self.schedule_member_id

#スケジュール参加者(継続)
class TrnScheduleMmember(models.Model):
    schedule_member_id = models.AutoField(verbose_name='ID', primary_key=True, unique=True)
    continue_schedule_cd = models.ForeignKey(TrnScheduleContinue, null=True, blank=True, on_delete=models.CASCADE)
    account_cd = models.CharField(verbose_name='アカウントコード', default='', max_length=5)
    disp_order = models.PositiveIntegerField(verbose_name='表示順', null=True, blank=True, default=0)

    class Meta:
        verbose_name_plural = 'スケジュール参加者(継続)'

    def __str__(self):
        return self.schedule_member_id

#スケジュール参加者(期間)
class TrnScheduleMmemberSpan(models.Model):
    schedule_member_id = models.AutoField(verbose_name='ID', primary_key=True, unique=True)
    span_schedule_cd = models.ForeignKey(TrnScheduleSpan, null=True, blank=True, on_delete=models.CASCADE)
    account_cd = models.CharField(verbose_name='アカウントコード', default='', max_length=5)
    disp_order = models.PositiveIntegerField(verbose_name='表示順', null=True, blank=True, default=0)

    class Meta:
        verbose_name_plural = 'スケジュール参加者(期間)'

    def __str__(self):
        return self.schedule_member_id

#スケジュール参加者(リピート)
class TrnScheduleMmemberRepeat(models.Model):
    schedule_member_id = models.AutoField(verbose_name='ID', primary_key=True, unique=True)
    repeat_schedule_cd = models.ForeignKey(TrnScheduleRepeat, null=True, blank=True, on_delete=models.CASCADE)
    account_cd = models.CharField(verbose_name='アカウントコード', default='', max_length=5)
    disp_order = models.PositiveIntegerField(verbose_name='表示順', null=True, blank=True, default=0)

    class Meta:
        verbose_name_plural = 'スケジュール参加者(リピート)'

    def __str__(self):
        return self.schedule_member_id

#スケジュール施設
class TrnScheduleInstitution(models.Model):
    schedule_id = models.AutoField(verbose_name='ID', primary_key=True, unique=True)
    schedule_cd = models.CharField(verbose_name='スケジュールコード', default='', max_length=8)
    schedule_type = models.PositiveIntegerField(verbose_name='スケジュール種別', default=1)
    institution_cd = models.CharField(verbose_name='施設コード', null=True, blank=True, max_length=5)
    disp_order = models.PositiveIntegerField(verbose_name='表示順', null=True, blank=True, default=0)

    class Meta:
        verbose_name_plural = 'スケジュール施設'

    def __str__(self):
        return self.schedule_id

#スケジュールファイル
class TrnScheduleFile(models.Model):
    schedule_id = models.AutoField(verbose_name='ID', primary_key=True, unique=True)
    schedule_cd = models.CharField(verbose_name='スケジュールコード', default='', max_length=8)
    schedule_type = models.PositiveIntegerField(verbose_name='スケジュール種別', default=1)
    schedule_file_name = models.CharField(verbose_name='ファイル名', default='', max_length=256)
    schedule_file_url = models.CharField(verbose_name='保存先', default='', max_length=256)

    class Meta:
        verbose_name_plural = 'スケジュールファイル'

    def __str__(self):
        return self.schedule_id

#予定メニュー登録マスタ
class MstScheduleType(models.Model):
    schedule_type_cd = models.CharField(verbose_name='予定コード', primary_key=True, unique=True, max_length=5)
    schedule_type_name = models.CharField(verbose_name='表示名', default='', max_length=24)
    disp_order = models.PositiveIntegerField(verbose_name='表示順', null=True, blank=True, default=0)
    schedule_type_color_cd = models.CharField(verbose_name='予定色コード', null=True, blank=True, max_length=5)

    class Meta:
        verbose_name_plural = '予定メニュー登録マスタ'

    def __str__(self):
        return self.schedule_type_cd

#予定色マスタ
class MstScheduleTypeColor(models.Model):
    schedule_type_color_cd = models.CharField(verbose_name='予定色コード', primary_key=True, unique=True, max_length=5)
    schedule_type_rgb = models.CharField(verbose_name='予定色RGBコード', default='', max_length=7)
    schedule_type_bg_rgb = models.CharField(verbose_name='予定色背景RGBコード', default='', max_length=7)
    disp_order = models.PositiveIntegerField(verbose_name='表示順', null=True, blank=True, default=0)
    schedule_type_color_discription = models.CharField(verbose_name='説明', null=True, blank=True, max_length=12)

    class Meta:
        verbose_name_plural = '予定色マスタ'

    def __str__(self):
        return self.schedule_type_color_cd

#施設グループ登録マスタ
class MstInstitutionGroup(models.Model):
    institution_group_cd = models.CharField(verbose_name='施設グループコード', primary_key=True, unique=True, max_length=5)
    institution_group_name = models.CharField(verbose_name='施設グループ名', default='', max_length=24)
    institution_group_disp_order = models.PositiveIntegerField(verbose_name='表示順', null=True, blank=True, default=0)
    institution_group_memo = models.CharField(verbose_name='メモ', null=True, blank=True, max_length=2048)

    class Meta:
        verbose_name_plural = '施設グループ登録マスタ'

    def __str__(self):
        return self.institution_group_cd

#施設登録マスタ
class MstInstitution(models.Model):
    institution_cd = models.CharField(verbose_name='施設コード', primary_key=True, unique=True, max_length=5)
    institution_name = models.CharField(verbose_name='施設名', default='', max_length=24)
    disp_order = models.PositiveIntegerField(verbose_name='表示順', default=0)
    institution_group_cd = models.CharField(verbose_name='施設グループコード', null=True, blank=True, max_length=5)
    institution_memo = models.CharField(verbose_name='メモ', null=True, blank=True, max_length=2048)

    class Meta:
        verbose_name_plural = '施設登録マスタ'

    def __str__(self):
        return self.institution_cd

#会社登録マスタ
class MstCompany(models.Model):
    company_cd = models.CharField(verbose_name='会社コード', primary_key=True, unique=True, max_length=5)
    company_name = models.CharField(verbose_name='会社名', default='', max_length=50)
    company_name_s = models.CharField(verbose_name='会社名略称', default='', max_length=24)

    class Meta:
        verbose_name_plural = '会社登録マスタ'

    def __str__(self):
        return self.company_cd

#祝日登録マスタ
class MstHoliday(models.Model):
    holiday_cd = models.CharField(verbose_name='祝日コード', primary_key=True, unique=True, max_length=5)
    holiday_date = models.DateField(verbose_name='日付', default='1900-01-01')
    holiday_name = models.CharField(verbose_name='祝日名', default='', max_length=50)

    class Meta:
        verbose_name_plural = '祝日登録マスタ'

    def __str__(self):
        return self.holiday_cd







