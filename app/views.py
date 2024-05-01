from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from typing import Any
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView, ListView, DetailView, View
from .models import CustomUser, CommentModel, PlayList
from .forms import (SearchForm,
                        ProfilePhotoForm,
                          CommentForm,
                            UserRegisterForm,
                              PrimePluseForm,
                                GetPrimePluse
                                )
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from .forms import ProfileUpdateForm
from django.contrib.auth.forms import PasswordChangeForm




class PrimePlusFormView(CreateView):
    template_name = 'uplouds/prime_plus_form.html'
    model = GetPrimePluse
    form_class = PrimePluseForm
    success_url = reverse_lazy('home')

    @method_decorator(login_required)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)

class GetPrimePlusMusic(TemplateView):
    template_name = 'pages/prime_plus.html'

    @method_decorator(login_required)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        user = self.request.user
        context['music'] = PlayList.objects.filter(prime_music = True)
        return context

class LoginView(TemplateView):
    template_name = 'authofication/login.html'

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login Is Succses')
            return redirect('home')
        return render(request, self.template_name)

class UserRegisterView(CreateView):
    model = CustomUser
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')
    template_name = 'authofication/sign_up.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_valid(form)


class MusicListView(TemplateView):
    template_name = 'pages/music_list.html'

    @method_decorator(login_required)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        user = self.request.user
        context['musics'] = PlayList.objects.filter(category = user.play_list)
        return context
    

class UserProfileView(TemplateView):
    template_name = 'user/profile.html'
    
    @method_decorator(login_required)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['profile_components'] = CustomUser.objects.filter(username = self.request.user.username)
        return context
    
class LikeView(View):

    @method_decorator(login_required)
    def dispatch(self, request: HttpRequest, pk:int, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request , pk, *args, **kwargs)
    
    def get(self, request, pk:int, *args, **kwargs):
        
        model = PlayList.objects.get(pk=pk)

        if request.user not in model.like.all():
            model.like.add(request.user)
            return JsonResponse({'messages': 'Like Added '})
        else:
            model.like.remove(request.user)
            model.save()
            return JsonResponse({'messages': 'Like removed'})

class AddPlaylistView(View):
    
    @method_decorator(login_required)
    def dispatch(self, request: HttpRequest, pk:int, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, pk, *args, **kwargs)
    
    def get(self, request, pk:int, *args, **kwargs):
        
        user = request.user
        music_model = get_object_or_404(PlayList, pk=pk)

        if music_model not in user.user_play_list.all():
            user.user_play_list.add(music_model)
            return JsonResponse({'message': 'You Added This Music To Your Play List'})
        
        else:
            user.user_play_list.remove(music_model)
            return JsonResponse({'message': 'This Play List Removed'})
    
class MusicDetail(DetailView):
    template_name = 'detail/music.html'
    model = PlayList
    context_object_name = 'music'

    @method_decorator(login_required)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context['music'] = self.object
        return context


class SearchMusics(TemplateView):
    template_name = 'pages/search.html'

    @method_decorator(login_required)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = SearchForm(request.GET or None)
        musics = None
        if form.is_valid():
            search = form.cleaned_data['search']
            musics = PlayList.objects.filter(music_title__icontains = search)
        
        return render(request, self.template_name, {'form':form, 'musics':musics})
    
class CommentView(TemplateView):

    template_name = 'uplouds/commment.html'
    
    @method_decorator(login_required)
    def dispatch(self, request: HttpRequest, pk:int, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, pk, *args, **kwargs)
    
    def get(self, request, pk:int, *args, **kwargs):
            
            content = get_object_or_404(PlayList,pk=pk)
            comments = CommentModel.objects.filter(music=content)
            form = CommentForm()

            return render(request, self.template_name, {'form': form, 'comments': comments, 'commentarion_obj': content})
    
    def post(self, request: HttpRequest, pk:int, *args: Any, **kwargs: Any) -> HttpResponse:

        content = get_object_or_404(PlayList, pk=pk) 
        comment = CommentModel.objects.filter(music = content)

        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment_obj_ = form.save(commit=False)
            new_comment_obj_.user = request.user
            new_comment_obj_.music = content
            new_comment_obj_.save()
            return redirect('comment_uploud_view', pk=pk)
        
        return render(request, self.template_name, {'form':form, 'comments':comment})



class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'uplouds/profile.html'
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('home')

    @method_decorator(login_required)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return self.request.user
    

class PassswordChangeView(View):
    form_class = PasswordChangeForm
    template_name = 'uplouds/password_change.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class(request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password Changed Successfully')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
        return render(request, self.template_name, {'form': form})
    

@login_required
def comment_delete_view(request:HttpRequest, pk:int) -> HttpResponse:

    comment = get_object_or_404(CommentModel, pk=pk)

    if request.user == comment.user:
        comment.delete()
        return JsonResponse({'message': 'Delete Succses '})
    else:
        return JsonResponse({'message': 'Вы не сможете удалить эту комментарию '})
    

class ProfilePhotoView(TemplateView):
    template_name = 'uplouds/profile_photo.html'

    @method_decorator(login_required)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = ProfilePhotoForm()
        return render(request, self.template_name, {'form':form})
    

    def post(self, request, *args, **kwargs):
        
        profile, created = CustomUser.objects.get_or_create(username = request.user)
        if not created and profile.profile_photo:
            messages.success(request, '')
        
        form = ProfilePhotoForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_profile_photo_obj = form.save(commit=False)
            new_profile_photo_obj.user = request.user
            new_profile_photo_obj.save()
            return redirect('home')
        return render(request, self.template_name, {'form':form})
    

class UserDetailView(DetailView):
    template_name = 'detail/user.html'
    model = CustomUser
    context_object_name = 'users'
    
    @method_decorator(login_required)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)
    
@login_required
def get_user_play_list(request, pk):
        user = CustomUser.objects.get(pk=pk)
        play_lists = user.user_play_list.all()
        return render(request, 'detail/play_list.html', {'play_lists': play_lists, 'user':user})


@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('login')


class GetCountryMusics(TemplateView):
    template_name = 'pages/country_musics.html'
    
    @method_decorator(login_required)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        user = self.request.user
        context['music'] = PlayList.objects.filter(music_country = user.country)
        return context
    

class SettingsView(TemplateView):
    template_name = 'pages/settings.html'

    @method_decorator(login_required)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


@login_required
def get_likes(request: HttpRequest, pk) -> HttpResponse:

    like_model = get_object_or_404(PlayList, pk=pk)

    context = like_model.like.all()
    return render(request, 'pages/likes.html', {'likes':context})