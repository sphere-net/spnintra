#path関数をインポート
from django.urls import  path
#ビューの設定ファイルをインポート
from .views import v_sch_ajax
from .views import v_sch_chg
from .views import v_sch_chg_repeat
from .views import v_sch_chg_span
from .views import v_sch_detail
from .views import v_sch_gday
from .views import v_sch_gweek
from .views import v_sch_msg_only
from .views import v_sch_pday
from .views import v_sch_pmonth
from .views import v_sch_pweek
from .views import v_sch_pyear
from .views import v_sch_regist
#アプリケーション名の指定（他に同じルーティングのある時に識別する用）
app_name = 'schedule'

#ルーティング
urlpatterns = [
    path( '', v_sch_gweek.ScheduleIndexView.as_view(), name = 'schedule_index'),
    path('grpday/', v_sch_gday.ScheduleGdayView.as_view(), name='schedule_gday'),
    path('personalday/', v_sch_pday.SchedulePdayView.as_view(), name='schedule_pday'),
    path('personalweek/', v_sch_pweek.SchedulePweekView.as_view(), name='schedule_pweek'),
    path('personalmonth/', v_sch_pmonth.SchedulePmonthView.as_view(), name='schedule_pmonth'),
    path('personalyear/', v_sch_pyear.SchedulePyearView.as_view(), name='schedule_pyear'),
    path('scheduleregist', v_sch_regist.ScheduleRegView.as_view(), name='schedule_regist'),
    path('schedulechange', v_sch_chg.ScheduleChgView.as_view(), name='schedule_change'),
    path('schedulechangerepeat', v_sch_chg_repeat.ScheduleChgRepeatView.as_view(), name='schedule_change_repeat'),
    path('schedulechangespan', v_sch_chg_span.ScheduleChgSpanView.as_view(), name='schedule_change_span'),
    path('schedulemessage', v_sch_msg_only.ScheduleDelView.as_view(), name='schedule_message'),
    path('scheduledetail', v_sch_detail.ScheduleDetailView.as_view(), name='schedule_detail'),
    # 以下Ajax　※リクエストごとに関数化
    path('sch-ajax-getdays', v_sch_ajax.ScheduleAjaxGetDays, name='sch_ajax_days'),
    path('sch-ajax-getgrs', v_sch_ajax.ScheduleAjaxGetGroup, name='sch_ajax_group'),
    path('sch-ajax-getsisetus', v_sch_ajax.ScheduleAjaxGetSisetsu, name='sch_ajax_sisetsu'),
    path('sch-ajax-accounts', v_sch_ajax.ScheduleAjaxSarchAccount, name='sch_ajax_account'),
]
