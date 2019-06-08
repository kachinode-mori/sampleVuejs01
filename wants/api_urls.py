from rest_framework import routers
from . import api_views

from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import verify_jwt_token


router = routers.DefaultRouter()
router.register('users', api_views.UserViewSet)
router.register('wants', api_views.WantViewSet)
router.register('likes', api_views.LikeViewSet)
router.register('userinfo', api_views.UserInfoViewSet)
router.register('userwants', api_views.UserWantsViewSet)
router.register('userlikes', api_views.UserLikesViewSet)

urlpatterns = [
    # ユーザ認証
    path('auth/', obtain_jwt_token),
    path('auth/verify/', verify_jwt_token),
    # path('register/', api_views.AuthRegister.as_view()),    #ユーザの新規登録：apiでできたので必要なかった

    # ユーザ削除(退会)
    path('userdelete/', api_views.userdelete),

    # # UserWantsList
    # path('userwantlist/<int:id>', api_views.UserWantList),

    # wants追加
    path('wantscreate/', api_views.wantscreate),

    # wantsデータ更新(displayOrder用)
    path('wantsupdate/', api_views.wantsupdate),

    # wants削除(want.id)
    path('delete/<int:id>/', api_views.wantsdelete),

    # likesボタンの押下(want.id)
    path('likepush/<int:id>/', api_views.likepush),

]
