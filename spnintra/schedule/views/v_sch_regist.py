from django.http import HttpResponse
from django.shortcuts import redirect
from urllib.parse import urlencode
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.functional import cached_property
# モデルインポート
from overview.models import *
from schedule.models import *
# 標準インポート
from django.db import transaction
from django.db.models import F
from django.db.models import Max
import datetime
import time
# オリジナルライブラリインポート
from commonutil.libraries import *
#この下はお試し用
from schedule.forms import ScheduleRegistForm

#=====================================================================================
# スケジュール登録画面 ※ログインしていないと見れないページ
#=====================================================================================
class ScheduleRegView(LoginRequiredMixin, FormView):
    template_name = "regist.html"
    form_class = ScheduleRegistForm
    #success_url = '/'  # リダイレクト先URL

    # ---------------------------------------------------------------------------------
    # 関数名：URLパラメータ取得　※HTML使用
    # ---------------------------------------------------------------------------------
    def get_url_schty(self):
        return lib_get_url_schty(self)

    #---------------------------------------------------------------------------------
    # 関数名：formにパラメータを渡す
    # 引　数：なし
    # 戻り値：
    # 備　考：
    #---------------------------------------------------------------------------------
    def get_form_kwargs(self, *args, **kwargs):
        kwgs = super().get_form_kwargs(*args, **kwargs)

        # ---------------------------------------------------------------------------------
        # URLパラメータ取得
        # ---------------------------------------------------------------------------------
        # 対象日
        url_param = lib_get_url_trday(self)
        tr_year = url_param[0:4]
        tr_month = url_param[5:7].lstrip('0')
        tr_day = url_param[8:10].lstrip('0')

        # 対象グループ
        default_gr = lib_get_url_ppgr(self)

        # 自アカウント
        q_my_account = lib_get_my_account_i(self)

        # ---------------------------------------------------------------------------------
        # 年コンボボックス要素作成　※一旦リスト型で作って、タプル型に変更しないとダメだった。。。
        # ---------------------------------------------------------------------------------
        # DBアクセス【プロジェクト設定マスタ】
        q_s_year = MstProjectConfig.objects.filter(pj_config_kubun_cd='sch_date', pj_config_key='s_year').first()
        q_e_year = MstProjectConfig.objects.filter(pj_config_kubun_cd='sch_date', pj_config_key='e_year').first()

        # コンボボックス用リスト（宣言）
        date_year: list[int, str] = []

        # コンボボックス中身
        for iLoop in range(int(q_s_year.pj_config_value), int(q_e_year.pj_config_value), 1):
            date_year.append([iLoop, str(iLoop) + '年'])

        # コンボボックスリストをタプルに変換して送信用データ作成
        kwgs["date_year"] = tuple(date_year)

        # 初期選択データ作成
        kwgs["date_year_select"] = tr_year
        kwgs["date_month_select"] = tr_month

        # ---------------------------------------------------------------------------------
        # 日コンボボックス要素作成
        # ---------------------------------------------------------------------------------
        # コンボボックス用リスト（宣言）
        date_day: list[int, str] = []
        date_day = lib_get_target_days(tr_year, tr_month)

        # コンボボックスリストをタプルに変換して送信用データ作成
        kwgs["date_day"] = tuple(date_day)

        # 初期選択データ作成
        kwgs["date_day_select"] = tr_day

        # ---------------------------------------------------------------------------------
        # 予定タグコンボボックス要素作成
        # ---------------------------------------------------------------------------------
        # コンボボックス用リスト（宣言）
        yotei_cat: list[str, str] = []
        yotei_cat.append(['0', '--'])
        # DBアクセス【予定メニュー登録マスタ】：表示名取得
        q_sch_type = MstScheduleType.objects.order_by('disp_order')

        # コンボボックス中身
        if q_sch_type.exists():
            for type_value in q_sch_type:

                # DBアクセス【予定色マスタ】：予定色RGBコード取得
                q_sch_type_color = MstScheduleTypeColor.objects.filter(
                    schedule_type_color_cd=type_value.schedule_type_color_cd)
                if q_sch_type_color.exists():
                    # 色コードが取れた場合、表示名の先頭に色コードを追加する　※JSで加工
                    yotei_cat.append([type_value.schedule_type_cd,
                                      '#' + q_sch_type_color[0].schedule_type_rgb + ',' + type_value.schedule_type_name])
                else:
                    yotei_cat.append([type_value.schedule_type_cd, type_value.schedule_type_name])

        # コンボボックスリストをタプルに変換して送信用データ作成
        kwgs["yotei_cat"] = tuple(yotei_cat)

        # ---------------------------------------------------------------------------------
        # グループコンボボックス要素作成
        # ---------------------------------------------------------------------------------
        # コンボボックス用リスト（宣言）
        gr: list[str, str] = []
        gr.append(['0', '(全員)'])
        # DBアクセス【グループマスタ】
        q_gr_list = MstGroup.objects.order_by('disp_order')

        # コンボボックス中身
        if q_gr_list.exists():
            for gr_value in q_gr_list:
                gr.append([gr_value.group_cd, gr_value.group_name])

        # コンボボックスリストをタプルに変換して送信用データ作成
        kwgs["disp_gr"] = tuple(gr)

        # 初期選択データ作成
        kwgs["disp_gr_select"] = default_gr

        # ---------------------------------------------------------------------------------
        # グループメンバーリスト要素作成
        # ---------------------------------------------------------------------------------
        # コンボボックス用リスト（宣言）
        gr_member: list[str, str] = []
        gr_member = lib_get_target_gr_members(default_gr)

        # コンボボックスリストをタプルに変換して送信用データ作成
        kwgs["gr_member"] = tuple(gr_member)

        # ---------------------------------------------------------------------------------
        # 施設コンボボックス要素作成
        # ---------------------------------------------------------------------------------
        # コンボボックス用リスト（宣言）
        setu: list[str, str] = []
        # DBアクセス【施設グループ登録マスタ】
        q_setu_list = MstInstitutionGroup.objects.order_by('institution_group_disp_order')

        # コンボボックス中身
        if q_setu_list.exists():
            for setu_value in q_setu_list:
                setu.append([setu_value.institution_group_cd, setu_value.institution_group_name])

        # コンボボックスリストをタプルに変換して送信用データ作成
        kwgs["setu_gr"] = tuple(setu)

        # ---------------------------------------------------------------------------------
        # 施設一覧リスト要素作成
        # ---------------------------------------------------------------------------------
        # コンボボックス用リスト（宣言）
        setu_member: list[str, str] = []

        # コンボボックス中身
        if q_setu_list.exists():
            setu_member = lib_get_target_sisetsu_members(q_setu_list[0].institution_group_cd)

        # コンボボックスリストをタプルに変換して送信用データ作成
        kwgs["setu_member"] = tuple(setu_member)

        # ---------------------------------------------------------------------------------
        # 参加者リスト要素作成
        # ---------------------------------------------------------------------------------
        # コンボボックス用リスト（宣言）
        my_account: list[str, str] = []

        # アカウント情報取得
        account_i = lib_get_account_i(lib_get_url_id(self))

        # コンボボックス中身
        my_account.append([account_i.account_cd, account_i.disp_name])

        # コンボボックスリストをタプルに変換して送信用データ作成
        kwgs["my_account"] = tuple(my_account)

        return kwgs

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
            u_prm_schty = lib_get_url_schty(self)

            # フォームデータ取得
            f_sv_syear = self.request.POST.get('f_s_year', None)
            f_sv_smonth = self.request.POST.get('f_s_month', None)
            f_sv_sday = self.request.POST.get('f_s_day', None)
            if u_prm_schty == 'nml' or  u_prm_schty == 'cte' or u_prm_schty == 'rep':
                f_sv_shour = self.request.POST.get('f_s_hour', None)
                f_sv_sminute = self.request.POST.get('f_s_minutes', None)
            if u_prm_schty == 'cte' or u_prm_schty == 'spn':
                f_sv_eyear = self.request.POST.get('f_e_year', None)
                f_sv_emonth = self.request.POST.get('f_e_month', None)
                f_sv_eday = self.request.POST.get('f_e_day', None)
            if u_prm_schty == 'nml' or  u_prm_schty == 'cte' or u_prm_schty == 'rep':
                f_sv_ehour = self.request.POST.get('f_e_hour', None)
                f_sv_eminute = self.request.POST.get('f_e_minutes', None)
            f_sv_tag = self.request.POST.get('f_tag', None)
            f_sv_title = self.request.POST['f_title']
            f_sv_memo = self.request.POST['f_memo']
            f_sv_member = self.request.POST.getlist('f_member_l', None)
            f_sv_stu = self.request.POST.getlist('f_setu_l', None)

            # フォームデータ変換：共通
            s_dt = datetime.date(int(f_sv_syear), int(f_sv_smonth), int(f_sv_sday))

            # 特殊処理
            if u_prm_schty == 'cte' or u_prm_schty == 'spn':
                # 終了日
                e_dt = datetime.date(int(f_sv_eyear), int(f_sv_emonth), int(f_sv_eday))
                if s_dt == e_dt:
                    # 継続、期間で開始日と終了日が同じだった場合、通常予定とする
                    sch_chg_flg = True

            # DB登録：共通
            create_id = '00000001'
            # タイトル
            if f_sv_title is not None:
                sch_name = str(f_sv_title)
            else:
                sch_name = '--'
            # メモ
            if f_sv_memo is not None:
                sch_memo = str(f_sv_memo)
            else:
                sch_memo = None
            # 公開／非公開設定
            is_release = False

            # 【トランザクション開始】
            with transaction.atomic():
                # ---------------------------------------------------------------------------------
                # DB登録：通常予定
                # ---------------------------------------------------------------------------------
                if u_prm_schty == 'nml' or sch_chg_flg == True:
                    # スケジュールID
                    # DBアクセス【スケジュール(通常)】：最後の登録
                    last_create_dt = TrnScheduleNormal.objects.all().aggregate(Max('normal_schedule_regist_dt'))
                    if last_create_dt is not None:
                        q_last_create = TrnScheduleNormal.objects.filter(normal_schedule_regist_dt=last_create_dt['normal_schedule_regist_dt__max'])
                        if q_last_create.exists():
                            create_id = str(int(q_last_create[0].normal_schedule_cd)+1).zfill(8)
                    # 時刻
                    if int(f_sv_shour) != 99 and int(f_sv_sminute) != 99 and int(f_sv_ehour) != 99 and int(f_sv_eminute) != 99:
                        s_time = datetime.time(hour=int(f_sv_shour), minute=int(f_sv_sminute), second=0, microsecond=0, tzinfo=None)
                        e_time = datetime.time(hour=int(f_sv_ehour), minute=int(f_sv_eminute), second=0, microsecond=0, tzinfo=None)
                    else:
                        s_time = None
                        e_time = None

                    # DBアクセス【スケジュール(通常)】：登録
                    create_caram = TrnScheduleNormal(normal_schedule_cd=create_id,
                                                     normal_schedule_date=s_dt,
                                                     normal_schedule_s_time=s_time,
                                                     normal_schedule_e_time=e_time,
                                                     company_cd='',
                                                     schedule_type_cd=str(f_sv_tag),
                                                     normal_schedule_name=sch_name,
                                                     normal_schedule_memo=sch_memo,
                                                     normal_schedule_register=my_account.account_cd,
                                                     normal_schedule_regist_dt=datetime.datetime.now(),
                                                     normal_schedule_chg=None,
                                                     normal_schedule_chg_dt=None,
                                                     is_normal_schedule_release=is_release)
                    create_caram.save()

                    # DBアクセス【ケジュール参加者(通常)】
                    count = 0;
                    for value in f_sv_member:
                        create_caram2 = TrnScheduleMmemberNormal(normal_schedule_cd_id=create_id, account_cd=value, disp_order=count)
                        create_caram2.save()
                        count = count + 1

                    # 施設タイプ
                    sch_type = 1

                # ---------------------------------------------------------------------------------
                # DB登録：翌日以降まで続く予定
                # ---------------------------------------------------------------------------------
                elif u_prm_schty == 'cte':
                    # スケジュールID
                    # DBアクセス【スケジュール(継続)】：最後の登録
                    last_create_dt = TrnScheduleContinue.objects.all().aggregate(Max('continue_schedule_regist_dt'))
                    if last_create_dt is not None:
                        q_last_create = TrnScheduleContinue.objects.filter(continue_schedule_regist_dt=last_create_dt['continue_schedule_regist_dt__max'])
                        if q_last_create.exists():
                            create_id = str(int(q_last_create[0].continue_schedule_cd)+1).zfill(8)
                    # 時刻
                    if int(f_sv_shour) != 99 and int(f_sv_sminute) != 99 and int(f_sv_ehour) != 99 and int(f_sv_eminute) != 99:
                        s_time = datetime.time(hour=int(f_sv_shour), minute=int(f_sv_sminute), second=0, microsecond=0, tzinfo=None)
                        e_time = datetime.time(hour=int(f_sv_ehour), minute=int(f_sv_eminute), second=0, microsecond=0, tzinfo=None)
                    else:
                        s_time = None
                        e_time = None

                    # DBアクセス【スケジュール(継続)】：登録
                    create_caram = TrnScheduleContinue(continue_schedule_cd=create_id,
                                                       continue_schedule_s_date=s_dt,
                                                       continue_schedule_s_time=s_time,
                                                       continue_schedule_e_date=e_dt,
                                                       continue_schedule_e_time=e_time,
                                                       company_cd='',
                                                       schedule_type_cd=str(f_sv_tag),
                                                       continue_schedule_name=sch_name,
                                                       continue_schedule_memo=sch_memo,
                                                       continue_schedule_register=my_account.account_cd,
                                                       continue_schedule_regist_dt=datetime.datetime.now(),
                                                       continue_schedule_chg=None,
                                                       continue_schedule_chg_dt=None,
                                                       is_continue_schedule_release=is_release)
                    create_caram.save()

                    # DBアクセス【ケジュール参加者(継続)】
                    count = 0;
                    for value in f_sv_member:
                        create_caram2 = TrnScheduleMmember(continue_schedule_cd_id=create_id, account_cd=value, disp_order=count)
                        create_caram2.save()
                        count = count + 1

                    # 施設タイプ
                    sch_type = 2

                # ---------------------------------------------------------------------------------
                # DB登録：期間予定
                # ---------------------------------------------------------------------------------
                elif u_prm_schty == 'spn':
                    # スケジュールID
                    # DBアクセス【スケジュール(期間)】：最後の登録
                    last_create_dt = TrnScheduleSpan.objects.all().aggregate(Max('span_schedule_regist_dt'))
                    if last_create_dt is not None:
                        q_last_create = TrnScheduleSpan.objects.filter(span_schedule_regist_dt=last_create_dt['span_schedule_regist_dt__max'])
                        if q_last_create.exists():
                            create_id = str(int(q_last_create[0].span_schedule_cd)+1).zfill(8)

                    # DBアクセス【スケジュール(期間)】：登録
                    create_caram = TrnScheduleSpan(span_schedule_cd=create_id,
                                                   span_schedule_s_date=s_dt,
                                                   span_schedule_e_date=e_dt,
                                                   company_cd='',
                                                   schedule_type_cd=str(f_sv_tag),
                                                   span_schedule_name=sch_name,
                                                   span_schedule_memo=sch_memo,
                                                   span_schedule_register=my_account.account_cd,
                                                   span_schedule_regist_dt=datetime.datetime.now(),
                                                   span_schedule_chg=None,
                                                   span_schedule_chg_dt=None,
                                                   is_span_schedule_release=is_release)
                    create_caram.save()

                    # DBアクセス【ケジュール参加者(期間)】
                    count = 0;
                    for value in f_sv_member:
                        create_caram2 = TrnScheduleMmemberSpan(span_schedule_cd_id=create_id, account_cd=value, disp_order=count)
                        create_caram2.save()
                        count = count + 1

                    # 施設タイプ
                    sch_type = 3

                # ---------------------------------------------------------------------------------
                # DB登録：繰り返し予定
                # ---------------------------------------------------------------------------------
                else:
                    # DBアクセス【スケジュール(リピート)】
                    q_my_account = MstAccount.objects.filter(user_id=self.request.user).first()

                    # DBアクセス【ケジュール参加者(リピート)】
                    count = 0;
                    for value in f_sv_member:
                        create_caram2 = TrnScheduleMmemberRepeat(normal_schedule_cd_id=create_id, account_cd=value, disp_order=count)
                        create_caram2.save()
                        count = count + 1

                    # 施設タイプ
                    sch_type = 4

                # ---------------------------------------------------------------------------------
                # 全予定共通：DBアクセス【スケジュール施設】
                # ---------------------------------------------------------------------------------
                count = 0;
                for value in f_sv_stu:
                    create_caram3 = TrnScheduleInstitution(schedule_cd=create_id,
                                                           schedule_type=sch_type,
                                                           institution_cd=value,
                                                           disp_order=count)
                    create_caram3.save()
                    count = count + 1

            # 【トランザクション終了】

            # DBアクセス【スケジュールファイル】

            # リダイレクト情報作成作成
            o_prm_trday = str(f_sv_syear) + '.' + str(f_sv_smonth).zfill(2) + '.' + str(f_sv_sday).zfill(2)

            # スケジュール種別を変更していた場合、リンクパラメータも変える
            if sch_chg_flg == True:
                remake_schty = 'nml'
            else:
                remake_schty = u_prm_schty

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
                                      'schid': create_id,
                                      'schty': remake_schty})

            # URLを逆引きして、パラメータを追加　※遷移先は詳細
            url = reverse('schedule:schedule_detail') + f'?{query_string}'
            return redirect(url)

        # POST以外（失敗含む）は、元の画面に戻る
        return self.get(request, *args, **kwargs)

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
    # 関数名：登録画面へのリンク用パラメータ作成（登録種別除く）
    # 引　数：なし
    # 戻り値：リンク用URLパラメータ
    # 備　考：登録種別は除く　※上部タブで登録種別切り替えリンク用
    #---------------------------------------------------------------------------------
    @cached_property # リクエスト単位でキャッシュ
    def get_linkurl_outof_schtype(self):
        # パラメータ取得
        url_id = lib_get_url_id(self)
        url_trday = lib_get_url_trday(self)
        url_pp = lib_get_url_pp(self)
        url_ppgr = lib_get_url_ppgr(self)

        # 戻り情報作成
        ret_param = '?id=' + url_id + '&trday=' + url_trday + '&PP=' + url_pp + '&PPGr=' + url_ppgr + '&schty='

        return ret_param

    #---------------------------------------------------------------------------------
    # 関数名：登録SUBMITへのリンク用パラメータ作成（登録種別含む）
    # 引　数：なし
    # 戻り値：リンク用URLパラメータ
    # 備　考：登録種別含む　※Sbumit後のリダイレクト用
    #---------------------------------------------------------------------------------
    @cached_property # リクエスト単位でキャッシュ
    def get_regist_param(self):
        return lib_make_url_prm_id_trday_pp_ppgr_schty(self)

    #---------------------------------------------------------------------------------
    # 関数名：キャンセルボタンへのリンク用URL作成
    # 引　数：なし
    # 戻り値：URL
    # 備　考：
    #---------------------------------------------------------------------------------
    @cached_property # リクエスト単位でキャッシュ
    def get_redirect_param(self):
        return lib_make_url_to_pp(self)



