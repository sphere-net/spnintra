#path関数をインポート
from django.urls import  path
#ビューの設定ファイルをインポート
from.import views

#アプリケーション名の指定（他に同じルーティングのある時に識別する用）
app_name = 'workflow'

#ルーティング
urlpatterns = [
    path('', views.WorkflowIndexView.as_view(), name='workflow_index'),
]
