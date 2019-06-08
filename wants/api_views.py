from django.db import transaction
from django.http.response import HttpResponse, Http404
from django.contrib.auth import authenticate

from rest_framework_jwt.settings import api_settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions, authentication
# from rest_framework import viewsets, filters, generics, status
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
#from rest_framework.views import APIView

from .models import Want, Like, User
from .serializer import UserSerializer, WantSerializer, LikeSerializer, PasswordSerializer
# from rest_framework.decorators import list_route
from rest_framework.decorators import action

import os
import csv
import urllib
import django_filters


# API User一覧
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_fields = ('id', 'email', 'nickname')

    # ユーザパスワード更新
    @action(methods=['post'], detail=True)
    def set_password(self, request, pk=None):
        serializer = PasswordSerializer(data=request.data)
        user = self.get_object()

        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                return Response({'oldPassword': ['元のパスワードが違います。確認して下さい']},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response({'status': 'password set'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API Want一覧
class WantViewSet(viewsets.ModelViewSet):
    queryset = Want.objects.all()
    serializer_class = WantSerializer

# API Like一覧
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

# ログインユーザのユーザ情報取得
class UserInfoViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(email=user)

# ログインユーザID別want一覧
class UserWantsViewSet(viewsets.ModelViewSet):
    queryset = Want.objects.all()
    serializer_class = WantSerializer

    def get_queryset(self):
        user = self.request.user
        # return Want.objects.filter(user=user).order_by('-create_date')
        # return Want.objects.filter(user=user).order_by('display_order')
        return Want.objects.filter(user=user).order_by('display_order', '-id')

# ログインユーザID別likes一覧
class UserLikesViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_queryset(self):
        user = self.request.user
        return Like.objects.filter(user=user)

# #
# class UserWantList(generics.ListAPIView):
#     serializer_class = WantSerializer
#     print(serializer_class)

#     def get_queryset(self):
#         user = self.kwargs['user']
#         return Want.objects.filter(want__user=user)


# wants追加
@api_view(['PUT'])
def wantscreate(request):

    # # display_orderのMAX値を取得
    # uwant_disnum = Want.objects.filter(user=request.user).aggregate(Max('display_order'))
    # # Max値が取得できなかった場合、はじめての新規登録なので、1を設定
    # if uwant_disnum['display_order__max'] is None:
    #     maxnum = 1
    # # それ以外の場合、+1を設定
    # else:
    #     maxnum = uwant_disnum['display_order__max'] + 1
    #
    # request.data['display_order'] = maxnum

    request.data['user'] = request.user.id
    want = WantSerializer(data=request.data)
    if want.is_valid():
        want.save()
        return Response(want.data, status=status.HTTP_201_CREATED)
    return Response(want.errors, status=status.HTTP_400_BAD_REQUEST)


# wants更新(display_order更新用)
@api_view(['PATCH'])
def wantsupdate(request):

    for updata in request.data['upwants']:

        want = generics.get_object_or_404(Want, pk=updata['id'])
        want.display_order = updata['display_order']
        want.save()

    return Response(status=status.HTTP_204_NO_CONTENT, content_type=request.content_type)

# wants削除
@api_view(['DELETE'])
def wantsdelete(request, id):
    want = generics.get_object_or_404(Want, pk=id)
    want.delete()
    return Response(status=status.HTTP_204_NO_CONTENT, content_type=request.content_type)

# likePush
@api_view(['PUT'])
def likepush(request, id):
    want = generics.get_object_or_404(Want, pk=id)

    is_like = Like.objects.filter(user=request.user).filter(want=want).count()
    # unlike
    if is_like > 0:
        liking = Like.objects.get(want__id=id, user=request.user)
        liking.delete()
        want.like_num -= 1
        want.save()
    # like
    else:
        want.like_num += 1
        want.save()
        like = Like()
        like.user = request.user
        like.want = want
        like.save()

    return Response(status=status.HTTP_204_NO_CONTENT, content_type=request.content_type)


# ユーザ削除(DELETE) is_activeを 0 にする
@api_view(['DELETE'])
def userdelete(request):
    user = generics.get_object_or_404(User, email=request.user)
    #user.delete()
    user.is_active = 0
    user.save()
    return Response(status=status.HTTP_204_NO_CONTENT, content_type=request.content_type)


# # ユーザ作成(POST)
# class AuthRegister(generics.CreateAPIView):
#     permission_classes = (permissions.AllowAny,)
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     @transaction.atomic
#     def post(self, request, format=None):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def get_queryset(self):
    #     # status = 'doing'
    #     # return Want.objects.filter(status__contains=status)

    #     user = 3
    #     #user = self.request.user
    #     return Want.objects.filter(user=user)

# # API Want一覧
# class WantFilterViewSet(generics.ListAPIView):
#     serializer_class = WantSerializer

#     def get_queryset(self):
#         query_user_id = self.kwargs['user_id']
#         return Want.objects.filter(user=query_user_id)

# # wantsranking一覧
# @api_view(['GET'])
# class WantsList(viewsets.ViewSet):

#     def wantsranking(self, request):
#         queryset = Want.objects.all()
#         serializer = WantSerializer(queryset, many=True)
#         return Response(serializer.data)

# # tab区切りダウンロード
# @api_view(['GET'])
# def download(request, id):
#     wants = Want.objects.filter(user=id)
#     response = HttpResponse(content_type='text/csv; charset=Shift-JIS')
#     filename = urllib.parse.quote((u'MyWantsList.txt').encode("utf8"))
#     response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}'.format(filename)
#     writer = csv.writer(response, delimiter='\t')
#     for want in wants:
#         writer.writerow([want.content, want.status, want.target_date, want.publish_set, want.achieve_date, want.achieve_text, want.achieve_url])
#     return response
