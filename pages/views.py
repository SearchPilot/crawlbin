# Copyright 2015 Distilled
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

import logging

from django.shortcuts import render

from helpers_directive import canonical_directives
from helpers_directive import delay_directives
from helpers_directive import h1_directive
from helpers_directive import handle_redirect
from helpers_directive import index_follow_directives
from helpers_directive import vary_directives
from helpers_url import get_directives_from_random_matching_block

logger = logging.getLogger('crawlbin.pages.views')


def index(request):
    """ Render the crawlbin index page.

    """

    context = {}
    return render(request, 'pages/index.html', context)


def robots(request):
    """ Render the crawlbin robots.txt.

    """

    context = {}
    response = render(request, "pages/robots.txt", context)
    response['Content-Type'] = "text/plain; charset=UTF-8"
    return response


def handle(request, url):
    """ Render all crawlbin urls.

    """

    url_parts = url.split("/")
    last_part = url_parts[-1]
    previous_parts = url_parts[:-1]
    directives = get_directives_from_random_matching_block(
        last_part,
        user_agent=request.META['HTTP_USER_AGENT']
    )

    base_url = '{scheme}://{host}'.format(
        scheme=request.scheme,
        host=request.get_host()
    )
    current_url = '{base}{path}'.format(
        base=base_url,
        path=request.path
    )

    # Avoid ending up with 2 trailing slashes for empty paths
    path = '/'.join(pp for pp in previous_parts)
    if path:
        previous_parts_url = '{base}/{path}/'.format(base=base_url, path=path)
    else:
        previous_parts_url = '{base}/'.format(base=base_url)

    context = {
        'url': url,
        'previous_parts_url': previous_parts_url,
        'directives': directives
    }
    headers = {}

    # handle h1 directives
    h1_context, h1_headers = h1_directive(directives)
    context.update(h1_context)
    headers.update(h1_headers)

    # handle index_follow directives
    index_follow_context, index_follow_headers = index_follow_directives(
        directives
    )
    context.update(index_follow_context)
    headers.update(index_follow_headers)

    # handle canonical directives
    canonical_context, canonical_headers = canonical_directives(
        directives,
        base_url,
        current_url,
        previous_parts_url
    )
    context.update(canonical_context)
    headers.update(canonical_headers)

    # handle vary directives
    vary_context, vary_headers = vary_directives(directives)
    context.update(vary_context)
    headers.update(vary_headers)

    # handle delay directives
    delay_context, delay_headers = delay_directives(directives)
    context.update(delay_context)
    headers.update(delay_headers)

    # for debug/output purposes
    context.update({'headers': headers})

    response_context, response_headers, status_code = handle_redirect(
        directives,
        previous_parts_url
    )
    context.update(response_context)
    headers.update(response_headers)

    response = render(
        request,
        "pages/template.html",
        context,
        status=status_code
    )

    for header_key, header_val in headers.iteritems():
        response[header_key] = header_val

    return response
