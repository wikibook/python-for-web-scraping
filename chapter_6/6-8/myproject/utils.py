import logging

import lxml.html
import readability


logging.getLogger('readability.readability').setLevel(logging.WARNING)


def get_content(html):
    document = readability.Document(html)
    content_html = document.summary()
    content_text = lxml.html.fromstring(content_html).text_content().strip()
    short_title = document.short_title()

    return short_title, content_text
