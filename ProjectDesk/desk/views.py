from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,TemplateView,View
from .models import Post,Category,Comment
from .filters import PostFilter
from .forms import PostForm,CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
class Postivew(ListView):
    model = Post
    ordering = 'header'
    template_name = 'news.html'
   # context_object_name = 'news'
    #paginate_by = 2

class CommentCreate(LoginRequiredMixin,CreateView):
    model = Comment
    template_name = 'news_detail.html'
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(comit=False)
        comment.commentUser = self.request.user
        comment.commentPost_id = self.kwargs['pk']
        comment.save()
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['news_id'] = self.kwargs['pk']
        return context

class PostDetail(DetailView,CommentCreate):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news'

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])


class PostCreate(CreateView):
    form_class = PostForm
    # модель товаров
    model = Post
    category = Category.name
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.position = self.request.path
        return super().form_valid(form)


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

class PostAuth(LoginRequiredMixin, TemplateView):
    template_name = 'news_edit.html'
class PostDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news')

class AddPost(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_PostCreate','news.change_PostUpdate',
                           'news.view_PostView','news.delete_PostDelete')