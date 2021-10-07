from django.http import HttpResponse
from urllib.parse import urlencode
from django.shortcuts import render
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
from django.db import connection

#=====================================================================================
# スケジュール詳細画面 ※ログインしていないと見れないページ
#=====================================================================================
class ScheduleDetailView(LoginRequiredMixin, TemplateView):
    template_name = "detail.html"

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
    # 関数名：パンくずリスト用情報作成
    # 引　数：なし
    # 戻り値：disp：表示文字列　｜　url_type：画面種別　｜　detail_link：予定詳細表示リンク用URLパラメータ
    # 備　考：リンク先情報(StLink)
    #---------------------------------------------------------------------------------
    @cached_property # リクエスト単位でキャッシュ
    def get_pan_i(self):
        # パラメータ取得
        url_id = lib_get_url_id(self)
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
            query_string = urlencode({'id': url_id, 'trday': url_trday, 'PPGr': url_ppgr})
            url = reverse('schedule:schedule_pday') + f'?{query_string}'
        elif url_pp == 'pw':
            st_link.disp = '個人週表示'
            query_string = urlencode({'id': url_id, 'trday': url_trday, 'PPGr': url_ppgr})
            url = reverse('schedule:schedule_pweek') + f'?{query_string}'
        elif url_pp == 'pm':
            st_link.disp = '個人月表示'
            query_string = urlencode({'id': url_id, 'trday': url_trday, 'PPGr': url_ppgr})
            url = reverse('schedule:schedule_pmonth') + f'?{query_string}'
        else:
            st_link.disp = '個人年表示'
            query_string = urlencode({'id': url_id, 'trday': url_trday, 'PPGr': url_ppgr})
            url = reverse('schedule:schedule_pyear') + f'?{query_string}'

        st_link.link_url = url

        return st_link

    #---------------------------------------------------------------------------------
    # 関数名：スケジュール詳細情報作成
    # 引　数：なし
    # 戻り値：スケジュール詳細情報構造体【StDetail】
    # 備　考：
    #---------------------------------------------------------------------------------
    @cached_property # リクエスト単位でキャッシュ
    def get_detail_i(self):
        # 戻り構造体
        st_detail_i = StDetail()

        # パラメータ取得
        url_schty = lib_get_url_schty(self)
        url_schid = lib_get_url_schid(self)

        my_account = lib_get_my_account_i(self)

        # 戻り情報作成
        # ---------------------------------------------------------------------------------
        # 通常予定
        # ---------------------------------------------------------------------------------
        if url_schty == 'nml':
            # DBアクセス【スケジュール(通常)】：スケジュールコード指定で１レコード取得
            q_sch_nml = TrnScheduleNormal.objects.filter(normal_schedule_cd=url_schid).first()
            # DBアクセス【予定メニュー登録マスタ】：表示名取得
            if q_sch_nml.schedule_type_cd is not None:
                q_sch_type = MstScheduleType.objects.filter(schedule_type_cd=q_sch_nml.schedule_type_cd)
                if q_sch_type.exists():
                    st_detail_i.tag_title = q_sch_type[0].schedule_type_name + '：'

            # タグ名 & 予定タイトル
            st_detail_i.tag_title += q_sch_nml.normal_schedule_name

            # 登録情報
            account_i = lib_get_account_i(q_sch_nml.normal_schedule_register)
            st_detail_i.regist_i = account_i.disp_name + '   ' + q_sch_nml.normal_schedule_regist_dt.strftime('%Y').lstrip('0') \
                                   + '/' + q_sch_nml.normal_schedule_regist_dt.strftime('%m').lstrip('0') \
                                   + '/' + q_sch_nml.normal_schedule_regist_dt.strftime('%d').lstrip('0') \
                                   + '(' + lib_chg_youbi_eng_to_jpn(q_sch_nml.normal_schedule_regist_dt.strftime('%a')) + ')' \
                                   + ' ' + q_sch_nml.normal_schedule_regist_dt.strftime('%H') \
                                   + ':' + q_sch_nml.normal_schedule_regist_dt.strftime('%M')

            # 登録者ICON種別
            if my_account.account_cd == account_i.account_cd :
                st_detail_i.regist_icon = '1'

            # 更新情報
            if q_sch_nml.normal_schedule_chg is not None:
                account_i = lib_get_account_i(q_sch_nml.normal_schedule_chg)
                st_detail_i.change_i = account_i.disp_name + '   ' + q_sch_nml.normal_schedule_chg_dt.strftime('%Y').lstrip('0') \
                                       + '/' + q_sch_nml.normal_schedule_chg_dt.strftime('%m').lstrip('0') \
                                       + '/' + q_sch_nml.normal_schedule_chg_dt.strftime('%d').lstrip('0') \
                                       + '(' + lib_chg_youbi_eng_to_jpn(q_sch_nml.normal_schedule_chg_dt.strftime('%a')) + ')' \
                                       + ' ' + q_sch_nml.normal_schedule_chg_dt.strftime('%H') \
                                       + ':' + q_sch_nml.normal_schedule_chg_dt.strftime('%M')

                # 更新者ICON種別
                if my_account.account_cd == account_i.account_cd :
                    st_detail_i.change_icon = '1'
                else:
                    st_detail_i.regist_icon = '0'

            # 日時情報
            reg_day_wk = q_sch_nml.normal_schedule_date.strftime('%Y').lstrip('0') \
                                       + ' 年 ' + q_sch_nml.normal_schedule_date.strftime('%m').lstrip('0') \
                                       + ' 月 ' + q_sch_nml.normal_schedule_date.strftime('%d').lstrip('0') \
                                       + ' 日 (' + lib_chg_youbi_eng_to_jpn(q_sch_nml.normal_schedule_date.strftime('%a'))
            if q_sch_nml.normal_schedule_e_time is None:
                st_detail_i.d_t = reg_day_wk + ')　(終日)'
            else:
                st_detail_i.d_t = reg_day_wk + ') ' + q_sch_nml.normal_schedule_s_time.strftime('%H') \
                                  + ':' + q_sch_nml.normal_schedule_s_time.strftime('%M') + ' ～ ' \
                                  + '' + q_sch_nml.normal_schedule_e_time.strftime('%H') \
                                  + ':' + q_sch_nml.normal_schedule_e_time.strftime('%M')

            # メモ情報
            if q_sch_nml.normal_schedule_memo is not None:
                st_detail_i.memo_i = q_sch_nml.normal_schedule_memo

            # 施設情報
            # DBアクセス【スケジュール施設】
            q_sch_institution = TrnScheduleInstitution.objects.filter(schedule_cd=q_sch_nml.normal_schedule_cd, schedule_type=1)
            if q_sch_institution.exists():
                for sch_institution in q_sch_institution:
                    # DBアクセス【施設登録マスタ】：施設名取得
                    q_institution = MstInstitution.objects.filter(institution_cd=sch_institution.institution_cd)
                    if q_institution.exists():
                        st_detail_i.institution_i.append(q_institution[0].institution_name)

            # メンバー情報
            # DBアクセス【スケジュール参加者(通常)】
            q_sch_member = TrnScheduleMmemberNormal.objects.filter(normal_schedule_cd=url_schid)
            if q_sch_member.exists():
                for sch_member in q_sch_member:
                    # 戻り構造体
                    st_member = StMember()
                    # アカウント情報取得
                    account_i = lib_get_account_i(sch_member.account_cd)
                    st_member.disp_name = account_i.disp_name
                    if my_account.account_cd == account_i.account_cd:
                        st_member.icon_type = '1'       # 自アカウント
                    elif account_i.is_valid == True:
                        st_member.icon_type = '99'      # 無効アカウント
                    else:
                        st_member.icon_type = '0'       # その他
                    st_detail_i.member_i.append(st_member)
                st_detail_i.menber_num = TrnScheduleMmemberNormal.objects.filter(normal_schedule_cd=url_schid).count()
            else:
                st_detail_i.menber_num = '0'

        # ---------------------------------------------------------------------------------
        # 翌日以降まで続く予定
        # ---------------------------------------------------------------------------------
        elif url_schty == 'cte':
            # DBアクセス【スケジュール(継続)】：スケジュールコード指定で１レコード取得
            q_sch_cte = TrnScheduleContinue.objects.filter(continue_schedule_cd=url_schid).first()
            # DBアクセス【予定メニュー登録マスタ】：表示名取得
            if q_sch_cte.schedule_type_cd is not None:
                q_sch_type = MstScheduleType.objects.filter(schedule_type_cd=q_sch_cte.schedule_type_cd)
                if q_sch_type.exists():
                    st_detail_i.tag_title = q_sch_type[0].schedule_type_name + '：'

            # タグ名 & 予定タイトル
            st_detail_i.tag_title += q_sch_cte.continue_schedule_name

            # 登録情報
            account_i = lib_get_account_i(q_sch_cte.continue_schedule_register)
            st_detail_i.regist_i = account_i.disp_name + '   ' + q_sch_cte.continue_schedule_regist_dt.strftime('%Y').lstrip('0') \
                                   + '/' + q_sch_cte.continue_schedule_regist_dt.strftime('%m').lstrip('0') \
                                   + '/' + q_sch_cte.continue_schedule_regist_dt.strftime('%d').lstrip('0') \
                                   + '(' + lib_chg_youbi_eng_to_jpn(q_sch_cte.continue_schedule_regist_dt.strftime('%a')) + ')' \
                                   + ' ' + q_sch_cte.continue_schedule_regist_dt.strftime('%H') \
                                   + ':' + q_sch_cte.continue_schedule_regist_dt.strftime('%M')

            # 登録者ICON種別
            if my_account.account_cd == account_i.account_cd :
                st_detail_i.regist_icon = '1'
            else:
                st_detail_i.regist_icon = '0'

            # 更新情報
            if q_sch_cte.continue_schedule_chg is not None:
                account_i = lib_get_account_i(q_sch_cte.continue_schedule_chg)
                st_detail_i.change_i = account_i.disp_name + '   ' + q_sch_cte.continue_schedule_chg_dt.strftime('%Y').lstrip('0') \
                                       + '/' + q_sch_cte.continue_schedule_chg_dt.strftime('%m').lstrip('0') \
                                       + '/' + q_sch_cte.continue_schedule_chg_dt.strftime('%d').lstrip('0') \
                                       + '(' + lib_chg_youbi_eng_to_jpn(q_sch_cte.continue_schedule_chg_dt.strftime('%a')) + ')' \
                                       + ' ' + q_sch_cte.continue_schedule_chg_dt.strftime('%H') \
                                       + ':' + q_sch_cte.continue_schedule_chg_dt.strftime('%M')

                # 更新者ICON種別
                if my_account.account_cd == account_i.account_cd :
                    st_detail_i.change_icon = '1'

            # 日時情報
            reg_day_wk = q_sch_cte.continue_schedule_s_date.strftime('%Y').lstrip('0') \
                                       + ' 年 ' + q_sch_cte.continue_schedule_s_date.strftime('%m').lstrip('0') \
                                       + ' 月 ' + q_sch_cte.continue_schedule_s_date.strftime('%d').lstrip('0') \
                                       + ' 日 (' + lib_chg_youbi_eng_to_jpn(q_sch_cte.continue_schedule_s_date.strftime('%a')) + ')'
            if q_sch_cte.continue_schedule_s_time is not None:
                reg_day_wk += ' ' + q_sch_cte.continue_schedule_s_time.strftime('%H') \
                             + ' 時 ' + q_sch_cte.continue_schedule_s_time.strftime('%M') + ' 分 '
            reg_day_wk += ' ～' + q_sch_cte.continue_schedule_e_date.strftime('%Y').lstrip('0') \
                         + ' 年 ' + q_sch_cte.continue_schedule_e_date.strftime('%m').lstrip('0') \
                         + ' 月 ' + q_sch_cte.continue_schedule_e_date.strftime('%d').lstrip('0') \
                         + ' 日 (' + lib_chg_youbi_eng_to_jpn(q_sch_cte.continue_schedule_e_date.strftime('%a'))
            if q_sch_cte.continue_schedule_e_time is not None:
                reg_day_wk += ') ' + q_sch_cte.continue_schedule_e_time.strftime('%H') \
                             + ' 時 ' + q_sch_cte.continue_schedule_e_time.strftime('%M') + ' 分 '
            else :
                reg_day_wk += ') '
            st_detail_i.d_t = reg_day_wk
            # メモ情報
            if q_sch_cte.continue_schedule_memo is not None:
                st_detail_i.memo_i = q_sch_cte.continue_schedule_memo

            # 施設情報
            # DBアクセス【スケジュール施設】
            q_sch_institution = TrnScheduleInstitution.objects.filter(schedule_cd=q_sch_cte.continue_schedule_cd, schedule_type=2)
            if q_sch_institution.exists():
                for sch_institution in q_sch_institution:
                    # DBアクセス【施設登録マスタ】：施設名取得
                    q_institution = MstInstitution.objects.filter(institution_cd=sch_institution.institution_cd)
                    if q_institution.exists():
                        st_detail_i.institution_i.append(q_institution[0].institution_name)

            # メンバー情報
            # DBアクセス【スケジュール参加者(継続)】
            q_sch_member = TrnScheduleMmember.objects.filter(continue_schedule_cd=url_schid)
            if q_sch_member.exists():
                for sch_member in q_sch_member:
                    # 戻り構造体
                    st_member = StMember()
                    # アカウント情報取得
                    account_i = lib_get_account_i(sch_member.account_cd)
                    st_member.disp_name = account_i.disp_name
                    if my_account.account_cd == account_i.account_cd:
                        st_member.icon_type = '1'   # 自アカウント
                    elif account_i.is_valid == True:
                        st_member.icon_type = '99'  # 無効アカウント
                    else:
                        st_member.icon_type = '0'   # その他
                    st_detail_i.member_i.append(st_member)
                st_detail_i.menber_num = TrnScheduleMmember.objects.filter(continue_schedule_cd=url_schid).count()
            else:
                st_detail_i.menber_num = '0'

        # ---------------------------------------------------------------------------------
        # 期間予定
        # ---------------------------------------------------------------------------------
        elif url_schty == 'spn':
            # DBアクセス【スケジュール(期間)】：スケジュールコード指定で１レコード取得
            q_sch_spn = TrnScheduleSpan.objects.filter(span_schedule_cd=url_schid).first()
            # DBアクセス【予定メニュー登録マスタ】：表示名取得
            if q_sch_spn.schedule_type_cd is not None:
                q_sch_type = MstScheduleType.objects.filter(schedule_type_cd=q_sch_spn.schedulse_type_cd)
                if q_sch_type.exists():
                    st_detail_i.tag_title = q_sch_type[0].schedule_type_name + '：'

            # タグ名 & 予定タイトル
            st_detail_i.tag_title += q_sch_spn.span_schedule_name

            # 登録情報
            account_i = lib_get_account_i(q_sch_spn.span_schedule_register)
            st_detail_i.regist_i = account_i.disp_name + '   ' + q_sch_spn.span_schedule_regist_dt.strftime('%Y').lstrip('0') \
                                   + '/' + q_sch_spn.span_schedule_regist_dt.strftime('%m').lstrip('0') \
                                   + '/' + q_sch_spn.span_schedule_regist_dt.strftime('%d').lstrip('0') \
                                   + '(' + lib_chg_youbi_eng_to_jpn(q_sch_spn.span_schedule_regist_dt.strftime('%a')) + ')' \
                                   + ' ' + q_sch_spn.span_schedule_regist_dt.strftime('%H') \
                                   + ':' + q_sch_spn.span_schedule_regist_dt.strftime('%M')

            # 登録者ICON種別
            if my_account.account_cd == account_i.account_cd :
                st_detail_i.regist_icon = '1'

            # 更新情報
            if q_sch_spn.span_schedule_chg is not None:
                account_i = lib_get_account_i(q_sch_spn.span_schedule_chg)
                st_detail_i.change_i = account_i.disp_name + '   ' + q_sch_spn.span_schedule_chg_dt.strftime('%Y').lstrip('0') \
                                       + '/' + q_sch_spn.span_schedule_chg_dt.strftime('%m').lstrip('0') \
                                       + '/' + q_sch_spn.span_schedule_chg_dt.strftime('%d').lstrip('0') \
                                       + '(' + lib_chg_youbi_eng_to_jpn(q_sch_spn.span_schedule_chg_dt.strftime('%a')) + ')' \
                                       + ' ' + q_sch_spn.span_schedule_chg_dt.strftime('%H') \
                                       + ':' + q_sch_spn.span_schedule_chg_dt.strftime('%M')

                # 更新者ICON種別
                if my_account.account_cd == account_i.account_cd :
                    st_detail_i.change_icon = '1'
                else:
                    st_detail_i.regist_icon = '0'

            # 日時情報
            reg_day_wk = q_sch_spn.span_schedule_s_date.strftime('%Y').lstrip('0') \
                                       + ' 年 ' + q_sch_spn.span_schedule_s_date.strftime('%m').lstrip('0') \
                                       + ' 月 ' + q_sch_spn.span_schedule_s_date.strftime('%d').lstrip('0') \
                                       + ' 日 (' + lib_chg_youbi_eng_to_jpn(q_sch_spn.span_schedule_s_date.strftime('%a'))
            st_detail_i.d_t = reg_day_wk + ') ～ ' + q_sch_spn.span_schedule_e_date.strftime('%Y').lstrip('0') \
                              + ' 年 ' + q_sch_spn.span_schedule_e_date.strftime('%m').lstrip('0') \
                              + ' 月 ' + q_sch_spn.span_schedule_e_date.strftime('%d').lstrip('0') \
                              + ' 日 (' + lib_chg_youbi_eng_to_jpn(q_sch_spn.span_schedule_e_date.strftime('%a')) + ')'

            # メモ情報
            if q_sch_spn.span_schedule_memo is not None:
                st_detail_i.memo_i = q_sch_spn.span_schedule_memo

            # 施設情報
            # DBアクセス【スケジュール施設】
            q_sch_institution = TrnScheduleInstitution.objects.filter(schedule_cd=q_sch_spn.span_schedule_cd, schedule_type=3)
            if q_sch_institution.exists():
                for sch_institution in q_sch_institution:
                    # DBアクセス【施設登録マスタ】：施設名取得
                    q_institution = MstInstitution.objects.filter(institution_cd=sch_institution.institution_cd)
                    if q_institution.exists():
                        st_detail_i.institution_i.append(q_institution[0].institution_name)

            # メンバー情報
            # DBアクセス【スケジュール参加者(期間)】
            q_sch_member = TrnScheduleMmemberSpan.objects.filter(span_schedule_cd=url_schid)
            if q_sch_member.exists():
                for sch_member in q_sch_member:
                    # 戻り構造体
                    st_member = StMember()
                    # アカウント情報取得
                    account_i = lib_get_account_i(sch_member.account_cd)
                    st_member.disp_name = account_i.disp_name
                    if my_account.account_cd == account_i.account_cd:
                        st_member.icon_type = '1'  # 自アカウント
                    elif account_i.is_valid == True:
                        st_member.icon_type = '99'  # 無効アカウント
                    else:
                        st_member.icon_type = '0'  # その他
                    st_detail_i.member_i.append(st_member)
                st_detail_i.menber_num = TrnScheduleMmemberSpan.objects.filter(span_schedule_cd=url_schid).count()
            else:
                st_detail_i.menber_num = '0'

        # ---------------------------------------------------------------------------------
        # 繰り返し予定
        # ---------------------------------------------------------------------------------
        else: # url_schty == 'rep':
            # タグ名 & 予定タイトル
            st_detail_i.tag_title = ''
            # 登録情報
            st_detail_i.regist_i = ''
            # 更新情報
            st_detail_i.change_i = ''
            # 日時情報
            st_detail_i.d_t = ''
            # メモ情報
            st_detail_i.memo_i = ''
            # 施設情報
            st_detail_i.institution_i = ''

        # メンバーリストに自アカウントが含まれるか確認
        if any(value.icon_type == '1' for value in st_detail_i.member_i):
            st_detail_i.my_sch_flg = '0'
        else:
            st_detail_i.my_sch_flg = '1'

        return st_detail_i

    #---------------------------------------------------------------------------------
    # 関数名：変更するボタンリンク情報作成
    # 引　数：なし
    # 戻り値：リンク用URL　※パラメータ含む
    # 備　考：
    #---------------------------------------------------------------------------------
    @cached_property # リクエスト単位でキャッシュ
    def get_schchange_param(self):
        # パラメータ取得
        url_id = lib_get_url_id(self)
        url_trday = lib_get_url_trday(self)
        url_pp = lib_get_url_pp(self)
        url_ppgr = lib_get_url_ppgr(self)
        url_schty = lib_get_url_schty(self)

        # パラメータ情報作成
        query_string = urlencode({'id': url_id, 'trday': url_trday, 'PP': url_pp, 'PPGr': url_ppgr, 'schty': url_schty})

        # URLを逆引きして、パラメータを追加
        if url_schty == 'nml' or url_schty == 'cte':
            ret_param = reverse('schedule:schedule_change') + f'?{query_string}'
        elif url_schty == 'spn':
            ret_param = reverse('schedule:schedule_change_span') + f'?{query_string}'
        else:
            ret_param = reverse('schedule:schedule_change_repeat') + f'?{query_string}'

        return ret_param

    #---------------------------------------------------------------------------------
    # 関数名：削除するボタンリンク情報作成
    # 引　数：なし
    # 戻り値：リンク用URL　※パラメータ含む
    # 備　考：
    #---------------------------------------------------------------------------------
    @cached_property # リクエスト単位でキャッシュ
    def get_schdelete_param(self):
        # パラメータ取得
        url_id = lib_get_url_id(self)
        url_trday = lib_get_url_trday(self)
        url_pp = lib_get_url_pp(self)
        url_ppgr = lib_get_url_ppgr(self)
        url_schid = lib_get_url_schid(self)
        url_schty = lib_get_url_schty(self)

        # パラメータ情報作成
        query_string = urlencode({'id': url_id, 'trday': url_trday, 'PP': url_pp, 'PPGr': url_ppgr, 'schid': url_schid,
                                  'schty': url_schty, 'msgty': 'del'})

        # URLを逆引きして、パラメータを追加
        ret_param = reverse('schedule:schedule_message') + f'?{query_string}'

        return ret_param

    #---------------------------------------------------------------------------------
    # 関数名：この予定から抜けるボタンリンク情報作成
    # 引　数：なし
    # 戻り値：リンク用URL　※パラメータ含む
    # 備　考：
    #---------------------------------------------------------------------------------
    @cached_property # リクエスト単位でキャッシュ
    def get_schout_param(self):
        # パラメータ取得
        url_id = lib_get_url_id(self)
        url_trday = lib_get_url_trday(self)
        url_pp = lib_get_url_pp(self)
        url_ppgr = lib_get_url_ppgr(self)
        url_schid = lib_get_url_schid(self)
        url_schty = lib_get_url_schty(self)

        # パラメータ情報作成
        query_string = urlencode({'id': url_id, 'trday': url_trday, 'PP': url_pp, 'PPGr': url_ppgr, 'schid': url_schid,
                                  'schty': url_schty, 'msgty': 'out'})

        # URLを逆引きして、パラメータを追加
        ret_param = reverse('schedule:schedule_message') + f'?{query_string}'

        return ret_param

    #---------------------------------------------------------------------------------
    # 関数名：この予定に参加するボタンリンク情報作成
    # 引　数：なし
    # 戻り値：リンク用URL　※パラメータ含む
    # 備　考：
    #---------------------------------------------------------------------------------
    @cached_property # リクエスト単位でキャッシュ
    def get_schjoin_param(self):
        # パラメータ取得
        url_id = lib_get_url_id(self)
        url_trday = lib_get_url_trday(self)
        url_pp = lib_get_url_pp(self)
        url_ppgr = lib_get_url_ppgr(self)
        url_schid = lib_get_url_schid(self)
        url_schty = lib_get_url_schty(self)

        # パラメータ情報作成
        query_string = urlencode({'id': url_id, 'trday': url_trday, 'PP': url_pp, 'PPGr': url_ppgr, 'schid': url_schid,
                                  'schty': url_schty, 'msgty': 'join'})

        # URLを逆引きして、パラメータを追加
        ret_param = reverse('schedule:schedule_message') + f'?{query_string}'

        return ret_param
