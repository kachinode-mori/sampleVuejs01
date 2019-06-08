from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

from .models import Want, Like
from accounts.models import User
from .forms import WantsCreateForm, WantsUpdateForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Sum

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import os
from django.conf import settings
from django.http.response import HttpResponse
import csv
import urllib

# from django.db.models import Max

# home画面
def wantshome(request):
    ranks = Want.objects.filter(publish_set=1, like_num__gte=1).order_by('-like_num')[:5]      # __gte=1 は、>=1の意味
    wants = Want.objects.filter(publish_set=1).order_by('-create_date')[:5]
    users = User.objects.all()

    return render(request, 'home.html', dict(ranks=ranks, wants=wants, users=users))

#ユーザlikes一覧
def ulikelist(request, id):
    ulike_list = Like.objects.filter(user=id)
    paginator = Paginator(ulike_list, 50)
    page = request.GET.get('page')
    ulikes = paginator.get_page(page)
    users = User.objects.all()
    return render(request, 'ulikelist.html', dict(ulikes=ulikes, users=users))

#Ranking一覧
def ranklist(request):
    rank_list = Want.objects.filter(like_num__gte=1).order_by('-like_num')      # __gte=1 は、>=1の意味
    paginator = Paginator(rank_list, 100)
    page = request.GET.get('page')
    ranks = paginator.get_page(page)
    users = User.objects.all()
    return render(request, 'ranklist.html', dict(ranks=ranks, users=users))

# wants一覧
class WantsListView(ListView):
    #model = Want
    template_name = 'wants/list.html'
    #success_url = reverse_lazy('wants_list')

    def get_queryset(self):
        # return Want.objects.filter(user=self.kwargs['id'])
        # return Want.objects.filter(user=self.kwargs['id']).order_by('create_date')
        return Want.objects.filter(user=self.kwargs['id']).order_by('display_order', '-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_list'] = User.objects.filter(id=self.kwargs['id'])
        context['wantscount'] = self.get_queryset().count()
        context['likescount'] = self.get_queryset().aggregate(Sum('like_num')).get('like_num__sum', 0)
        context['nostart'] = self.get_queryset().filter(status='nostart').count()
        context['doing'] = self.get_queryset().filter(status='doing').count()
        context['done'] = self.get_queryset().filter(status='done').count()
        return context

# # wants追加
# @login_required
# def wantscreate(request):
#     if request.method == 'POST':
#         form = WantsCreateForm(request.POST)
#         if form.is_valid():
#             want = form.save(commit=False)
#             want.user = request.user
#             want.save()
#             return redirect('wants_list', want.user_id)
#     else:
#         form = WantsCreateForm()
#
#     return render(request, 'wants/create.html', {'form': form})

# wants追加
@login_required
def wantscreate(request):

    if request.method == 'POST':
        # 新規wants追加の際には、display_orderは0で設定するためコメント
        # (更新時に、上から順番にカウントアップし、display_orderが0が複数の場合は、want_idでソート)
        # # display_orderのMAX値を取得
        # uwant_disnum = Want.objects.filter(user=request.user).aggregate(Max('display_order'))
        # # Max値が取得できなかった場合、はじめての新規登録なので、1を設定
        # if uwant_disnum['display_order__max'] is None:
        #     maxnum = 1
        # # それ以外の場合、+1を設定
        # else:
        #     maxnum = uwant_disnum['display_order__max'] + 1

        form = WantsCreateForm(request.POST)
        if form.is_valid():
            want = form.save(commit=False)
            want.user = request.user
            # want.display_order = maxnum
            want.save()
            return redirect('wants_list', want.user_id)
    else:
        form = WantsCreateForm()

    return render(request, 'wants/create.html', {'form': form})

# wants更新
def wantsupdate(request, id):
    want = get_object_or_404(Want, pk=id)
    if request.method == 'POST':
        form = WantsCreateForm(request.POST, instance=want)
        if form.is_valid():
            want = form.save(commit=False)
            want.user = request.user
            want.save()
            return redirect('wants_list', want.user_id)
    else:
        form = WantsCreateForm(instance=want)

    return render(request, 'wants/update.html', {'form': form})

# wants達成更新
def wantsachieve(request, id):
    want = get_object_or_404(Want, pk=id)
    if request.method == 'POST':
        form = WantsUpdateForm(request.POST, instance=want)
        if form.is_valid():
            want = form.save(commit=False)
            want.user = request.user
            want.save()
            return redirect('wants_list', want.user_id)
    else:
        form = WantsUpdateForm(instance=want)

    return render(request, 'wants/achieve.html', dict(form=form, want=want, id=id))

# wants削除
def wantsdelete(request, id):
    if request.method == 'POST':
        want = get_object_or_404(Want, pk=id)
        want.delete()
        #messages.info(request, '削除しました')
        return redirect('wants_list', want.user_id)

# like追加
@login_required
def wantslike(request, id):
    want = get_object_or_404(Want, pk=id)

    is_like = Like.objects.filter(user=request.user).filter(want=want).count()
    # unlike
    if is_like > 0:
        liking = Like.objects.get(want__id=id, user=request.user)
        liking.delete()
        want.like_num -= 1
        want.save()
        #messages.warning(request, 'いいねを取り消しました')
        return redirect('wants_list', want.user_id)
    else:
        want.like_num += 1
        want.save()
        like = Like()
        like.user = request.user
        like.want = want
        like.save()
        #messages.success(request, 'いいね！しました')
        return redirect('wants_list', want.user_id)

# tab区切りダウンロード
def download(request, id):
    wants = Want.objects.filter(user=id)
    response = HttpResponse(content_type='text/csv; charset=Shift-JIS')
    filename = urllib.parse.quote((u'MyWantsList.txt').encode("utf8"))
    response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}'.format(filename)
    writer = csv.writer(response, delimiter='\t')
    for want in wants:
        writer.writerow([want.content, want.status, want.target_date, want.publish_set, want.achieve_date, want.achieve_text, want.achieve_url])
    return response

# apihome画面
def apihome(_):
    html = open(
        os.path.join(settings.STATICFILES_DIRS[0], "vue_grid.html"), encoding="utf-8_sig"
    ).read()
    return HttpResponse(html)



# # 変数formを生成する → form.html
# class WantsCreateView(CreateView):
#     model = Want
#     template_name = 'wants/form.html'
#     form_class = WantsForm
#     success_url = reverse_lazy('wants_list')

# class WantsDeleteView(DeleteView):
#     model = Want
#     template_name = 'wants/delete.html'
#     pk_url_kwarg = 'id'
#     success_url = reverse_lazy('wants_list')

# wants更新
# class WantsUpdateView(UpdateView):
#     model = Want
#     template_name = 'wants/update.html'
#     pk_url_kwarg = 'id'
#     form_class = WantsCreateForm
#     success_url = reverse_lazy('wants_list')

# # wants更新
# class WantsAchieveView(UpdateView):
#     model = Want
#     template_name = 'wants/achieve.html'
#     pk_url_kwarg = 'id'
#     form_class = WantsUpdateForm
#     success_url = reverse_lazy('wants_list')


# # wants追加/更新
# @login_required
# def wantsaddedit(request, id=None):
#     if id:
#         want = get_object_or_404(Want, pk=id)
#     else:
#         want = Want()

#     if request.method == 'POST':
#         form = WantsCreateForm(request.POST, instance=want)
#         if form.is_valid():
#             want = form.save(commit=False)
#             want.user = request.user
#             want.save()
#             return redirect('wants_list', want.user_id)
#     else:
#         form = WantsCreateForm(instance=want)

#     return render(request, 'wants/addedit.html', dict(form=form, want=want, id=id))


# # Ranking一覧
# class RankListView(ListView):
#     template_name = 'ranklist.html'
#     paginate_by = 5

#     def get_queryset(self):
#         return Want.objects.filter(like_num__gte=1).order_by('-like_num')      # __gte=1 は、>=1の意味

# #    def get_context_data(self, **kwargs):
#         #context = super().get_context_data(**kwargs)
#     def get_context_data(self):
#         context = super().get_context_data()
#         context['user_list'] = User.objects.all()
#         return context
