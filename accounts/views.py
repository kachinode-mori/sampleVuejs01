from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth import get_user_model
from .models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from .forms import UserUpdateForm

# def userlist(request):
#     users = User.objects
#     return render(request, 'userlist.html', {'users': users})

# def userlist(request):
#     user_list = User.objects.all()
#     paginator = Paginator(user_list, 5)
#     page = request.GET.get('page')
#     users = paginator.get_page(page)
#     return render(request, 'userlist.html', {'users': users})

class UserListView(ListView):
    model = User
    template_name = 'userlist.html'
    paginate_by = 10
    success_url = reverse_lazy('userlist')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('wants_list', user.id)
    else:
        form = SignUpForm()
    return render(request, 'account/signup.html', {'form': form})


from django.contrib.auth.views import LoginView as AuthLoginView

class LoginView(AuthLoginView):
    template_name='account/login.html'




@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = get_user_model()
    template_name = 'account/my_account.html'
    form_class = UserUpdateForm
    #success_url = reverse_lazy('home')

    #model = User
    #fields = ('username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff')
    #fields = ('email', 'nickname', 'twitter_url', 'intro_text', 'image')
    #label_tag = ('email':'Emailアドレス','nickname': 'ユーザ名(ニックネーム)','twitter_url':'Twitter URL','intro_text':'自己紹介','image':'画像')
    #success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('wants_list', kwargs={'id': self.request.user.id})
