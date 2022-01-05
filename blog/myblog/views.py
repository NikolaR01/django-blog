from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comments
from .forms import PostForm, UpdateForm, AddCommentForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

# Create your views here.

class HomeView(ListView):
	model = Post
	template_name = 'home.html'
	ordering = ['-post_date']

	def get_context_data(self,*args,**kwargs):
		cat_menu = Category.objects.all()
		context = super(HomeView, self).get_context_data(*args,**kwargs)
		context["cat_menu"] = cat_menu
		return context


def CategoryView(request, category):
	category_posts = Post.objects.filter(category=category.replace('-',' '))
	return render(request, 'categories.html', {'category':category.title().replace('-',' '), 'category_posts':category_posts})


class ArticleDetailView(DetailView):
	model = Post
	template_name = 'article_details.html'

	def get_context_data(self,*args,**kwargs):
		cat_menu = Category.objects.all()
		context = super(ArticleDetailView, self).get_context_data(*args,**kwargs)
		details = get_object_or_404(Post, id=self.kwargs['pk'])
		total_likes = details.total_likes()

		liked = False
		if details.likes.filter(id=self.request.user.id).exists():
			liked = True

		context["cat_menu"] = cat_menu
		context["total_likes"] = total_likes
		context['liked'] = liked
		return context


class AddPostView(CreateView):
	model = Post
	form_class = PostForm
	template_name = 'add_post.html'
	#fields = '__all__'


class UpdatePostView(UpdateView):
	model = Post
	template_name = 'update_post.html'
	form_class = UpdateForm


class DeletePostView(DeleteView):
	model = Post
	template_name = 'delete_post.html'
	success_url = reverse_lazy('home')


class AddCategoryView(CreateView):
	model = Category
	template_name = 'add_category.html'
	fields = '__all__'


def CategoryListView(request):
	cat_menu_list = Category.objects.all()
	return render(request, 'category_list.html', {'cat_menu_list':cat_menu_list})


def LikeView(request, pk):
	post = get_object_or_404(Post, id=request.POST.get('post_id'))
	liked = post.likes.filter(id=request.user.id).exists()

	if liked:
		post.likes.remove(request.user)
		liked = False
	else:
		post.likes.add(request.user)
		liked = True

	return HttpResponseRedirect(reverse('article-detail', args = [str(pk)]))


class AddCommentView(CreateView):
	model = Comments
	form_class = AddCommentForm
	template_name = 'add_comment.html'
	success_url = reverse_lazy('home')

	def form_valid(self, form):
		form.instance.post_id = self.kwargs['pk']
		return super().form_valid(form)