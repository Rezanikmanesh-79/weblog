from django.contrib.auth import views as auth_views
from django.urls import path, include, reverse_lazy
from accounting.views import SignUpView, ProfileView, custom_user_panel, AuthorPanelView, PostCreateView, PostUpdateView

app_name = "accounting"

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(next_page='accounting:login'), name='logout'),

    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='registration/pass_change_form.html',
            success_url=reverse_lazy('accounting:login')
        ),
        name='password_change'
    ),
    path('', include('django.contrib.auth.urls')),
    path("register/", SignUpView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path('users/', custom_user_panel, name='custom_user_panel'),
    path("authors/", AuthorPanelView.as_view(), name="author_panel"),  
    path("posts/new/", PostCreateView.as_view(), name="post_create"),
    path("posts/<int:pk>/edit/", PostUpdateView.as_view(), name="post_update"),
]
