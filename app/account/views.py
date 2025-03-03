from django.views.generic import TemplateView, View

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect, reverse, get_object_or_404

from account.forms import CreateUserForm


class RegisterView(View):

    def get(self, request):  # noqa
        form = CreateUserForm()
        context = {'register_form': form, 'title': 'Edenthought | Register'}
        return render(request, 'account/register.html', context)

    def post(self, request): # noqa
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account has been created successfully!')
            return redirect('login')

        messages.error(request, f'Invalid data has been provided: {form.errors}')
        return redirect(request.META.get('HTTP_REFERER', reverse('register')))


class LoginView(View):
    def get(self, request):  # noqa
        form = AuthenticationForm()
        context = {'login_form': form, 'title': 'Edenthought | Login'}
        return render(request, 'account/login.html', context)

    def post(self, request):  # noqa
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')  # Username / Email
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                if user.is_writer:  # noqa
                    return redirect(reverse('writer:dashboard',
                                            kwargs={'writer_id': user.id}))

                return redirect(reverse('client:dashboard'))

        messages.error(request, 'Invalid username or password!')
        return redirect(request.META.get('HTTP_REFERER', reverse('login')))


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out!')
    return redirect('index')
