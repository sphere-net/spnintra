#path関数をインポート
from django.urls import  path
#ビューの設定ファイルをインポート
from.import views

#アプリケーション名の指定（他に同じルーティングのある時に識別する用）
app_name = 'equipment'

#ルーティング
urlpatterns = [
    path('', views.EquipmentIndexView.as_view(), name='equipment_index'),
]
