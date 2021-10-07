from django.http import HttpResponse
from django.shortcuts import render
from urllib.parse import urlencode
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.functional import cached_property
# モデルインポート
from overview.models import *
from schedule.models import *
# 標準インポート
from django.db.models import F
import datetime
import time
# オリジナルライブラリインポート
from commonutil.libraries import *
#この下はお試し用

#=====================================================================================
# グループ週画面（スケジュールメイン） ※ログインしていないと見れないページ
#=====================================================================================
class ScheduleIndexView(LoginRequiredMixin, TemplateView):
    template_name = "schedule.html"

    # ---------------------------------------------------------------------------------
    # 関数名：URLパラメータ取得　※HTML使用
    # ---------------------------------------------------------------------------------
    def get_url_gr(self):
        return lib_get_url_gr(self)

    #---------------------------------------------------------------------------------
    # 関数名：全グループ情報取得
    # 引　数：なし
    # 戻り値：グループマスタ全グループ取得情報
    # 備　考：表示順にて並び替え
    #---------------------------------------------------------------------------------
    @cached_property # リクエスト単位でキャッシュ
    def get_group_list(self):
        # 戻り構造体
        st_gr_list_i = []

        # DBアクセス【グループマスタ】
        q_gr_list = MstGroup.objects.order_by('disp_order')

        for value in q_gr_list:
            st_gr_i = StGroupListInfo()
            st_gr_i.group_cd = value.group_cd
            st_gr_i.group_name = value.group_name

            # リダイレクトパラメ―タ作成
            # gr=グループID（DB値）
            # trday=対象日（URLパラメータ）
            query_string = urlencode({'gr': value.group_cd, 'trday': lib_get_url_trday(self)})

            # URLを逆引きして、パラメータを追加　※遷移先は詳細
            url = reverse('schedule:schedule_index') + f'?{query_string}'
            st_gr_i.group_url = url

            # 構造体へ追加
            st_gr_list_i.append(st_gr_i)

        return st_gr_list_i

    #---------------------------------------------------------------------------------
    # 関数名：予定作成リンクパラメータ作成
    # 引　数：なし
    # 戻り値：リンクパラメータ
    # 備　考：
    #---------------------------------------------------------------------------------
    @cached_property # リクエスト単位でキャッシュ
    def get_regist_link_i(self):
        # 変数初期化
        gr_code = lib_get_url_gr(self)              # 表示対象グループコード
        my_account_i = lib_get_my_account_i(self)   # 自分のアカウント情報

        # 基準日作成
        url_param = lib_get_url_trday(self)
        dt = datetime.date(int(url_param[0:4]), int(url_param[5:7]), int(url_param[8:10]))

        # 予定登録リンク用URLパラメータ作成
        return '?id=' + my_account_i.account_cd + '&trday=' + dt.strftime('%Y.%m.%d') + '&PP=gw&PPGr=' + gr_code + '&schty=nml'

    #---------------------------------------------------------------------------------
    # 関数名：基準日表示用データ作成
    # 引　数：なし
    # 戻り値：表示用データ文字列
    # 備　考：表示形式 ⇒ YYYY 年 MM 月 DD 日 ( aa )
    #---------------------------------------------------------------------------------
    @cached_property # リクエスト単位でキャッシュ
    def get_day_i(self):
        return lib_get_day_i(self)

    #---------------------------------------------------------------------------------
    # 関数名：日付変更リンクのURL遷移パラメータ作成（前週、前日、本日、明日、次週）
    # 引　数：なし
    # 戻り値：日付変更リンクのURL遷移パラメータ構造体【StTranInfo】
    # 備　考：URLに直接出力できる形式の文字列として作成
    #---------------------------------------------------------------------------------
    @cached_property # リクエスト単位でキャッシュ
    def get_tran_i(self):
        # 戻り構造体
        st_tran_i = StTranInfo()

        # グループ指定
        gr_cd = lib_get_url_gr(self)

        # 基準日作成
        url_param = lib_get_url_trday(self)
        dt = datetime.date(int(url_param[0:4]), int(url_param[5:7]), int(url_param[8:10]))

        # 遷移パラメータ作成（前週、前日、本日、明日、次週）
        st_tran_i.pre_week_ymd = '?gr=' + gr_cd + '&trday=' + lib_chg_day(dt, -7).strftime('%Y.%m.%d')
        st_tran_i.pre_day_ymd = '?gr=' + gr_cd + '&trday=' + lib_chg_day(dt, -1).strftime('%Y.%m.%d')
        st_tran_i.today_ymd = '?gr=' + gr_cd + '&trday=' + lib_chg_day(datetime.date.today(), 0).strftime('%Y.%m.%d')
        st_tran_i.next_day_ymd = '?gr=' + gr_cd + '&trday=' + lib_chg_day(dt, 1).strftime('%Y.%m.%d')
        st_tran_i.next_week_ymd = '?gr=' + gr_cd + '&trday=' + lib_chg_day(dt, 7).strftime('%Y.%m.%d')

        return st_tran_i

    #---------------------------------------------------------------------------------
    # 関数名：表ヘッダ情報作成
    # 引　数：なし
    # 戻り値：表ヘッダ情報構造体【StHeaderInfoの配列】
    # 備　考：表示色変更用CSSのクラス文字列も作成する
    #---------------------------------------------------------------------------------
    @cached_property # リクエスト単位でキャッシュ
    def get_head_i(self):
        # 戻り構造体
        st_head_i = []

        # 基準日作成
        url_param = lib_get_url_trday(self)
        dt = datetime.date(int(url_param[0:4]), int(url_param[5:7]), int(url_param[8:10]))

        # １週間分ループ
        for iLoop in range(7):
            # 戻り構造体
            st_head_wk = StHeaderInfo()

            # 基準日作成
            dt_wk = lib_chg_day(dt, iLoop)

            # 日付のみ
            st_head_wk.day = dt_wk.strftime('%d').lstrip("0")

            # 曜日（日本語表記）
            st_head_wk.day_of_week = lib_chg_youbi_eng_to_jpn(dt_wk.strftime('%a'))

            # DBアクセス【祝日登録マスタ】：日付指定して祝日情報取得
            q_holiday = MstHoliday.objects.filter(holiday_date=dt_wk)

            # 祝日：祝日登録マスタに対象日がある場合、もしくは日曜日
            if q_holiday.exists() or st_head_wk.day_of_week == '日':
                st_head_wk.day_type = 'cl-holiday'
            # 土曜
            elif st_head_wk.day_of_week == '土':
                st_head_wk.day_type = 'cl-saturday'
            # 平日
            else:
                st_head_wk.day_type = 'cl-weekday'

            # 構造体へ追加
            st_head_i.append(st_head_wk)

        return st_head_i

    #---------------------------------------------------------------------------------
    # 関数名：行情報作成
    # 引　数：なし
    # 戻り値：行情報構造体【StOneAcountInfoの配列】
    # 備　考：ヘッダ業作成有無、期間予定含む
    #---------------------------------------------------------------------------------
    def get_member_i(self):
        # 変数初期化
        gr_code = lib_get_url_gr(self)              # 表示対象グループコード
        my_account_i = lib_get_my_account_i(self)   # 自分のアカウント情報
        row_counter = 0                             # 処理対象行番号
        holiday_flg = True                          # 初回祝日表示フラグ

        # 戻り構造体
        st_member_i = []

        # 基準日作成
        url_param = lib_get_url_trday(self)

        # スケジュール(期間)用開始終了日作成
        start_dt = datetime.date(int(url_param[0:4]), int(url_param[5:7]), int(url_param[8:10]))
        end_dt = lib_chg_day(start_dt, 6)

        # DBアクセス【グループ登録マスタ】：表示対象グループ情報取得
        q_gr_accounts = MstBelongGroup.objects.filter(group_cd=gr_code)

        # 表示対象グループに自アカウントが存在する場合、先頭に表示
        if q_gr_accounts.filter(account_cd=my_account_i.account_cd).count() > 0:
            st_one_account_wk = StOneAcountInfo()
            st_one_account_wk.head_flg = 1
            st_one_account_wk.icon_name = my_account_i.icon_file_url
            st_one_account_wk.disp_name = my_account_i.disp_name
            st_one_account_wk.month_link_i = '?id=' + my_account_i.account_cd + '&trday=' + url_param
            # １週間分スケジュール情報
            for iLoop in range(7):
                st_one_account_wk.oneday_other_i.\
                    append(self.get_sch_oneday_base_i(my_account_i.account_cd, url_param, iLoop, holiday_flg))

            # DBアクセス【スケジュール(期間)】
            q_sch_span = TrnScheduleSpan.objects.select_related().\
                filter(trnschedulemmemberspan__account_cd=my_account_i.account_cd, span_schedule_s_date__lte=end_dt, span_schedule_e_date__gte=start_dt)
            if q_sch_span.exists() :
                # スケジュール(期間)あり
                st_one_account_wk.sch_span_flg = 1
                for sch_spna_vale in q_sch_span:
                    st_one_account_wk.span_disp_i.append(self.get_sch_span_i(sch_spna_vale, start_dt, end_dt, my_account_i.account_cd))
            else:
                # スケジュール(期間)なし
                st_one_account_wk.sch_span_flg = 0

            # 初回祝日表示フラグOFF
            holiday_flg = False

            # １行情報作成完了
            st_member_i.append(st_one_account_wk)

        # 行カウンタインクリメント
        row_counter += 1

        # グループアカウント分ループ
        for account in q_gr_accounts :
            # 自アカウントは先頭のため、とばす
            if account.account_cd == my_account_i.account_cd:
                continue

            st_one_account_wk = StOneAcountInfo()

            # アカウント情報取得
            account_i = lib_get_account_i(account.account_cd)

            # 無効アカウントは、とばす
            if account_i.is_valid == True:
                continue

            # 先頭、自アカウントの直下、５データ置きにヘッダ情報を表示する（１：表示、０：非表示）
            if row_counter == 1 or row_counter % 6 == 0 :
                st_one_account_wk.head_flg = 1
            else:
                st_one_account_wk.head_flg = 0
            st_one_account_wk.icon_name = account_i.icon_file_url
            st_one_account_wk.disp_name = account_i.disp_name
            st_one_account_wk.month_link_i = '?id=' + account_i.account_cd + '&trday=' + url_param

            # １週間分スケジュール情報
            for iLoop in range(7):
                st_one_account_wk.oneday_other_i.\
                    append(self.get_sch_oneday_base_i(account_i.account_cd, url_param, iLoop, holiday_flg))

            # DBアクセス【スケジュール(期間)】
            q_sch_span = TrnScheduleSpan.objects.select_related(). \
                filter(trnschedulemmemberspan__account_cd=account_i.account_cd, span_schedule_s_date__lte=start_dt, span_schedule_e_date__gte=end_dt)
            if q_sch_span.exists():
                # スケジュール(期間)あり
                st_one_account_wk.sch_span_flg = 1
                for sch_spna_vale in q_sch_span:
                    st_one_account_wk.span_disp_i.append(self.get_sch_span_i(sch_spna_vale, start_dt, end_dt, account_i.account_cd))
            else:
                # スケジュール(期間)なし
                st_one_account_wk.sch_span_flg = 0

            # 初回祝日表示フラグOFF
            if holiday_flg == True:
                holiday_flg = False

            # １行情報作成完了
            st_member_i.append(st_one_account_wk)

            # 行カウンタインクリメント
            row_counter += 1

        return st_member_i

    #---------------------------------------------------------------------------------
    # 関数名：１日分の予定取得：祝日＆予定登録
    # 引　数：アカウントコード　｜　基準日　｜　基準日からの日数　｜　祝日表示フラグ
    # 戻り値：１日分の予定情報構造体【StOneDayWap】
    # 備　考：表示色変更用CSSのクラス文字列も作成する
    #---------------------------------------------------------------------------------
    def get_sch_oneday_base_i(self, account_cd, base_day, spandays, holiday_flg):
        # 戻り構造体
        st_o_day_wap = StOneDayWap()

        # 基準日作成
        base_dt = datetime.date(int(base_day[0:4]), int(base_day[5:7]), int(base_day[8:10]))
        tar_dt = lib_chg_day(base_dt, spandays)

        # 祝日名作成　※先頭行のみ
        st_o_day_wap.holiday_name = ''
        if holiday_flg == True:
            # DBアクセス【グループ登録マスタ】：祝日取得
            q_holiday = MstHoliday.objects.filter(holiday_date=tar_dt)
            if q_holiday.exists() :
                st_o_day_wap.holiday_name = q_holiday[0].holiday_name

        # 予定登録リンク用URLパラメータ作成
        st_o_day_wap.regist_link_info = '?id=' + account_cd + '&trday=' + tar_dt.strftime('%Y.%m.%d') + '&PP=gw&PPGr='\
                                        + lib_get_url_gr(self) + '&schty=nml'

        # 表示対象日作成
        st_o_day_wap.tar_day = tar_dt.strftime('%Y.%m.%d')

        # １日分スケジュール情報：詳細
        # DBアクセス【スケジュール(継続)】
        q_sch_cntinue = TrnScheduleContinue.objects.select_related().\
            filter(trnschedulemmember__account_cd=account_cd, continue_schedule_s_date__lte=tar_dt, continue_schedule_e_date__gte=tar_dt)
        for sch_cntinue_vale in q_sch_cntinue:
            st_o_day_wap.oneday_she_disp_i.append(self.get_sch_oneday_continue_i(sch_cntinue_vale, tar_dt, account_cd))

        # DBアクセス【スケジュール(通常)】
        q_sch_normal = TrnScheduleNormal.objects.select_related().\
            filter(trnschedulemmembernormal__account_cd=account_cd, normal_schedule_date=tar_dt).order_by(F('normal_schedule_s_time').asc(nulls_last=False))
        for sch_normal_vale in q_sch_normal:
            st_o_day_wap.oneday_she_disp_i.append(self.get_sch_oneday_normal_i(sch_normal_vale, tar_dt, account_cd))

        # DBアクセス【スケジュール(リピート)】★保留★
        #sch_repeat = TrnScheduleRepeat.objects.select_related().filter(trnschedulemmemberrepeat__account_cd=account_cd)

        return st_o_day_wap

    #---------------------------------------------------------------------------------
    # 関数名：１日分スケジュール情報：【スケジュール(継続)】
    # 引　数：クエリセット(対象日１スケジュール分)　｜　対象日(DateTime型)　｜　アカウントID
    # 戻り値：１日分の予定情報構造体【スケジュール(継続)】【StOneDayDetail】
    # 備　考：表示色変更用CSSのクラス文字列も作成する
    #---------------------------------------------------------------------------------
    def get_sch_oneday_continue_i(self, sch_cte_val, tar_dt, account_cd):
        # 戻り構造体
        st_cnt_detail = StOneDayDetail()

        # 予定種別：0＝繰り返し、1=翌日以降続く、2=通常
        st_cnt_detail.type = 0

        # 時間指定
        str_s_timespan = sch_cte_val.continue_schedule_s_date.strftime('%m').lstrip("0")\
                         + '/' + sch_cte_val.continue_schedule_s_date.strftime('%d').lstrip("0")
        str_e_timespan = sch_cte_val.continue_schedule_e_date.strftime('%m').lstrip("0") \
                         + '/' + sch_cte_val.continue_schedule_e_date.strftime('%d').lstrip("0")
        if sch_cte_val.continue_schedule_s_date == tar_dt and sch_cte_val.continue_schedule_s_time is not None:
            # 開始日かつ開始時刻ありの場合、開始時刻―終了日 ※開始書き換え
            str_s_timespan = sch_cte_val.continue_schedule_s_time.strftime('%H')\
                             + ':' + sch_cte_val.continue_schedule_s_time.strftime('%M')
        elif sch_cte_val.continue_schedule_e_date == tar_dt and sch_cte_val.continue_schedule_e_time is not None:
            # 終了日かつ終了時刻ありの場合、開始日―終了時刻　※終了書き換え
            str_e_timespan = sch_cte_val.continue_schedule_e_time.strftime('%H')\
                             + ':' + sch_cte_val.continue_schedule_e_time.strftime('%M')
        st_cnt_detail.timespan = str_s_timespan + '-' + str_e_timespan

        # 予定タイトル
        if len(sch_cte_val.continue_schedule_name) > 1 :
            st_cnt_detail.title = sch_cte_val.continue_schedule_name
        else:
            st_cnt_detail.title = '--'

        # 予定詳細表示リンク用URLパラメータ
        st_cnt_detail.detail_link_i = '?id=' + account_cd + '&trday=' + tar_dt.strftime('%Y.%m.%d') \
            + '&PP=gw&PPGr=' + lib_get_url_gr(self) + '' + '&schid=' +  sch_cte_val.continue_schedule_cd + '&schty=cte'

        # タグ名　※初期化
        st_cnt_detail.tag = ''
        # タグ背景色色コード　※初期化
        st_cnt_detail.tagcolor = ''
        # 予定背景色色コード　※初期化
        st_cnt_detail.bkcolor = ''

        # DBアクセス【予定メニュー登録マスタ】：表示名取得
        q_sch_type = MstScheduleType.objects.filter(schedule_type_cd=sch_cte_val.schedule_type_cd)
        if q_sch_type.exists():
            st_cnt_detail.tag = q_sch_type[0].schedule_type_name

            # DBアクセス【予定色マスタ】：予定色RGBコード取得
            q_sch_type_color = MstScheduleTypeColor.objects.filter(schedule_type_color_cd=q_sch_type[0].schedule_type_color_cd)
            if q_sch_type_color.exists():
                st_cnt_detail.tagcolor = q_sch_type_color[0].schedule_type_rgb
                st_cnt_detail.bkcolor = q_sch_type_color[0].schedule_type_bg_rgb

        # 期間重複警告アイコン表示有無★保留★
        st_cnt_detail.warning_icon = ''

        # 共有予定アイコン表示有無
        c_num = TrnScheduleMmember.objects.filter(continue_schedule_cd=sch_cte_val.continue_schedule_cd).count()
        if c_num > 1:
            st_cnt_detail.share_plan_icon = '1'
        else:
            st_cnt_detail.share_plan_icon = '0'

        return st_cnt_detail

    #---------------------------------------------------------------------------------
    # 関数名：１日分スケジュール情報：【スケジュール(通常)】
    # 引　数：クエリセット(対象日１スケジュール分)　｜　対象日(DateTime型)　｜　アカウントID
    # 戻り値：１日分の予定情報構造体【スケジュール(通常)】【StOneDayDetail】
    # 備　考：表示色変更用CSSのクラス文字列も作成する
    #---------------------------------------------------------------------------------
    def get_sch_oneday_normal_i(self, sch_nml_val, tar_dt, account_cd):
        # 戻り構造体
        st_nml_detail = StOneDayDetail()

        # 予定種別：0＝繰り返し、1=翌日以降続く、2=通常
        st_nml_detail.type = 2

        # 時間指定
        if sch_nml_val.normal_schedule_s_time is not None and sch_nml_val.normal_schedule_e_time is not None:
            # 時刻ありの場合、開始時刻―終了時刻
            st_nml_detail.timespan = sch_nml_val.normal_schedule_s_time.strftime('%H')\
                                       + ':' + sch_nml_val.normal_schedule_s_time.strftime('%M')\
                                       + '-' + sch_nml_val.normal_schedule_e_time.strftime('%H')\
                                       + ':' + sch_nml_val.normal_schedule_e_time.strftime('%M')
        else:
            st_nml_detail.timespan = ''

        # 予定タイトル
        if len(sch_nml_val.normal_schedule_name) > 1:
            st_nml_detail.title = sch_nml_val.normal_schedule_name
        else:
            st_nml_detail.title = '--'

        # 予定詳細表示リンク用URLパラメータ
        st_nml_detail.detail_link_i = '?id=' + account_cd + '&trday=' + tar_dt.strftime('%Y.%m.%d')  \
                + '&PP=gw&PPGr=' + lib_get_url_gr(self) + '' + '&schid=' + sch_nml_val.normal_schedule_cd + '&schty=nml'

        # タグ名　※初期化
        st_nml_detail.tag = ''
        # タグ背景色色コード　※初期化
        st_nml_detail.tagcolor = ''
        # 予定背景色色コード　※初期化
        st_nml_detail.bkcolor = ''

        # DBアクセス【予定メニュー登録マスタ】：表示名取得
        q_sch_type = MstScheduleType.objects.filter(schedule_type_cd=sch_nml_val.schedule_type_cd)
        if q_sch_type.exists():
            st_nml_detail.tag = q_sch_type[0].schedule_type_name

            # DBアクセス【予定色マスタ】：予定色RGBコード取得
            q_sch_type_color = MstScheduleTypeColor.objects.filter(schedule_type_color_cd=q_sch_type[0].schedule_type_color_cd)
            if q_sch_type_color.exists():
                st_nml_detail.tagcolor = q_sch_type_color[0].schedule_type_rgb
                st_nml_detail.bkcolor = q_sch_type_color[0].schedule_type_bg_rgb

        # 期間重複警告アイコン表示有無★保留★
        st_nml_detail.warning_icon = ''

        # 共有予定アイコン表示有無
        c_num = TrnScheduleMmemberNormal.objects.filter(normal_schedule_cd=sch_nml_val.normal_schedule_cd).count()
        if c_num > 1:
            st_nml_detail.share_plan_icon = '1'
        else:
            st_nml_detail.share_plan_icon = '0'

        return st_nml_detail

    #---------------------------------------------------------------------------------
    # 関数名：スケジュール(期間)情報
    # 引　数：クエリセット(対象期間内の１スケジュール分)　｜　期間開始日(DateTime型)　｜　期間終了日(DateTime型)　｜　アカウントID
    # 戻り値：スケジュール(期間)情報【StScheduleSpanDispInfo】
    # 備　考：表示色変更用CSSのクラス文字列も作成する
    #---------------------------------------------------------------------------------
    def get_sch_span_i(self, sch_spn_val, start_dt, end_dt, account_cd):
        # 戻り構造体
        st_spn_detail = StScheduleSpanDispInfo()

        # 予定なし列数
        if sch_spn_val.span_schedule_s_date <= start_dt:
            # 開始日期間外
            st_spn_detail.no_sch_colspan = 0
        else:
            # 開始日期間内：予定開始日から期間開始日を引いた日数
            st_spn_detail.no_sch_colspan = (sch_spn_val.span_schedule_s_date - start_dt).days

        # 予定あり列数
        if sch_spn_val.span_schedule_e_date >= end_dt:
            # 終了日期間外
            st_spn_detail.sch_colspan = 7 - st_spn_detail.no_sch_colspan
            # 予定あり後列数
            st_spn_detail.sch_after_colspan = 0
        else:
            # 終了日期間内：表示期間 - 予定終了日から期間終了日を引いた日数 - 予定なし列数
            day_wk = (end_dt - sch_spn_val.span_schedule_e_date).days
            st_spn_detail.sch_colspan = 7 - day_wk - st_spn_detail.no_sch_colspan
            # 予定あり後列数
            st_spn_detail.sch_after_colspan = day_wk

        # タグ名　※初期化
        st_spn_detail.tag = ''
        # タグ背景色色コード　※初期化
        st_spn_detail.tagcolor = ''

        # DBアクセス【予定メニュー登録マスタ】：表示名取得
        q_sch_type = MstScheduleType.objects.filter(schedule_type_cd=sch_spn_val.schedulse_type_cd)
        if q_sch_type.exists():
            st_spn_detail.tag = q_sch_type[0].schedule_type_name

            # DBアクセス【予定色マスタ】：予定色RGBコード取得
            q_sch_type_color = MstScheduleTypeColor.objects.filter(schedule_type_color_cd=q_sch_type[0].schedule_type_color_cd)
            if q_sch_type_color.exists():
                st_spn_detail.tagcolor = q_sch_type_color[0].schedule_type_rgb

        # 予定タイトル
        if len(sch_spn_val.span_schedule_name) > 1:
            st_spn_detail.title = sch_spn_val.span_schedule_name
        else:
            st_spn_detail.title = '--'

        # 予定詳細表示リンク用URLパラメータ
        st_spn_detail.detail_link_i = '?id=' + account_cd + '&trday=' +  start_dt.strftime('%Y.%m.%d') \
                + '&PP=gw&PPGr=' + lib_get_url_gr(self) + '' + '&schid=' + sch_spn_val.span_schedule_cd + '&schty=spn'

        # 共有予定アイコン表示有無
        c_num = TrnScheduleMmemberSpan.objects.filter(span_schedule_cd_id=sch_spn_val.span_schedule_cd_id).count()
        if c_num > 1:
            st_spn_detail.share_plan_icon = '1'
        else:
            st_spn_detail.share_plan_icon = '0'

        return st_spn_detail



        # SQL直書きメモ
        #with connection.cursor() as cursor:
        #    cursor.execute("SELECT group_cd, group_name FROM overview_mstgroup ORDER BY disp_order")
        #    st_group_i.group_list = cursor.fetchall()
