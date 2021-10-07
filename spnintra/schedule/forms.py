from django import forms

#=====================================================================================
# 定数
#=====================================================================================
MONOTH_CHOICES = (
    (1, '1月'),
    (2, '2月'),
    (3, '3月'),
    (4, '4月'),
    (5, '5月'),
    (6, '6月'),
    (7, '7月'),
    (8, '8月'),
    (9, '9月'),
    (10, '10月'),
    (11, '11月'),
    (13, '12月')
)

HOUR_CHOICES = (
    (99, '--時'),
    (0, '0時'),
    (1, '1時'),
    (2, '2時'),
    (3, '3時'),
    (4, '4時'),
    (5, '5時'),
    (6, '6時'),
    (7, '7時'),
    (8, '8時'),
    (98, '--時'),
    (9, '9時'),
    (10, '10時'),
    (11, '11時'),
    (12, '12時'),
    (13, '13時'),
    (14, '14時'),
    (15, '15時'),
    (16, '16時'),
    (17, '17時'),
    (18, '18時'),
    (19, '19時'),
    (20, '20時'),
    (21, '21時'),
    (22, '22時'),
    (23, '23時')
)

MINUTE_CHOICES = (
    (99, '--分'),
    (0, '00分'),
    (15, '15分'),
    (30, '30分'),
    (45, '45分')
)

#=====================================================================================
# バリデーション
#=====================================================================================

#=====================================================================================
# メインクラス
#=====================================================================================
class ScheduleRegistForm(forms.Form):
    # 開始年月日
    f_s_year = forms.ChoiceField(widget=forms.widgets.Select)
    f_s_month = forms.ChoiceField(widget=forms.widgets.Select, choices=MONOTH_CHOICES)
    f_s_day = forms.ChoiceField(widget=forms.widgets.Select)

    # 終了年月日
    f_e_year = forms.ChoiceField(widget=forms.widgets.Select)
    f_e_month = forms.ChoiceField(widget=forms.widgets.Select, choices=MONOTH_CHOICES)
    f_e_day = forms.ChoiceField(widget=forms.widgets.Select)

    # 開始時分
    f_s_hour = forms.ChoiceField(widget=forms.widgets.Select, choices=HOUR_CHOICES)
    f_s_minutes = forms.ChoiceField(widget=forms.widgets.Select, choices=MINUTE_CHOICES)

    # 終了時分
    f_e_hour = forms.ChoiceField(widget=forms.widgets.Select, choices=HOUR_CHOICES)
    f_e_minutes = forms.ChoiceField(widget=forms.widgets.Select, choices=MINUTE_CHOICES)

    # 会社情報
    f_company = forms.CharField(max_length=50)

    # 予定（タグ、タイトル、メモ）
    f_tag = forms.ChoiceField(widget=forms.widgets.Select)
    f_title = forms.CharField(max_length=24)
    f_memo = forms.CharField(max_length=2048, widget=forms.Textarea)

    # 参加者（参加者リスト左右、ユーザー検索、グループ）
    f_member_l = forms.MultipleChoiceField()
    f_member_r = forms.MultipleChoiceField()
    f_user = forms.CharField(max_length=50)
    f_member_gr = forms.ChoiceField(widget=forms.widgets.Select)

    # 施設（施設リスト左右、グループ）
    f_setu_l = forms.MultipleChoiceField()
    f_setu_r = forms.MultipleChoiceField()
    f_setu_gr = forms.ChoiceField(widget=forms.widgets.Select)

    # ファイル
    f_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        # 年月日設定
        wk_date_year = kwargs.pop('date_year')
        wk_date_day = kwargs.pop('date_day')

        wk_date_year_select = kwargs.pop('date_year_select')
        wk_date_month_select = kwargs.pop('date_month_select')
        wk_date_day_select = kwargs.pop('date_day_select')

        self.base_fields['f_s_year'].choices = wk_date_year
        self.base_fields['f_s_year'].initial = wk_date_year_select
        self.base_fields['f_s_month'].initial = wk_date_month_select
        self.base_fields['f_s_day'].choices = wk_date_day
        self.base_fields['f_s_day'].initial = wk_date_day_select

        self.base_fields['f_e_year'].choices = wk_date_year
        self.base_fields['f_e_year'].initial = wk_date_year_select
        self.base_fields['f_e_month'].initial = wk_date_month_select
        self.base_fields['f_e_day'].choices = wk_date_day
        self.base_fields['f_e_day'].initial = wk_date_day_select

        # 予定タグ設定
        self.base_fields['f_tag'].choices = kwargs.pop('yotei_cat')

        # 参加者グループ設定
        self.base_fields['f_member_gr'].choices = kwargs.pop('disp_gr')
        self.base_fields['f_member_gr'].initial = kwargs.pop('disp_gr_select')
        self.base_fields['f_member_r'].choices = kwargs.pop('gr_member')
        self.base_fields['f_member_l'].choices = kwargs.pop('my_account')

        # 施設グループ設定
        setu_gr = kwargs.pop('setu_gr')
        setu_member = kwargs.pop('setu_member')
        if setu_gr is not None:
            self.base_fields['f_setu_gr'].choices = setu_gr
        if setu_member is not None:
            self.base_fields['f_setu_r'].choices = setu_member

        # css属性追加
        self.base_fields['f_title'].widget.attrs['class'] = 'regist-yotei-title'
        self.base_fields['f_memo'].widget.attrs['class'] = 'regist-yotei-memo'
        self.base_fields['f_member_l'].widget.attrs['class'] = 'regist_select'
        self.base_fields['f_member_r'].widget.attrs['class'] = 'regist_select'
        self.base_fields['f_setu_l'].widget.attrs['class'] = 'regist_select'
        self.base_fields['f_setu_r'].widget.attrs['class'] = 'regist_select'
        self.base_fields['f_member_l'].widget.attrs['size'] = 10
        self.base_fields['f_member_r'].widget.attrs['size'] = 6
        self.base_fields['f_setu_l'].widget.attrs['size'] = 10
        self.base_fields['f_setu_r'].widget.attrs['size'] = 6
        self.base_fields['f_member_gr'].widget.attrs['class'] = 'regist_select'
        self.base_fields['f_setu_gr'].widget.attrs['class'] = 'regist_select'

        super().__init__(*args, **kwargs)

