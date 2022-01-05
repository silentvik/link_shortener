from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic.edit import CreateView

from shortener_app.forms import UrlForm, UserLoginForm, UserRegistrationForm
from shortener_app.models import MyUrl
from shortener_app.services import view_services


class CreateUserView(View):
    """
        Available methods - GET, POST.
        The main task is to display the user registration page.
    """

    def get(self, request):
        """
            Returns a rendered page (with registration fields).
        """

        response = render(request, 'shortener_app/registration.html')
        return response

    def post(self, request):
        """
            Creates a new account if the data
            in the form was entered correctly.
            Automatically authenticates the user
            when creating a new account
            (and redirects to the home page).
        """

        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            view_services.process_user_registration(request, form)
            return HttpResponseRedirect(reverse('home'))

        response = render(
                request,
                'shortener_app/registration.html',
                context={'form': form}
            )
        return response


class LoginView(View):
    """
        Available methods - GET, POST.
        The main task is to display the user login page.
    """

    def get(self, request):
        """
            Returns the rendered page (with login fields).
        """

        response = render(
            request,
            'shortener_app/login.html'
        )
        return response

    def post(self, request):
        """
            Authenticates the user if the form was filled
            out correctly and redirects to the home page,
            otherwise returns the page with the login form.
        """

        form = UserLoginForm(request.POST)
        if form.is_valid():
            login_success = view_services.user_auth_login(request, form)
            if login_success:
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


class ShortUrlView(CreateView):
    """
        Home page, where the user can
        choose what to do, including shorten the link.
    """

    def get(self, request):
        current_user = self.request.user
        current_username = view_services.get_username_or_none(current_user)
        response = render(
            request,
            'shortener_app/urlview.html',
            context={
                'current_username': current_username,
            }
        )
        return response

    def post(self, request):
        form = UrlForm(request.POST)
        current_user = self.request.user
        current_username = view_services.get_username_or_none(current_user)
        short_url = None
        if form.is_valid():
            short_url = view_services.get_short_url(
                form.cleaned_data['real_url'],
                current_user
            )

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
            MyUrl.objects.filter(
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
            print(f'urls_list = {urls_list}')
        elif len_urls_list == 0:
            # This value is needed in template.
            # If user is authenticated but hasn't short
            # urls - we dont want to show a table of urls,
            # but want to show some message.
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
    """
        Redirects to the original link.
    """

    url = get_object_or_404(MyUrl, short_url=short_url)
    url.used_count += 1
    url.save()
    return HttpResponseRedirect(url.real_url)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect(reverse('login'))


def home_redirect(request):
    return HttpResponseRedirect(reverse('home'))
