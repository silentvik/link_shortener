from math import ceil

from django.conf import settings


def validate_page(view_page, max_page):
    """
        Checks whether this page can be used to display.
        Returns [int or None], [bool]
    """

    try:
        view_page = int(view_page)
    except ValueError:
        return None, False
    if view_page > max_page or view_page < 1:
        return None, False
    return view_page, True


def accurate_string_datetime(date):
    """[Summary]
        Converts datetime to accurate readable string version.
        Args:
            date ([datetime.datetime])
        Returns:
            [str]
    """

    year = str(date.year)
    month = str(date.month)
    day = str(date.day)
    hours = str(date.hour)
    if len(hours) == 1:
        hours = '0' + hours
    minutes = str(date.minute)
    if len(minutes) == 1:
        minutes = '0' + minutes
    return f'{day}-{month}-{year} ({hours}:{minutes})'


def edit_urls_list(urls_list, max_big_url_len):
    """
        Recalculates and edits some data to display the list in the template.
        It operates with model fields, so it cannot be saved.
        If there is a need to save the model later,
        then this function should be rewritten.
    """

    for number, url in enumerate(urls_list, max_big_url_len):
        url.number = number+1
        url.short_url = f"{settings.SITE_URL}{url.short_url}"
        if len(url.real_url) > max_big_url_len:
            url.real_url = f"{url.real_url[:40]}..."
        url.creation_date = accurate_string_datetime(url.creation_date)
    return urls_list


def paginate_urls_list(urls_list, paginate_by, view_page):
    """
        Truncates the list according to the selected page
    """

    return urls_list[
        paginate_by*(view_page-1):paginate_by*view_page
    ]


def get_prev_next_page_url(view_url, view_page, max_page):
    """
        Creates links to the previous and next pages.
        Returns 2 links. (link can be None)
    """

    prev_page_url, next_page_url = None, None
    if view_page < max_page:
        next_page_url = f"{view_url}?page={view_page + 1}"
    if view_page > 1:
        prev_page_url = f"{view_url}?page={view_page - 1}"
    return prev_page_url, next_page_url


def get_max_page(len_urls_list, paginate_by):
    """
        Considers which page is the maximum possible.
    """

    return ceil(len_urls_list / paginate_by)
