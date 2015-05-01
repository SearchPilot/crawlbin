# Copyright 2015 Distilled
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

"""
It is helpful to understand the following definitions when reading this
code.

Directives:

Each possible 'command', such as 'vary_cookie' or 'response_404' is
called a 'directive'.

Blocks:

A 'block' is any set of directives wrapped in [].

There are two blocks here, with three directives in total:
http://crawlbin.com/[meta_noindex+vary_cookie][response_404]/

One of the two blocks above would be selected at random. Directives in a
block are joined with +.

Nested blocks are possible, which introduces randomness within a block.

For example, here there are two outer blocks (one has a nested block):
http://crawlbin.com/[meta_index+[vary_cookie,vary_referer]][response_404]/

"""

import logging
import re
import random
import user_agents

logger = logging.getLogger('crawlbin.pages.helpers_url')


def parse_brackets(url_path):
    """Verify the brackets in the URL match & are not too deeply nested.

    If there are no outer brackets then add them to make matching
    against them easier and more consistent later on.

    If there are nested brackets then we swap them for parentheses here
    so as to make matching pairs easier later on.

    url_path is should not contain the domain name or forward slashes.

    """

    parsed_url = ""
    bracket_depth = 0

    # If we aren't wrapped in [brackets] then add them now.
    if not re.search("^\[.*\]$", url_path):
        url_path = "["+url_path+"]"

    for char in url_path:

        if char == "]":
            if bracket_depth == 0:
                raise SyntaxError("Encountered an unexpected closing bracket.")
            elif bracket_depth == 1:
                parsed_url += char
            elif bracket_depth == 2:
                parsed_url += ")"

            bracket_depth -= 1

        elif char == "[":
            if bracket_depth == 0:
                parsed_url += char
            elif bracket_depth >= 1:
                parsed_url += "("

            bracket_depth += 1

        else:
            parsed_url += char

        if bracket_depth > 2:
            raise SyntaxError("Too many nested levels of brackets.")

    return parsed_url


def random_nested_directives(block):
    """If the specified block contains any comma separated nested
    directives, then randomly elimante all but one of those directives.

    The block being passed in should be a single block without the outer
    set of brackets. For example:

    meta_index+(vary_cookie,vary_referer)

    which would be one of the blocks in this URL:

    http://crawlbin.com/[meta_index+[vary_cookie,vary_referer]][response_404]/

    """

    directives = set()

    plain_blocks = set(re.split('\([^\)]*\)', block))
    random_blocks = set(re.findall('\([^\)]*\)', block))

    for plain_block in plain_blocks:
        block_directives = plain_block.split("+")
        directives.update(block_directives)

    for random_block in random_blocks:

        block_directives = random_block[1:-1].split(",")

        if len(block_directives) < 1 and "+" in random_blocks:
            block_directives = random_blocks[1:-1].split("+")

        directives.add(random.choice(block_directives))

    return "+".join(filter(None, directives))


def collate_blocks_by_user_agent(url_path):
    """Produce a dictionary keyed on user agent categories, with each
    entry containing a list of all the blocks that are specific to that
    category. Anything without a specified category goes into 'all'.

    Also in this function we take the opportunity to randomly select
    directives whenever there are multiple options within a nested block.

    url_path is should not contain the domain name or forward slashes.

    """
    parsed_url = parse_brackets(url_path)

    found_blocks = re.findall('\[[^\]]*\]', parsed_url)

    trimmed_blocks_for_ua_filter = dict()
    trimmed_blocks_for_ua_filter["none"] = set()

    user_agents = ["all",
                   "bot",
                   "googlebot",
                   "desktop",
                   "mobile",
                   "tablet",
                   "ie",
                   "ff"
                   ]

    for ua in user_agents:
        trimmed_blocks_for_ua_filter[ua] = set()

    for this_block in found_blocks:
        this_block_trimmed = this_block[1:-1]

        user_agent_directives = re.findall('^[a-z 0-9]+:', this_block_trimmed)

        if len(user_agent_directives) > 0:

            ua_filter = user_agent_directives[0][:-1]

            if ua_filter not in trimmed_blocks_for_ua_filter:
                trimmed_blocks_for_ua_filter[ua_filter] = set()

            this_block_trimmed_ua_removed = this_block_trimmed[len(user_agent_directives[0]):]
            rand_nested_directives = random_nested_directives(this_block_trimmed_ua_removed)
            trimmed_blocks_for_ua_filter[ua_filter].add(rand_nested_directives)

        else:
            trimmed_blocks_for_ua_filter["none"].add(random_nested_directives(this_block_trimmed))

    return trimmed_blocks_for_ua_filter


def get_directives_from_random_matching_block(url, user_agent):
    """Select a random block from all those that could apply to this user
    agent. Nested blocks with multiple choices to randomise between will
    be resolved in the call to collate_blocks_by_user_agent().

    url here is the full url with leading and trailing slashes.

    We return a list of the directives within the block we selected.

    """

    matched_blocks = set()
    all_blocks = collate_blocks_by_user_agent(url)

    ua = user_agents.parse(user_agent)

    matched_something = False
    matched_blocks.update(all_blocks['all'])

    if ua.is_bot and len(all_blocks['bot']) > 0:
        matched_blocks.update(all_blocks['bot'])
        matched_something = True

    if ua.browser.family == "Googlebot" and len(all_blocks['googlebot']) > 0:
        matched_blocks.update(all_blocks['googlebot'])
        matched_something = True

    if ua.browser.family == "IE" and len(all_blocks['ie']) > 0:
        matched_blocks.update(all_blocks['ie'])
        matched_something = True

    if ua.browser.family == "Firefox" and len(all_blocks['ff']) > 0:
        matched_blocks.update(all_blocks['ff'])
        matched_something = True

    if ua.is_mobile and len(all_blocks['mobile']) > 0:
        matched_blocks.update(all_blocks['mobile'])
        matched_something = True

    if ua.is_pc and len(all_blocks['desktop']) > 0:
        matched_blocks.update(all_blocks['desktop'])
        matched_something = True

    if ua.is_tablet and len(all_blocks['tablet']) > 0:
        matched_blocks.update(all_blocks['tablet'])
        matched_something = True

    if not matched_something:
        matched_blocks.update(all_blocks['none'])

    if len(matched_blocks) > 0:
        chosen_block = random.choice(list(matched_blocks))

        return chosen_block.split("+")

    return []
