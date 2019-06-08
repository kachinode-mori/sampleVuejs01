from django.urls import path
from . import views


urlpatterns = [
    # wants home画面
    path('', views.wantshome, name='wants'),
    # wants list(user.id)
    path('list/<int:id>/', views.WantsListView.as_view(), name='wants_list'),
    # 新規作成
    path('create/', views.wantscreate, name='wants_create'),
    # wants編集(want.id)
    path('update/<int:id>/', views.wantsupdate, name='wants_update'),
    # wants達成入力(want.id)
    path('achieve/<int:id>/', views.wantsachieve, name='wants_achieve'),
    # wants削除(want.id)
    path('delete/<int:id>/', views.wantsdelete, name='wants_delete'),
    # wantsいいね(want.id)
    path('like/<int:id>/', views.wantslike, name='wants_like'),
    #ユーザlikes一覧
    path('ulikelist/<int:id>', views.ulikelist, name='ulike_list'),
    #いいねranking一覧
    path('ranklist/', views.ranklist, name='rank_list'),
    #path('ranklist/', views.RankListView.as_view(), name='rank_list'),

    # タブ区切りダウンロード(user.id)
    path('export/<int:id>', views.download, name='export'),

    #api画面テスト
    path('wantsapi/', views.apihome, name='wantsapp'),

]

    #path('list/<int:id>/', views.wantslist, name='wants_list'),
    #path('', views.WantsListView.as_view(), name='wants_list'),
    #path('achieve/<int:id>/', views.WantsAchieveView.as_view(), name='wants_achieve'),
    #path('addedit/<int:id>/', views.wantsaddedit, name='wants_addedit'),
    #path('update/<int:id>/', views.WantsUpdateView.as_view(), name='wants_update'),
    #path('achieve/<int:id>/', views.wantsachieve, name='wants_achieve'),
    #path('create/', views.WantsCreateView.as_view(), name='wants_form'),
    #path('delete/<int:id>/', views.WantsDeleteView.as_view(), name='wants_delete'),
    #path('detail/<int:id>/', views.TodoDetailView.as_view(), name='todo_detail'),
