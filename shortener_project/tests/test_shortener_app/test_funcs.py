from datetime import datetime

import pytest
from django.contrib.auth.models import AnonymousUser
from shortener_app.models import MyUrl
from shortener_app.services import model_services, view_services


@pytest.mark.django_db
class TestModelServices:
    """
        Testing all funcs in model_services
    """

    def test_create_url(self, create_user):
        real_url = 'https://docs.djangoproject.com/'

        user = create_user()
        url_inst = model_services.create_url(real_url, user)
        assert url_inst
        assert len(url_inst.short_url) == 6
        assert url_inst.created_by_id != 0

        user = AnonymousUser
        url_inst = model_services.create_url(real_url, user)
        assert url_inst
        assert len(url_inst.short_url) == 6
        assert url_inst.created_by_id == 0

    def test_generate_short_url(self):
        for length in range(1, 200):
            res = model_services.generate_short_url(length)
            assert len(res) == length

    def test_make_new_short_url(self):
        for _ in range(10000):
            res = model_services.make_new_short_url()
            assert res
            assert len(res) == 6
        urls_list = list(MyUrl.objects.all())
        short_urls = []
        for url in urls_list:
            short_urls.append(url.short_url)
        assert len(short_urls) == len(set(short_urls))


@pytest.mark.django_db
class TestViewServices:
    """
        Testing some funcs in view_services
    """

    def test_validate_page(self):
        """
            Page input is a string. Max page is a [int] by default.
        """
        pages_tuples = [
            ('1', 2),
            ('15', 150),
            ('-200', 0),
            ('300', 299),
            ('100', 100),
            ('asdf', 5)
        ]
        results_tuples = [
            (1, True),
            (15, True),
            (None, False),
            (None, False),
            (100, True),
            (None, False)
        ]
        for i, page_tuple in enumerate(pages_tuples):
            res = view_services.validate_page(*page_tuple)
            assert res == results_tuples[i]

    def test_accurate_string_datetime(self):
        for i in range(10):
            time_now = datetime.now()
            readable_time = view_services.accurate_string_datetime(time_now)
            assert type(readable_time) == str
            in_parentheses = readable_time[-7:]
            # here we check a len of output in parentheses
            # last 7 symbols in readable_time must be '(hh:mm)'
            assert in_parentheses[0] == '('
            assert in_parentheses[-1] == ')'
