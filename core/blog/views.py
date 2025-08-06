from django.views.generic import ListView, DetailView
from blog.models import Post
from blog.forms import CommentForm

class ListOfPostView(ListView):
    model = Post
    template_name = "blog/post-list.html"
    context_object_name = 'posts'

class PostDetail(DetailView):
    model = Post
    template_name = "blog/post-detail.html"
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(is_approved=True)
        if 'form' not in context:
            context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object 
            comment.save()
            return self.get(request, *args, **kwargs)
        context = self.get_context_data()
        context['form'] = form 
        return self.render_to_response(context)
