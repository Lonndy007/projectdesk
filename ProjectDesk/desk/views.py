from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,TemplateView,View
from .models import Post,Category
from .filters import PostFilter
from django.forms import PostForm
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

class PostDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news'

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

    def comment(self):

class PostCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
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