from urllib.parse import urlencode
from django.urls import reverse
# モデルインポート
from overview.models import *
from schedule.models import *
# 標準インポート
from django.db.models import F
import datetime
import time
import calendar

MINUTE_CHOICES = (
    (99, '--分'),
    (0, '00分'),
    (15, '15分'),
    (30, '30分'),
    (45, '45分')
)
#★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
# 共通構造体
#★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
# 遷移先情報【使用：グループ週】
class StTranInfo:
    def __init__(self):
        self.pre_week_ymd = ''          # リンク用URLパラメータ文字列：前週
        self.pre_day_ymd = ''           # リンク用URLパラメータ文字列：前日
        self.today_ymd = ''             # リンク用URLパラメータ文字列：今日
        self.next_day_ymd = ''          # リンク用URLパラメータ文字列：翌日
        self.next_week_ymd = ''         # リンク用URLパラメータ文字列：翌週

# ヘッダ情報【使用：グループ週】
class StHeaderInfo:
    def __init__(self):
        self.day = ''                   # 日付※日のみ
        self.day_of_week = ''           # 曜日※和名短縮形
        self.day_type = ''              # 祝日、平日、土曜に対応する色指定CSS

# グループリスト情報【使用：グループ週】
class StGroupListInfo:
    def __init__(self):
        self.group_cd = ''              # グループID
        self.group_name = ''            # グループ名（表示用）
        self.group_url = ''             # リンクURL

# グループ週画面データ表示情報【使用：グループ週】
class StOneAcountInfo:
    def __init__(self):
        self.head_flg = ''              # ヘッダ表示有無
        self.icon_name = ''             # アイコンファイル名
        self.disp_name = ''             # ユーザー名
        self.month_link_i = ''          # 月表示リンク用URLパラメータ
        self.oneday_other_i = []        # １日分スケジュール情報：祝日＆予定登録
        self.sch_span_flg = ''          # 期間予定有無
        self.span_disp_i = []           # 期間予定情報

# １日分スケジュール情報：祝日＆予定登録【使用：グループ週】
class StOneDayWap:
    def __init__(self):
        self.month_day = ''             # 月/日　表示用文字列
        self.holiday_name = ''          # 祝日表示文字列
        self.regist_link_info = ''      # 予定登録リンク用URLパラメータ
        self.tar_day = ''               # 表示対象日
        self.oneday_she_disp_i = []     # １日分スケジュール情報：詳細

# １日分スケジュール情報：詳細【使用：グループ週】
class StOneDayDetail:
    def __init__(self):
        self.type = ''                  # 予定種別：0＝繰り返し、1=翌日以降続く、2=通常
        self.timespan = ''              # 時間指定(表示用）
        self.tag = ''                   # タグ名
        self.tagcolor = ''              # タグ背景色色コード
        self.title = ''                 # 予定タイトル
        self.bkcolor = ''               # 予定背景色色コード
        self.detail_link_i = ''         # 予定詳細表示リンク用URLパラメータ
        self.warning_icon = ''          # 期間重複警告アイコン表示有無
        self.share_plan_icon = ''       # 共有予定アイコン表示有無

# 期間予定情報【使用：グループ週】
class StScheduleSpanDispInfo:
    def __init__(self):
        self.no_sch_colspan = ''        # 予定なし列数
        self.sch_colspan = ''           # 予定あり列数
        self.sch_after_colspan = ''     # 予定あり後列数
        self.tag = ''                   # タグ名
        self.tagcolor = ''              # タグ背景色色コード
        self.title = ''                 # 予定タイトル
        self.detail_link_i = ''         # 予定詳細表示リンク用URLパラメータ
        self.share_plan_icon = ''       # 共有予定アイコン表示有無

# リンク先情報【使用：詳細】
class StLink:
    def __init__(self):
        self.disp = ''                  # 表示用文字列
        self.link_url = ''              # リンク用URL

# スケジュール詳細情報【使用：詳細】
class StDetail:
    def __init__(self):
        self.tag_title = ''             # タグ名 & 予定タイトル
        self.regist_i = ''              # 登録情報
        self.regist_icon = ''           # 登録者ICON種別
        self.change_i = ''              # 更新情報
        self.change_icon = ''           # 更新者ICON種別
        self.d_t = ''                   # 日時情報
        self.memo_i = ''                # メモ情報
        self.institution_i = []         # 施設情報
        self.member_i = []              # 参加者情報
        self.menber_num = ''            # 参加者数
        self.my_sch_flg = ''            # 予定に自アカウントを含む＝TRUE、含まない＝FALSE

# 参加者情報【使用：詳細】
class StMember:
    def __init__(self):
        self.disp_name = ''             # 表示用文字列
        self.icon_type = ''             # ICON種別

#★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
# 共通関数
#★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
# ---------------------------------------------------------------------------------
# 関数名：アカウントコード指定してアカウント情報取得
# 引　数：アカウントコード
# 戻り値：アカウント登録マスタの指定アカウントの全取得情報
# 備　考：
# ---------------------------------------------------------------------------------
def lib_get_account_i(get_account_cd):
    # DBアクセス【アカウント登録マスタ】
    q_account = MstAccount.objects.filter(account_cd=get_account_cd).first()

    return q_account

# ---------------------------------------------------------------------------------
# 関数名：日付操作：基準日から指定日前後の日付（DateTime型）
# 引　数：基準日　｜　基準日から取得したい指定日までの日数（マイナス可）
# 戻り値：計算結果（DateTime型）
# 備　考：基準日はDateTime型で受け取る想定
# ---------------------------------------------------------------------------------
def lib_chg_day(tar_day, chg_day):
    dt = tar_day + datetime.timedelta(days=chg_day)
    return dt

# ---------------------------------------------------------------------------------
# 関数名：英語表記から日本語表記に曜日表記変更
# 引　数：英語表記の曜日（短縮形）
# 戻り値：日本語表記の曜日（短縮形）
# 備　考：ロケーションを変えると文字化けしたので仕方なしに作成。。。
# ---------------------------------------------------------------------------------
def lib_chg_youbi_eng_to_jpn(youbi):
    if youbi == 'Mon':
        ret = '月'
    elif youbi == 'Tue':
        ret = '火'
    elif youbi == 'Wed':
        ret = '水'
    elif youbi == 'Thu':
        ret = '木'
    elif youbi == 'Fri':
        ret = '金'
    elif youbi == 'Sat':
        ret = '土'
    else:
        ret = '日'
    return ret

# ---------------------------------------------------------------------------------
# 関数名：数値から日本語表記に曜日表記変更
# 引　数：数値の曜日（月曜が0、日曜が6）※int型
# 戻り値：日本語表記の曜日（短縮形）
# 備　考：
# ---------------------------------------------------------------------------------
def lib_chg_youbi_num_to_jpn(youbi):
    if youbi == 0:
        ret = '月'
    elif youbi == 1:
        ret = '火'
    elif youbi == 2:
        ret = '水'
    elif youbi == 3:
        ret = '木'
    elif youbi == 4:
        ret = '金'
    elif youbi == 5:
        ret = '土'
    else:
        ret = '日'
    return ret

# ---------------------------------------------------------------------------------
# 関数名：日付情報取得　※曜日、祝日情報込み
# 引　数：対象年、対象月
# 戻り値：日付情報(リスト型)
# 備　考：
# ---------------------------------------------------------------------------------
def lib_get_target_days(tr_year, tr_month):
    # 基準日作成（祝日判定用）
    dt = datetime.date(int(tr_year), int(tr_month), 1)

    # コンボボックス用リスト（宣言）
    date_day: list[int, str] = []

    # 対象月の日数取得
    tr_days = calendar.monthrange(int(tr_year), int(tr_month))[1]

    # 対象月の１日の曜日取得
    tr_s_youbi = calendar.monthrange(int(tr_year), int(tr_month))[0]

    # コンボボックス中身
    for iLoop in range(1, int(tr_days) + 1, 1):
        # 日付作成
        dt_wk = lib_chg_day(dt, iLoop - 1)

        # DBアクセス【祝日登録マスタ】：日付指定して祝日情報取得
        q_holiday = MstHoliday.objects.filter(holiday_date=dt_wk)
        # 祝日判定
        if q_holiday.exists():
            date_day.append([iLoop, str(iLoop) + '(' + lib_chg_youbi_num_to_jpn(tr_s_youbi) + ')祝'])
        else:
            date_day.append([iLoop, str(iLoop) + '(' + lib_chg_youbi_num_to_jpn(tr_s_youbi) + ')'])

        # 曜日コントロール
        tr_s_youbi = tr_s_youbi + 1
        if tr_s_youbi > 6:
            tr_s_youbi = 0

    return date_day

# ---------------------------------------------------------------------------------
# 関数名：グループ情報取得
# 引　数：取得対象グループID
# 戻り値：グループ情報(リスト型)
# 備　考：
# ---------------------------------------------------------------------------------
def lib_get_target_gr_members(tr_group):
    # コンボボックス用リスト（宣言）
    gr_member: list[str, str] = []

    # DBアクセス【グループ登録マスタ】：表示対象グループ情報取得
    q_gr_accounts = MstBelongGroup.objects.filter(group_cd=tr_group)

    # コンボボックス中身
    for account in q_gr_accounts:
        # アカウント情報取得
        account_i = lib_get_account_i(account.account_cd)
        gr_member.append([account_i.account_cd, account_i.disp_name])

    return gr_member

# ---------------------------------------------------------------------------------
# 関数名：施設情報取得
# 引　数：取得対象施設ID
# 戻り値：施設情報(リスト型)
# 備　考：
# ---------------------------------------------------------------------------------
def lib_get_target_sisetsu_members(tr_group):
    # コンボボックス用リスト（宣言）
    setu_member: list[str, str] = []

    # DBアクセス【施設登録マスタ】
    q_setu_member_list = MstInstitution.objects.filter(institution_group_cd=tr_group).order_by('disp_order')
    if q_setu_member_list.exists():
        for setu_member_value in q_setu_member_list:
            setu_member.append([setu_member_value.institution_cd, setu_member_value.institution_name])

    return setu_member

# ---------------------------------------------------------------------------------
# 関数名：自アカウント情報取得
# 引　数：なし
# 戻り値：アカウント登録マスタの自アカウント取得情報
# 備　考：
# ---------------------------------------------------------------------------------
def lib_get_my_account_i(self):
    # DBアクセス【アカウント登録マスタ】
    q_my_account = MstAccount.objects.filter(user_id=self.request.user).first()

    return q_my_account

# ---------------------------------------------------------------------------------
# 関数名：URLパラメータ（対象者）取得
# 引　数：なし
# 戻り値：URLパラメータ（対象者）
# 備　考：パラメータがない場合は、ログインユーザ
# ---------------------------------------------------------------------------------
def lib_get_url_id(self):
    # パラメータ取得
    url_param = self.request.GET.get('id', '')

    # パラメータがない時のデフォルト作成
    if url_param == '0' or url_param == '':
        # DBアクセス【アカウント登録マスタ】
        q_my_account = lib_get_my_account_i(self)
        url_param = q_my_account.account_cd

    return url_param


# ---------------------------------------------------------------------------------
# 関数名：URLパラメータ（選択グループ情報）取得
# 引　数：なし
# 戻り値：URLパラメータ（選択グループ情報）
# 備　考：パラメータがない場合は、アカウントマスターのデフォルトグループとする
# ---------------------------------------------------------------------------------
def lib_get_url_gr(self):
    # パラメータ取得
    url_param = self.request.GET.get('gr', '')

    # パラメータがない時のデフォルト作成
    if url_param == '0' or url_param == '':
        # DBアクセス【アカウント登録マスタ】
        q_my_account = lib_get_my_account_i(self)
        url_param = q_my_account.default_group_cd

    return url_param

# ---------------------------------------------------------------------------------
# 関数名：URLパラメータ（基準日）取得
# 引　数：なし
# 戻り値：URLパラメータ（基準日）
# 備　考：パラメータがない場合は、本日の日付
# ---------------------------------------------------------------------------------
def lib_get_url_trday(self):
    # パラメータ取得
    url_param = self.request.GET.get('trday', '')

    # パラメータがない時のデフォルト作成
    if url_param == '0' or url_param == '':
        dt = datetime.date.today()
        url_param = dt.strftime('%Y.%m.%d')

    return url_param

# ---------------------------------------------------------------------------------
# 関数名：URLパラメータ（遷移前のページ）取得
# 引　数：なし
# 戻り値：URLパラメータ（遷移前のページ）
# 備　考：パラメータがない場合は、スケジュール_グループ週
# ---------------------------------------------------------------------------------
def lib_get_url_pp(self):
    # パラメータ取得
    url_param = self.request.GET.get('PP', '')

    # パラメータがない時のデフォルト作成
    if url_param == '0' or url_param == '':
        url_param = 'gw'

    return url_param

# ---------------------------------------------------------------------------------
# 関数名：URLパラメータ（遷移前のページのグループID）取得
# 引　数：なし
# 戻り値：URLパラメータ（遷移前のページのグループID）
# 備　考：パラメータがない場合は、アカウントマスターのデフォルトグループとする
# ---------------------------------------------------------------------------------
def lib_get_url_ppgr(self):
    # パラメータ取得
    url_param = self.request.GET.get('PPGr', '')

    # パラメータがない時のデフォルト作成
    if url_param == '0' or url_param == '':
        q_my_account = lib_get_my_account_i(self)
        url_param = q_my_account.default_group_cd

    return url_param

# ---------------------------------------------------------------------------------
# 関数名：URLパラメータ（スケジュールID）取得
# 引　数：なし
# 戻り値：URLパラメータ（スケジュールID）
# 備　考：パラメータがない場合は、00000000
# ---------------------------------------------------------------------------------
def lib_get_url_schid(self):
    # パラメータ取得
    url_param = self.request.GET.get('schid', '')

    # パラメータがない時のデフォルト作成
    if url_param == '0' or url_param == '':
        url_param = '00000000'

    return url_param

# ---------------------------------------------------------------------------------
# 関数名：URLパラメータ（スケジュールタイプ）取得
# 引　数：なし
# 戻り値：URLパラメータ（スケジュールタイプ）
# 備　考：パラメータがない場合は、通常(nml) ※継続：cte、期間：spn、リピート：rep
# ---------------------------------------------------------------------------------
def lib_get_url_schty(self):
    # パラメータ取得
    url_param = self.request.GET.get('schty', '')

    # パラメータがない時のデフォルト作成
    if url_param == '0' or url_param == '':
        url_param = 'nml'

    return url_param

# ---------------------------------------------------------------------------------
# 関数名：URLパラメータ（メッセージタイプ）取得
# 引　数：なし
# 戻り値：URLパラメータ（メッセージタイプ）
# 備　考：パラメータがない場合は、削除(del) ※予定から抜ける：out、予定に参加する：join
# ---------------------------------------------------------------------------------
def lib_get_url_msgty(self):
    # パラメータ取得
    url_param = self.request.GET.get('msgty', '')

    # パラメータがない時のデフォルト作成
    if url_param == '0' or url_param == '':
        url_param = 'del'

    return url_param

# ---------------------------------------------------------------------------------
# 関数名：URLパラメータ作成
# 引　数：なし
# 戻り値：URLパラメータ
# 備　考：
# ---------------------------------------------------------------------------------
def lib_make_url_prm_id_trday_pp_ppgr(self):
    # パラメータ取得
    url_id = lib_get_url_id(self)
    url_trday = lib_get_url_trday(self)
    url_pp = lib_get_url_pp(self)
    url_ppgr = lib_get_url_ppgr(self)

    # 戻り情報作成
    ret_param = '?id=' + url_id + '&trday=' + url_trday + '&PP=' + url_pp + '&PPGr=' + url_ppgr

    return ret_param

def lib_make_url_prm_id_trday_pp_ppgr_schty(self):
    # パラメータ取得
    url_id = lib_get_url_id(self)
    url_trday = lib_get_url_trday(self)
    url_pp = lib_get_url_pp(self)
    url_ppgr = lib_get_url_ppgr(self)
    url_schty = lib_get_url_schty(self)

    # 戻り情報作成
    ret_param = '?id=' + url_id + '&trday=' + url_trday + '&PP=' + url_pp + '&PPGr=' + url_ppgr + '&schty=' + url_schty

    return ret_param

def lib_make_url_prm_id_trday_pp_ppgr_schid_schty(self):
    # パラメータ取得
    url_id = lib_get_url_id(self)
    url_trday = lib_get_url_trday(self)
    url_pp = lib_get_url_pp(self)
    url_ppgr = lib_get_url_ppgr(self)
    url_schid = lib_get_url_schid(self)
    url_schty = lib_get_url_schty(self)

    # 戻り情報作成
    ret_param = '?id=' + url_id + '&trday=' + url_trday + '&PP=' + url_pp + '&PPGr=' + url_ppgr + '&schid=' + url_schid + '&schty=' + url_schty

    return ret_param

def lib_make_url_prm_id_trday_pp_ppgr_schid_schty_msgy(self):
    # パラメータ取得
    url_id = lib_get_url_id(self)
    url_trday = lib_get_url_trday(self)
    url_pp = lib_get_url_pp(self)
    url_ppgr = lib_get_url_ppgr(self)
    url_schid = lib_get_url_schid(self)
    url_schty = lib_get_url_schty(self)
    url_msgty = lib_get_url_msgty(self)

    # 戻り情報作成
    ret_param = '?id=' + url_id + '&trday=' + url_trday + '&PP=' + url_pp + '&PPGr=' + url_ppgr + \
                '&schid=' + url_schid + '&schty=' + url_schty + '&msgty=' + url_msgty

    return ret_param

# ---------------------------------------------------------------------------------
# 関数名：URL作成
# 引　数：なし
# 戻り値：URL
# 備　考：画面へのURL
# ---------------------------------------------------------------------------------
# PP画面への遷移
def lib_make_url_to_pp(self):
    # パラメータ取得
    url_id = lib_get_url_id(self)
    url_trday = lib_get_url_trday(self)
    url_pp = lib_get_url_pp(self)
    url_ppgr = lib_get_url_ppgr(self)

    # 戻り情報作成
    if url_pp == 'gd':
        query_string = urlencode({'grday': url_ppgr, 'trday': url_trday})
        # URLを逆引きして、パラメータを追加
        ret_param = reverse('schedule:schedule_gday') + f'?{query_string}'
    elif url_pp == 'gw':
        query_string = urlencode({'gr': url_ppgr, 'trday': url_trday})
        # URLを逆引きして、パラメータを追加
        ret_param = reverse('schedule:schedule_index') + f'?{query_string}'
    elif url_pp == 'pd':
        query_string = urlencode({'trday': url_trday})
        # URLを逆引きして、パラメータを追加
        ret_param = reverse('schedule:schedule_pday') + f'?{query_string}'
    elif url_pp == 'pw':
        query_string = urlencode({'trday': url_trday})
        # URLを逆引きして、パラメータを追加
        ret_param = reverse('schedule:schedule_pweek') + f'?{query_string}'
    elif url_pp == 'pm':
        query_string = urlencode({'id': url_id, 'trday': url_trday})
        # URLを逆引きして、パラメータを追加
        ret_param = reverse('schedule:schedule_pmonth') + f'?{query_string}'
    elif url_pp == 'py':
        query_string = urlencode({'trday': url_trday})
        # URLを逆引きして、パラメータを追加
        ret_param = reverse('schedule:schedule_pyear') + f'?{query_string}'

    return ret_param

#---------------------------------------------------------------------------------
# 関数名：基準日表示用データ作成
# 引　数：なし
# 戻り値：表示用データ文字列
# 備　考：表示形式 ⇒ YYYY 年 MM 月 DD 日 ( aa )
#---------------------------------------------------------------------------------
def lib_get_day_i(self):
    # パラメータ取得
    url_param = lib_get_url_trday(self)

    # 表示用データ作成
    year = url_param[0:4]
    month = url_param[5:7]
    day = url_param[8:10]
    disp_day = year + ' 年 ' + month.lstrip("0") + ' 月 ' + day.lstrip("0") + ' 日 '
    dt = datetime.date(int(year), int(month), int(day))
    disp_day += '(' + lib_chg_youbi_eng_to_jpn(dt.strftime('%a')) + ')'

    return disp_day

