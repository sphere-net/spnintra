#path関数をインポート
from django.urls import  path
#ビューの設定ファイルをインポート
from.import views

#アプリケーション名の指定（他に同じルーティングのある時に識別する用）
app_name = 'report'

#ルーティング
urlpatterns = [
    path('', views.ReportIndexView.as_view(), name='report_index'),
]
