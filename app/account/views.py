from django.conf import settings

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site

from django.core.mail import send_mail

from django.shortcuts import render, redirect, reverse, get_object_or_404

from django.template.loader import render_to_string

from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.views.generic import TemplateView, View, RedirectView

from account.forms import CreateUserForm, UpdateUserForm
from account.token import user_tokenizer_generate


class RegisterView(View):

    def get(self, request):  # noqa
        form = CreateUserForm()
        context = {'register_form': form, 'title': 'Edenthought | Register'}
        return render(request, 'account/register.html', context)

    def post(self, request): # noqa
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            # Email verification config

            current_site = get_current_site(request)
            user_email = user.email
            subject = 'Activate your Edenthought account.'

            content = render_to_string(
                'account/email_verification.html',
                {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': user_tokenizer_generate.make_token(user)
                }
            )

            send_mail(
                subject=subject,
                message=content,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user_email]
            )

            return redirect('email_verification_sent')

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


class AccountView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    def get(self, request):  # noqa
        form = UpdateUserForm(instance=request.user)
        context = {'account_form': form, 'title': 'Edenthought | Account'}
        return render(request, 'account/account.html', context)

    def post(self, request):  # noqa
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account has been updated successfully!')
        else:
            messages.error(request,
                           f'Invalid data has been provided: {form.errors}')

        return redirect('index')


@login_required(login_url='login')
def delete_account(request):
    user = get_object_or_404(get_user_model(), id=request.user.id)

    logout(request)
    user.delete()
    messages.success(request, 'Account has been deleted successfully!')

    return redirect(reverse('index'))


class EmailVerificationView(RedirectView):

    def dispatch(self, request, *args, **kwargs):
        uidb64 = self.kwargs.get('uidb64')
        token = self.kwargs.get('token')

        return super(EmailVerificationView, self).dispatch(
            request,
            uidb64,
            token,
            *args,
            **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        user_pk = force_str(urlsafe_base64_decode(self.kwargs.get('uidb64')))
        user = get_user_model().objects.get(pk=user_pk)
        token = self.kwargs.get('token')

        if user and user_tokenizer_generate.check_token(user, token):
            user.is_active = True
            user.save()

            return reverse('email_verification_success')

        return reverse('email_verification_failed')


class EmailVerificationSentView(TemplateView):
    template_name = 'account/email_verification_sent.html'


class EmailVerificationSuccessView(TemplateView):
    template_name = 'account/email_verification_success.html'


class EmailVerificationFailedView(TemplateView):
    template_name = 'account/email_verification_failed.html'
