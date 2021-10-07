from accounts.models import CustomUser
from django.db import models

#アカウント登録マスタ
class MstAccount(models.Model):
    account_cd = models.CharField(verbose_name='アカウントコード', primary_key=True, unique=True, max_length=5)
    disp_name = models.CharField(verbose_name='表示名', default='', max_length=50)
    disp_name_yomi = models.CharField(verbose_name='ふりがな', default='', max_length=50)
    use_func_type_cd = models.CharField(verbose_name='使用機能種別コード', null=True, blank=True, default='99999', max_length=5)
    officer_cd = models.CharField(verbose_name='役職コード', null=True, blank=True, default='99999', max_length=5)
    default_group_cd = models.CharField(verbose_name='デフォルトグループコード', null=True, blank=True, default='99999', max_length=5)
    default_company_cd = models.CharField(verbose_name='デフォルト会社コード', null=True, blank=True, default='99999', max_length=5)
    icon_file_url = models.ImageField(verbose_name='icon画像', null=True, blank=True, upload_to=None, height_field=None, width_field=None, max_length=256)
    user_id = models.ForeignKey(CustomUser, verbose_name='ユーザID', null=True, blank=True, on_delete=models.PROTECT)
    create_dt = models.DateTimeField(verbose_name='作成日', null=True, blank=True, auto_now=False, auto_now_add=False)
    create_account = models.CharField(verbose_name='作成者', null=True, blank=True, max_length=5)
    is_valid = models.BooleanField(verbose_name='無効フラグ', default=False)
    delete_dt = models.DateTimeField(verbose_name='失効日', null=True, blank=True, auto_now=False, auto_now_add=False)
    delete_memo = models.CharField(verbose_name='失効理由', null=True, blank=True, default='', max_length=16)
    last_login_dt = models.DateTimeField(verbose_name='最終ログイン', null=True, blank=True, auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name_plural = 'アカウント'

    def __str__(self):
        return self.account_cd

#管理者マスタ
class MstAdmin(models.Model):
    account_id = models.AutoField(verbose_name='ID', primary_key=True, unique=True)
    account_cd = models.CharField(verbose_name='アカウントコード', default='', max_length=5)

    class Meta:
        verbose_name_plural = '管理者マスタ'

    def __str__(self):
        return self.account_id

#使用機能種別マスタ
class MstUseFncType(models.Model):
    use_func_type_cd = models.CharField(verbose_name='使用機能種別コード', primary_key=True, unique=True, max_length=5)
    use_func_type_name = models.CharField(verbose_name='使用機能種別名', default='', max_length=24)
    disp_order = models.PositiveIntegerField(verbose_name='表示順', null=True, blank=True, default=0)
    is_fnc_t_schedule = models.BooleanField(verbose_name='スケジュール', default=True)
    is_fnc_t_file = models.BooleanField(verbose_name='ファイル管理', default=False)
    is_fnc_t_timecard = models.BooleanField(verbose_name='タイムカード', default=False)
    is_fnc_t_workflow = models.BooleanField(verbose_name='ワークフロー', default=False)
    is_fnc_t_infoboard = models.BooleanField(verbose_name='掲示板', default=True)
    is_fnc_t_message = models.BooleanField(verbose_name='メッセージ', default=True)
    is_fnc_t_mail = models.BooleanField(verbose_name='メール', default=False)
    is_fnc_t_task = models.BooleanField(verbose_name='タスク管理', default=True)
    is_fnc_t_equipment = models.BooleanField(verbose_name='備品管理', default=False)
    is_fnc_t_employee_info = models.BooleanField(verbose_name='社員情報', default=False)
    is_fnc_t_employee = models.BooleanField(verbose_name='社員評価', default=False)

    class Meta:
        verbose_name_plural = '使用機能種別マスタ'

    def __str__(self):
        return self.use_func_type_cd

#グループマスタ
class MstGroup(models.Model):
    group_cd = models.CharField(verbose_name='グループコード', primary_key=True, unique=True, max_length=5)
    group_name = models.CharField(verbose_name='グループ名', default='', max_length=24)
    disp_order = models.PositiveIntegerField(verbose_name='表示順', null=True, blank=True, default=0)

    class Meta:
        verbose_name_plural = 'グループマスタ'

    def __str__(self):
        return self.group_cd

#グループ登録マスタ
class MstBelongGroup(models.Model):
    belong_group_id = models.AutoField(verbose_name='ID', primary_key=True, unique=True)
    group_cd = models.CharField(verbose_name='グループコード', default='', max_length=5)
    account_cd = models.CharField(verbose_name='アカウントコード', default='', max_length=5)

    class Meta:
        verbose_name_plural = 'グループ登録マスタ'

    def __str__(self):
        return self.belong_group_id

#役職マスタ
class MstOfficer(models.Model):
    officer_cd = models.AutoField(verbose_name='役職コード', primary_key=True, unique=True)
    officer_name = models.CharField(verbose_name='役職名', default='', max_length=24)
    disp_order = models.PositiveIntegerField(verbose_name='表示順', null=True, blank=True, default=0)
    officer_level = models.PositiveIntegerField(verbose_name='役職レベル', null=True, blank=True, default=0)

    class Meta:
        verbose_name_plural = '役職マスタ'

    def __str__(self):
        return self.officer_cd

#部署マスタ
class MstDepartment(models.Model):
    department_cd = models.CharField(verbose_name='部署コード', primary_key=True, unique=True, max_length=5)
    department_name = models.CharField(verbose_name='署名', default='', max_length=24)
    disp_order = models.PositiveIntegerField(verbose_name='表示順', null=True, blank=True, default=0)

    class Meta:
        verbose_name_plural = '部署登録マスタ'

    def __str__(self):
        return self.department_cd

#部署登録マスタ
class MstBelongDepartment(models.Model):
    belong_department_id = models.AutoField(verbose_name='ID', primary_key=True, unique=True)
    department_cd = models.CharField(verbose_name='部署コード', default='', max_length=5)
    account_cd = models.CharField(verbose_name='アカウントコード', default='', max_length=5)
    officer_cd = models.CharField(verbose_name='役職コード', default='', max_length=5)

    class Meta:
        verbose_name_plural = '部署登録マスタ'

    def __str__(self):
        return self.belong_department_id

#プロジェクト設定マスタ
class MstProjectConfig(models.Model):
    pj_config_id = models.AutoField(verbose_name='ID', primary_key=True, unique=True)
    pj_config_kubun_cd = models.CharField(verbose_name='区分ID', default='', max_length=8)
    pj_config_key = models.CharField(verbose_name='キー項目', default='', max_length=8)
    pj_config_value = models.CharField(verbose_name='設定値', default='', max_length=16)
    pj_config_memo = models.CharField(verbose_name='メモ', default='', max_length=32)

    class Meta:
        verbose_name_plural = 'プロジェクト設定マスタ'

    def __str__(self):
        return self.belong_department_id





