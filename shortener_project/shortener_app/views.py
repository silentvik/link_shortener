from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic.edit import CreateView

from shortener_app.forms import UrlForm, UserLoginForm, UserRegistrationForm
from shortener_app.models import Urls
from shortener_app.services import model_services, view_services


class LoginView(View):
    def get(self, request):
        form = UserLoginForm()
        response = render(
                    request,
                    'shortener_app/login.html',
                    context={
                        'form': form,
                    }
                )
        return response

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                msg = 'incorrent username or password'
                form.add_error('password', msg)

        response = render(
                    request,
                    'shortener_app/login.html',
                    context={
                        'form': form,
                    }
                )
        return response


class CreateUserView(View):

    def get(self, request):
        response = render(request, 'shortener_app/registration.html')
        return response

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            user = authenticate(
                username=new_user.username,
                password=request.POST['password']
            )
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            response = render(
                    request,
                    'shortener_app/registration.html',
                    context={'form': form}
                )
            return response


class ShortUrlView(CreateView):
    def get(self, request):
        form = UrlForm()
        current_user = self.request.user
        current_username = None
        if not current_user.is_anonymous:
            current_username = current_user.username

        response = render(
                    request,
                    'shortener_app/urlview.html',
                    context={
                        'form': form,
                        'current_username': current_username,
                    }
                )
        return response

    def post(self, request):
        form = UrlForm(request.POST)
        current_user = self.request.user
        current_username = None
        if not current_user.is_anonymous:
            current_username = current_user.username
        short_url = None
        if form.is_valid():
            short_url = model_services.create_short_url(
                form.cleaned_data['real_url'],
                current_user
            ).short_url
            short_url = f'{settings.SITE_URL}{short_url}'
        response = render(
            request,
            'shortener_app/urlview.html',
            context={
                'form': form,
                'current_username': current_username,
                'short_url': short_url,
            }
        )
        return response


def urls_list_view(request):
    """
        View urls list of a specific user.
        List can be paginated.
        Generates links to the next and previous page.
    """

    # Some defaults:
    paginate_by = 10
    view_url = reverse('urlslist')
    urls_list = None
    view_page = None
    next_page_url = None
    prev_page_url = None
    max_big_url_len = 40

    if request.user.is_authenticated:
        urls_list = list(
            Urls.objects.filter(
                created_by_id=request.user.id
            ).order_by('creation_date')
        )
        len_urls_list = len(urls_list)
        view_page = request.GET.get('page', 1)
        max_page = view_services.get_max_page(len_urls_list, paginate_by)
        view_page, page_is_valid = view_services.validate_page(
            view_page,
            max_page
        )
        if page_is_valid:
            urls_list = view_services.edit_urls_list(
                urls_list,
                max_big_url_len
            )
            urls_list = view_services.paginate_urls_list(
                urls_list,
                paginate_by,
                view_page
            )
            prev_page_url, next_page_url = (
                view_services.get_prev_next_page_url(
                    view_url,
                    view_page,
                    max_page
                )
            )

        elif len_urls_list == 0:
            view_page = 0

    response = render(
        request,
        'shortener_app/urlslist.html',
        context={
            'urls_list': urls_list,
            'view_page': view_page,
            'next_page_url': next_page_url,
            'prev_page_url': prev_page_url,
            'user': request.user
        }
    )
    return response


def redirect_view(request, short_url):
    url = get_object_or_404(Urls, short_url=short_url)
    url.used_count += 1
    url.save()
    return HttpResponseRedirect(url.real_url)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect(reverse('login'))


def home_redirect(request):
    return HttpResponseRedirect(reverse('home'))
