from django.http import HttpResponse
from django.shortcuts import render
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
from django.db import connection

#=====================================================================================
# スケジュール削除画面 ※ログインしていないと見れないページ
#=====================================================================================
class ScheduleDelView(LoginRequiredMixin, TemplateView):
    template_name = "message_only.html"

    #---------------------------------------------------------------------------------
    # 関数名：パンくずリスト用情報作成
    # 引　数：なし
    # 戻り値：disp：表示文字列　｜　url_type：画面種別　｜　detail_link：予定詳細表示リンク用URLパラメータ
    # 備　考：リンク先情報(StLink)
    #---------------------------------------------------------------------------------
    @cached_property # リクエスト単位でキャッシュ
    def get_pan_pp_i(self):
        # パラメータ取得
        url_pp = lib_get_url_pp(self)
        url_trday = lib_get_url_trday(self)
        url_ppgr = lib_get_url_ppgr(self)

        # 戻り構造体
        st_link = StLink()

        # 戻り情報作成
        if url_pp == 'gd':
            st_link.disp = 'グループ日表示'
            query_string = urlencode({'gr': url_ppgr, 'trday': url_trday})
            url = reverse('schedule:schedule_gday') + f'?{query_string}'
        elif url_pp == 'gw':
            st_link.disp = 'グループ週表示'
            query_string = urlencode({'gr': url_ppgr, 'trday': url_trday})
            url = reverse('schedule:schedule_index') + f'?{query_string}'
        elif url_pp == 'pd':
            st_link.disp = '個人日表示'
            query_string = urlencode({'gr': url_ppgr, 'trday': url_trday})
            url = reverse('schedule:schedule_pday') + f'?{query_string}'
        elif url_pp == 'pw':
            st_link.disp = '個人週表示'
            query_string = urlencode({'gr': url_ppgr, 'trday': url_trday})
            url = reverse('schedule:schedule_pweek') + f'?{query_string}'
        elif url_pp == 'pm':
            st_link.disp = '個人月表示'
            query_string = urlencode({'gr': url_ppgr, 'trday': url_trday})
            url = reverse('schedule:schedule_pmonth') + f'?{query_string}'
        else:
            st_link.disp = '個人年表示'
            query_string = urlencode({'gr': url_ppgr, 'trday': url_trday})
            url = reverse('schedule:schedule_pyear') + f'?{query_string}'

        st_link.link_url = url

        return st_link

    #---------------------------------------------------------------------------------
    # 関数名：パンくずリスト用情報作成
    # 引　数：なし
    # 戻り値：詳細画面のURL
    # 備　考：
    #---------------------------------------------------------------------------------
    @cached_property # リクエスト単位でキャッシュ
    def get_pan_ditail(self):
        return lib_make_url_prm_id_trday_pp_ppgr_schid_schty(self)

    #---------------------------------------------------------------------------------
    # 関数名：パンくずリスト用情報作成
    # 引　数：なし
    # 戻り値：メッセージ表示対象画面
    # 備　考：
    #---------------------------------------------------------------------------------
    @cached_property # リクエスト単位でキャッシュ
    def get_pan_disp(self):
        url_msgty = lib_get_url_msgty(self)

        if url_msgty == 'del':
            ret_param = '予定の削除'
        elif url_msgty == 'out':
            ret_param = '予定から抜ける'
        else:  # join
            ret_param = '予定に参加する'

        return ret_param

    #---------------------------------------------------------------------------------
    # 関数名：タイトル表示用アイコン取得
    # 引　数：なし
    # 戻り値：
    # 備　考：
    #---------------------------------------------------------------------------------
    @cached_property # リクエスト単位でキャッシュ
    def get_title_icon(self):
        url_msgty = lib_get_url_msgty(self)

        if url_msgty == 'del':
            ret_param = 'fas fa-trash-alt'
        elif url_msgty == 'out':
            ret_param = 'fas fa-sign-out-alt'
        else:  # join
            ret_param = 'fas fa-sign-in-alt'

        return ret_param

    #---------------------------------------------------------------------------------
    # 関数名：BODY内のメッセージタイトル
    # 引　数：なし
    # 戻り値：BODY内のメッセージタイトル文字列
    # 備　考：
    #---------------------------------------------------------------------------------
    @cached_property # リクエスト単位でキャッシュ
    def get_pan_title(self):
        url_msgty = lib_get_url_msgty(self)

        if url_msgty == 'del':
            ret_param = '次のデータを削除します。'
        elif url_msgty == 'out':
            ret_param = '次の予定から抜けます。'
        else:  # join
            ret_param = '次の予定に参加します。'

        return ret_param

    #---------------------------------------------------------------------------------
    # 関数名：SUBMITボタン
    # 引　数：なし
    # 戻り値：SUBMITボタン文字列
    # 備　考：
    #---------------------------------------------------------------------------------
    @cached_property # リクエスト単位でキャッシュ
    def get_pan_submit(self):
        url_msgty = lib_get_url_msgty(self)

        if url_msgty == 'del':
            ret_param = '削除する'
        elif url_msgty == 'out':
            ret_param = '予定から抜ける'
        else:  # join
            ret_param = '参加する'

        return ret_param

    #---------------------------------------------------------------------------------
    # 関数名：登録SUBMITへのリンク用パラメータ作成
    # 引　数：なし
    # 戻り値：リンク用URLパラメータ
    # 備　考：Sbumit後のリダイレクト用
    #---------------------------------------------------------------------------------
    @cached_property # リクエスト単位でキャッシュ
    def get_regist_param(self):
        return lib_make_url_prm_id_trday_pp_ppgr_schid_schty(self)

    # ---------------------------------------------------------------------------------
    # 関数名：予定タイトル
    # 引　数：なし
    # 戻り値：予定タイトル文字列
    # 備　考：
    # ---------------------------------------------------------------------------------
    @cached_property  # リクエスト単位でキャッシュ
    def get_sch_title(self):
        # パラメータ取得
        url_schid = lib_get_url_schid(self)
        url_schty = lib_get_url_schty(self)

        # 初期化
        ret_param = ''

        # 通常予定
        if url_schty == 'nml':
            # DBアクセス【スケジュール(通常)】：スケジュールコード指定で１レコード取得
            q_sch_nml = TrnScheduleNormal.objects.filter(normal_schedule_cd=url_schid).first()
            ret_param = q_sch_nml.normal_schedule_name
        # 翌日以降まで続く予定
        elif url_schty == 'cte':
            # DBアクセス【スケジュール(継続)】：スケジュールコード指定で１レコード取得
            q_sch_cte = TrnScheduleContinue.objects.filter(continue_schedule_cd=url_schid).first()
            ret_param = q_sch_cte.continue_schedule_name
        # 期間予定
        elif url_schty == 'spn':
            # DBアクセス【スケジュール(期間)】：スケジュールコード指定で１レコード取得
            q_sch_spn = TrnScheduleSpan.objects.filter(span_schedule_cd=url_schid).first()
            ret_param = q_sch_spn.span_schedule_name
        # 繰り返し予定
        else: # url_schty == 'rep':
            ret_param = ''

        return ret_param

    #---------------------------------------------------------------------------------
    # 関数名：POSTリクエスト受信
    # 引　数：Formデータ
    # 戻り値：
    # 備　考：DB登録を行い、詳細画面へ遷移する
    #---------------------------------------------------------------------------------
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            # 内部変数
            sch_chg_flg = False

            # URLパラメータ取得
            my_account = lib_get_my_account_i(self)
            u_prm_pp = lib_get_url_pp(self)
            u_prm_ppgr = lib_get_url_ppgr(self)
            u_prm_schid = lib_get_url_schid(self)
            u_prm_schty = lib_get_url_schty(self)
            u_prm_msgty = lib_get_url_msgty(self)

            if url_msgty == 'del':
                ret_param = '削除する'
            elif url_msgty == 'out':
                ret_param = '予定から抜ける'
            else:  # join
                ret_param = '参加する'

            # リダイレクトパラメ―タ作成
            #       ?id=URLパラメータ：自アカウント
            #       &trday=登録：日付
            #       &PP=URLパラメータ
            #       &PPGr=URLパラメータ
            #       &schid=登録：スケジュールID
            #       &schty=URLパラメータ：タブ
            query_string = urlencode({'id': my_account.account_cd,
                                      'trday': o_prm_trday,
                                      'PP': u_prm_pp,
                                      'PPGr': u_prm_ppgr,
                                      'schid': u_prm_schid,
                                      'schty': remake_schty})

            # URLを逆引きして、パラメータを追加　※遷移先は詳細
            url = reverse('schedule:schedule_detail') + f'?{query_string}'
            return redirect(url)

        # POST以外（失敗含む）は、元の画面に戻る
        return self.get(request, *args, **kwargs)


