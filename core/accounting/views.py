# accounting/views.py
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden
from accounting.models import User
from blog.models import Post
from blog.forms import PostForm
from accounting.forms import RegistrationForm

# --------------------------
# Sign up
# --------------------------
class SignUpView(FormView):
    template_name = "registration/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("accounting:login")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

# --------------------------
# Profile
# --------------------------
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

# --------------------------
# Admin panel
# --------------------------
@staff_member_required
def custom_user_panel(request):
    users = User.objects.all()
    return render(request, "admin/user_panel.html", {"users": users})

# --------------------------
# Mixin for author or admin access
# --------------------------
class AuthorOrAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        # Allow access for authors or admin users
        return user.role in [User.Role.AUTHOR, User.Role.ADMIN] or user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('accounting:login')
        return HttpResponseForbidden("You are not allowed to view this page.")

# --------------------------
# Author panel
# --------------------------
class AuthorPanelView(LoginRequiredMixin, AuthorOrAdminRequiredMixin, ListView):
    model = Post
    template_name = "author/author_panel.html"
    context_object_name = "posts"

    def get_queryset(self):
        user = self.request.user
        # Admin sees all posts, author only their own
        if user.role == User.Role.ADMIN or user.is_superuser:
            return Post.objects.all()
        return Post.objects.filter(author=user)

# --------------------------
# Create post
# --------------------------
class PostCreateView(LoginRequiredMixin, AuthorOrAdminRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "author/post_form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Only admin can see/change the status
        if not (self.request.user.role == User.Role.ADMIN or self.request.user.is_superuser):
            form.fields.pop('status', None)
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        # For authors, status is default
        if not (self.request.user.role == User.Role.ADMIN or self.request.user.is_superuser):
            form.instance.status = Post.Status.DRAFT
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounting:author_panel')

# --------------------------
# Update post
# --------------------------
class PostUpdateView(LoginRequiredMixin, AuthorOrAdminRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "author/post_form.html"

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.ADMIN or user.is_superuser:
            return Post.objects.all()
        return Post.objects.filter(author=user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not (self.request.user.role == User.Role.ADMIN or self.request.user.is_superuser):
            form.fields.pop('status', None)
        return form

    def form_valid(self, form):
        if not (self.request.user.role == User.Role.ADMIN or self.request.user.is_superuser):
            # Keep the current post status for authors
            form.instance.status = self.get_object().status
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounting:author_panel')
