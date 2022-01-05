from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic import DetailView, CreateView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import SignUpForm, EditProfileForm, PasswordsChangedForm, EditProfilePageForm, CreateProfilePageForm
from myblog.models import UserProfile

# Create your views here.

class ShowProfilePageView(DetailView):
	model = UserProfile
	template_name = 'registration/user_profile.html'

	def get_context_data(self,*args,**kwargs):
		context = super(ShowProfilePageView, self).get_context_data(*args,**kwargs)
		
		page_user = get_object_or_404(UserProfile, id = self.kwargs['pk'])

		context["page_user"] = page_user
		return context


def password_success(request):
	return render(request, 'registration/password_success.html', {})


class PasswordsChangeView(PasswordChangeView):
	form_class = PasswordsChangedForm
	success_url = reverse_lazy('password_success')


class UserRegisterView(generic.CreateView):
	form_class = SignUpForm
	template_name = 'registration/registration.html'
	success_url = reverse_lazy('login')


class UserEditView(generic.UpdateView):
	form_class = EditProfileForm
	template_name = 'registration/edit_profile.html'
	success_url = reverse_lazy('home')


	def get_object(self):
		return self.request.user


class EditProfilePageView(generic.UpdateView):
	model = UserProfile
	template_name = 'registration/edit_profile_page.html'
	form_class = EditProfilePageForm

	success_url = reverse_lazy('home')


class CreateProfilePageView(CreateView):
	model = UserProfile
	template_name = "registration/create_user_profile_page.html"
	form_class = CreateProfilePageForm

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)