# Copyright 2015 Distilled
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

import logging
import random
import time

logger = logging.getLogger('crawlbin.pages.helpers_directive')


def handle_redirect(directives, previous_parts):
    """Handle the redirect directives:

    - response_301
    - response_302
    - response_303
    - response_307
    - response_308
    - response_400
    - response_401
    - response_403
    - response_404
    - response_410
    - response_418
    - response_500
    - response_503

    In all cases the relevant status code needs returning, along with
    and relevant headers (e.g Location or WWW-Authenticate).

    """

    status_code = 200
    context = {}
    headers = {}

    if 'response_301' in directives:
        status_code = 301
        headers['Location'] = previous_parts

    if 'response_302' in directives:
        status_code = 302
        headers['Location'] = previous_parts

    if 'response_303' in directives:
        status_code = 303
        headers['Location'] = previous_parts

    # TODO: add support for 304.
    # No body content should be returned for a 304.

    if 'response_307' in directives:
        status_code = 307
        headers['Location'] = previous_parts

    if 'response_308' in directives:
        status_code = 308
        headers['Location'] = previous_parts

    if 'response_400' in directives:
        status_code = 400

    if 'response_401' in directives:
        status_code = 401
        headers['WWW-Authenticate'] = 'Basic realm="crawlbin:"'

    if 'response_403' in directives:
        status_code = 403

    if 'response_404' in directives:
        status_code = 404

    if 'response_410' in directives:
        status_code = 410

    if 'response_418' in directives:
        status_code = 418

    if 'response_500' in directives:
        status_code = 500

    if 'response_503' in directives:
        status_code = 503

    return context, headers, status_code


def h1_directive(directives):
    """ Handle the H1 directives:

    - h1_off
    - h1_on
    - h1_multiple

    H1 is assumed to be on, so if off or multiple the h1 context
    variable needs setting accordingly.

    """

    if 'h1_off' in directives:
        return {'h1': 'off'}, {}

    if 'h1_multiple' in directives:
        return {'h1': 'multiple'}, {}

    return {'h1': ''}, {}


def title_tag_directive(directives):
    """ Handle the title tag directive:

    - random_title

    Title is always 'Crawlbin' in the absence of a directive

    """

    titles = ['Crawlbin', 'Crawlbin Alternative']

    choice = random.choice(titles)

    if 'random_title' in directives:
        return {'title': choice}, {}

    return {'title': 'Crawlbin'}, {}


def index_follow_directives(directives):
    """Handle the index / follow directives:

    - meta_follow
    - meta_nofollow
    - meta_index
    - meta_noindex
    - header_follow
    - header_nofollow
    - header_index
    - header_noindex

    Directives prefixed with meta require the meta_follow_index_string
    context variable to be set. Those prefixed with header require the
    X-Robots-Tag header variable to be set.

    """

    context = {}
    context['meta_follow_index_string'] = ""

    context['meta_follow'] = 'meta_follow' in directives
    context['meta_nofollow'] = 'meta_nofollow' in directives
    context['meta_index'] = 'meta_index' in directives
    context['meta_noindex'] = 'meta_noindex' in directives

    if context['meta_follow']:
        context['meta_follow_index_string'] += "follow, "
    if context['meta_nofollow']:
        context['meta_follow_index_string'] += "nofollow, "
    if context['meta_index']:
        context['meta_follow_index_string'] += "index, "
    if context['meta_noindex']:
        context['meta_follow_index_string'] += "noindex, "

    if context['meta_follow_index_string']:
        context['meta_follow_index_string'] = context['meta_follow_index_string'][:-2]

    header_values = []
    if 'header_noindex' in directives:
        header_values.append('noindex')
    if 'header_index' in directives:
        header_values.append('index')
    if 'header_nofollow' in directives:
        header_values.append('nofollow')
    if 'header_follow' in directives:
        header_values.append('follow')

    headers = {}
    if header_values:
        headers = {'X-Robots-Tag': ','.join(header_values)}

    return context, headers


def canonical_directives(directives, base, self, next_block):
    """Add relevant context and headers for the canonical directives.

    - canonical_next_block
    - canonical_random
    - canonical_self
    - canonical_home
    - header_next_block
    - header_random
    - header_self
    - header_home
    - html_next_block
    - html_random
    - html_self
    - html_home

    Directives prefixed with canonical require both the header and
    context variable setting.

    Directives prefixed with header, only need the header variable, and
    those prefixed with html only need the context variable.

    """

    context = {}
    headers = {}

    if 'canonical_next_block' in directives:
        canonical_url = next_block
        context['canonical_next_block'] = canonical_url
        headers['Link'] = '<{url}>; rel="canonical"'.format(url=canonical_url)

    if 'canonical_random' in directives:
        canonical_url = get_random_url(base)
        context['canonical_random'] = canonical_url
        headers['Link'] = '<{url}>; rel="canonical"'.format(url=canonical_url)

    if 'canonical_self' in directives:
        canonical_url = self
        context['canonical_self'] = canonical_url
        headers['Link'] = '<{url}>; rel="canonical"'.format(url=canonical_url)

    if 'canonical_home' in directives:
        canonical_url = base
        context['canonical_home'] = canonical_url
        headers['Link'] = '<{url}>; rel="canonical"'.format(url=canonical_url)

    # header canonicals
    if 'header_canonical_next_block' in directives:
        headers['Link'] = '<{url}>; rel="canonical"'.format(url=next_block)

    if 'header_canonical_random' in directives:
        headers['Link'] = '<{url}>; rel="canonical"'.format(url=get_random_url(base))

    if 'header_canonical_self' in directives:
        headers['Link'] = '<{url}>; rel="canonical"'.format(url=self)

    if 'header_canonical_home' in directives:
        headers['Link'] = '<{url}>; rel="canonical"'.format(url=base)

    # meta tags
    if 'html_canonical_next_block' in directives:
        context['canonical_next_block'] = next_block

    if 'html_canonical_random' in directives:
        context['canonical_random'] = get_random_url(base)

    if 'html_canonical_self' in directives:
        context['canonical_self'] = self

    if 'html_canonical_home' in directives:
        context['canonical_home'] = base

    return context, headers


def vary_directives(directives):
    """Handle the vary directives:

    - vary_accept_encoding
    - vary_user_agent
    - vary_cookie
    - vary_referer

    If any of the above are set they need concatenating and outputting
    in a header variable.

    """

    context = {}
    headers = {}

    varies_by = []

    if 'vary_accept_encoding' in directives:
        varies_by.append('Accept-Encoding')

    if 'vary_user_agent' in directives:
        varies_by.append('User-Agent')

    if 'vary_cookie' in directives:
        varies_by.append('Cookie')

    if 'vary_referer' in directives or 'vary_referrer' in directives:
        varies_by.append('Referer')

    if varies_by:
        headers['Vary'] = ','.join(varies_by)

    return context, headers


def delay_directives(directives):
    """Handle the delay directives:

    - delay_1
    - delay_2
    - delay_3
    - delay_4
    - delay_5

    """

    context = {}
    headers = {}

    if 'delay_1' in directives:
        time.sleep(1)
        context['delay'] = 1

    if 'delay_2' in directives:
        time.sleep(2)
        context['delay'] = 2

    if 'delay_3' in directives:
        time.sleep(3)
        context['delay'] = 3

    if 'delay_4' in directives:
        time.sleep(4)
        context['delay'] = 4

    if 'delay_5' in directives:
        time.sleep(5)
        context['delay'] = 5

    return context, headers


def get_random_url(base):
    """Return a random, valid crawlbin directive, concatenated to the
    given base url.

    """

    fragments = [
        'meta_no_index+meta_nofollow',
        'response_301',
        'meta_noindex',
        'canonical_self+vary_user_agent',
        'canonical_self',
        'vary_user_agent',
        'meta_noindex+canonical_random'
    ]

    choice = random.choice(fragments)

    return base + '/{choice}/'.format(choice=choice)
