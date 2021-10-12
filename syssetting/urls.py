#path関数をインポート
from django.urls import  path
#ビューの設定ファイルをインポート
from.views import v_sys_index
from.views import v_sys_schedule

#アプリケーション名の指定（他に同じルーティングのある時に識別する用）
app_name = 'syssetting'

#ルーティング
urlpatterns = [
    path('', v_sys_index.SysSettingIndexView.as_view(), name='syssetting_index'),
    path('schedule/', v_sys_schedule.SysSettingScheduleView.as_view(), name='syssetting_schedule'),
]
