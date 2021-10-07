#path関数をインポート
from django.urls import  path
#ビューの設定ファイルをインポート
from.import views

#アプリケーション名の指定（他に同じルーティングのある時に識別する用）
app_name = 'infomation'

#ルーティング
urlpatterns = [
    path('', views.IndexView.as_view(), name='infomation_index'),
    path('inquiry/', views.InquiryView.as_view(), name='infomation_inquiry')
]
