from django.contrib import admin                        #管理ページ用のオブジェクトをインポート
from django.contrib.staticfiles.urls import static      #メディアファイル配信用
from django.urls import path,include                    #ルーティング用の関数をインポート
from . import settings_common, settings_dev

#ルーティングの内容をリストに記載
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('infomation.urls')),
    path('accounts/', include('allauth.urls')),
    path('overview/', include('overview.urls')),
    path('schedule', include('schedule.urls')),
    path('timecard/', include('timecard.urls')),
    path('directory/', include('directory.urls')),
    path('report/', include('report.urls')),
    path('workflow/', include('workflow.urls')),
    path('infoboard/', include('infoboard.urls')),
    path('message/', include('message.urls')),
    path('mail/', include('mail.urls')),
    path('task/', include('task.urls')),
    path('project/', include('project.urls')),
    path('equipment/', include('equipment.urls')),
    path('employee/', include('employee.urls')),
    path('employeeinfo/', include('employeeinfo.urls')),
    path('rpa/', include('rpa.urls')),
    path('syssetting/', include('syssetting.urls'))
]

# 開発サーバーでメディアを配信できるようにする設定
urlpatterns += static(settings_common.MEDIA_URL, document_root=settings_dev.MEDIA_ROOT)
