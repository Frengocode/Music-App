from django.urls import path
from .views import MusicDetail, MusicListView, UserRegisterView, LoginView, LikeView, AddPlaylistView, UserProfileView, SearchMusics, CommentView, comment_delete_view, ProfilePhotoView, get_user_play_list, UserDetailView, logout_view, UserProfileUpdateView, PassswordChangeView, GetCountryMusics, PrimePlusFormView, GetPrimePlusMusic, SettingsView, get_likes


urlpatterns = [ 
    path('', MusicListView.as_view(), name='home'),
    path('user/account/login/', LoginView.as_view(), name='login'),
    path('user/account/create/', UserRegisterView.as_view(), name='register'),
    path('like/<int:pk>/', LikeView.as_view(), name='like_btn'),
    path('playlist/<int:pk>/', AddPlaylistView.as_view(), name='add_playlist'),
    path('detail/music/<int:pk>/', MusicDetail.as_view(), name='music_detail'),
    path('search/music/', SearchMusics.as_view(), name='search'),
    path('uploud/comment/<int:pk>/', CommentView.as_view(), name='comment_uploud_view'),
    path('comment/delete/<int:pk>/', comment_delete_view, name='comment_delete'),
    path('profile/component/photo/', ProfilePhotoView.as_view(), name='profile_photo'),
    path('user/playlist/list/<int:pk>/', get_user_play_list, name='user_playlist'),
    path('user/detail/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('logout/', logout_view, name='logout'),
    path('user/update/', UserProfileUpdateView.as_view(), name='user_profile_components_update'),
    path('music/country/', GetCountryMusics.as_view(), name='country_musics'),
    path('music/prime/', GetPrimePlusMusic.as_view(), name='get_prime_music'),
    path('user/password/change/', PassswordChangeView.as_view(), name='password_change'),
    path('user/profile/settings/', SettingsView.as_view(), name='settings'),
    path('music/likes/<int:pk>/', get_likes, name='music_like'),


]
