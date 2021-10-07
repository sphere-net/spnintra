# 標準
from django.http import JsonResponse
import json
from django.db.models import Q
# オリジナルライブラリインポート
from commonutil.libraries import *

#=====================================================================================
# スケジュールAjax
#=====================================================================================
# ---------------------------------------------------------------------------------
# 関数名：日付情報取得　※曜日、祝日情報込み
# 引　数：対象年、対象月
# 戻り値：日付情報
# 備　考：一般的にはAPIのレスポンスはdict型を推奨。list型の変数を返すとエラーが発生。
#       ※デフォルトsafe=True、safe=TrueでAPIのレスポンスとしてlist型の変数を返してはいけない
# ---------------------------------------------------------------------------------
def ScheduleAjaxGetDays(request):
    days: list[int, str] = []
    if request.method == 'GET':
        tr_year = str(request.GET.get('year'))
        tr_month = str(request.GET.get('month'))
        days = lib_get_target_days(tr_year, tr_month)

    return JsonResponse(json.dumps(days), safe=False)

# ---------------------------------------------------------------------------------
# 関数名：グループ情報取得
# 引　数：取得対象グループID
# 戻り値：グループメンバー
# 備　考：
# ---------------------------------------------------------------------------------
def ScheduleAjaxGetGroup(request):
    gr_member: list[str, str] = []
    if request.method == 'GET':
        tr_group = str(request.GET.get('group'))
        if tr_group == '0':
            # DBアクセス【アカウント登録マスタ】
            q_account_list = MstAccount.objects.order_by('disp_name_yomi')
            for value in q_account_list:
                gr_member.append([value.account_cd, value.disp_name])
        else:
            gr_member = lib_get_target_gr_members(tr_group)

    return JsonResponse(json.dumps(gr_member), safe=False)

# ---------------------------------------------------------------------------------
# 関数名：施設情報取得
# 引　数：取得対象施設ID
# 戻り値：施設メンバー
# 備　考：
# ---------------------------------------------------------------------------------
def ScheduleAjaxGetSisetsu(request):
    gr_member: list[str, str] = []
    if request.method == 'GET':
        tr_group = str(request.GET.get('group'))
        gr_member = lib_get_target_sisetsu_members(tr_group)

    return JsonResponse(json.dumps(gr_member), safe=False)

# ---------------------------------------------------------------------------------
# 関数名：アカウント検索
# 引　数：検索対象文字列
# 戻り値：検索結果
# 備　考：
# ---------------------------------------------------------------------------------
def ScheduleAjaxSarchAccount(request):
    search_res: list[str, str] = []
    if request.method == 'GET':
        tr_account = str(request.GET.get('search'))
        # DBアクセス【アカウントマスタ】
        q_my_account = MstAccount.objects.filter(Q(disp_name__contains=tr_account) | Q(disp_name_yomi__contains=tr_account))
        if q_my_account.exists():
            for value in q_my_account:
                search_res.append([value.account_cd, value.disp_name])

    return JsonResponse(json.dumps(search_res), safe=False)

