from unittest import TestCase  # Use unittest to avoid creating a database
from pages.helpers_directive import handle_redirect


class RedirectTestCase(TestCase):

    def test_status_code(self):
        """Status Codes are correctly reported"""

        null, null, status_200 = handle_redirect([], '')
        null, null, status_301 = handle_redirect(['response_301'], '')
        null, null, status_302 = handle_redirect(['response_302'], '')
        null, null, status_303 = handle_redirect(['response_303'], '')
        null, null, status_307 = handle_redirect(['response_307'], '')
        null, null, status_308 = handle_redirect(['response_308'], '')
        null, null, status_400 = handle_redirect(['response_400'], '')
        null, null, status_401 = handle_redirect(['response_401'], '')
        null, null, status_403 = handle_redirect(['response_403'], '')
        null, null, status_404 = handle_redirect(['response_404'], '')
        null, null, status_410 = handle_redirect(['response_410'], '')
        null, null, status_418 = handle_redirect(['response_418'], '')
        null, null, status_500 = handle_redirect(['response_500'], '')
        null, null, status_503 = handle_redirect(['response_503'], '')

        self.assertEqual(status_200, 200)
        self.assertEqual(status_301, 301)
        self.assertEqual(status_302, 302)
        self.assertEqual(status_303, 303)
        self.assertEqual(status_307, 307)
        self.assertEqual(status_308, 308)
        self.assertEqual(status_400, 400)
        self.assertEqual(status_401, 401)
        self.assertEqual(status_403, 403)
        self.assertEqual(status_404, 404)
        self.assertEqual(status_410, 410)
        self.assertEqual(status_418, 418)
        self.assertEqual(status_500, 500)
        self.assertEqual(status_503, 503)

    def test_headers(self):
        """Headers are correctly set"""

        null, headers_200, null = handle_redirect([], '')
        null, headers_301, null = handle_redirect(['response_301'], 'testcase')
        null, headers_302, null = handle_redirect(['response_302'], 'testcase')
        null, headers_303, null = handle_redirect(['response_303'], 'testcase')
        null, headers_307, null = handle_redirect(['response_307'], 'testcase')
        null, headers_308, null = handle_redirect(['response_308'], 'testcase')
        null, headers_400, null = handle_redirect(['response_400'], 'testcase')
        null, headers_401, null = handle_redirect(['response_401'], 'testcase')
        null, headers_403, null = handle_redirect(['response_403'], 'testcase')
        null, headers_404, null = handle_redirect(['response_404'], 'testcase')
        null, headers_410, null = handle_redirect(['response_410'], 'testcase')
        null, headers_418, null = handle_redirect(['response_418'], 'testcase')
        null, headers_500, null = handle_redirect(['response_500'], 'testcase')
        null, headers_503, null = handle_redirect(['response_503'], 'testcase')

        self.assertEqual(headers_200, {})
        self.assertEqual(headers_301, {'Location': 'testcase'})
        self.assertEqual(headers_302, {'Location': 'testcase'})
        self.assertEqual(headers_303, {'Location': 'testcase'})
        self.assertEqual(headers_307, {'Location': 'testcase'})
        self.assertEqual(headers_308, {'Location': 'testcase'})
        self.assertEqual(headers_400, {})
        self.assertEqual(headers_401, {
            'WWW-Authenticate': 'Basic realm="crawlbin:"'
        })
        self.assertEqual(headers_403, {})
        self.assertEqual(headers_404, {})
        self.assertEqual(headers_410, {})
        self.assertEqual(headers_418, {})
        self.assertEqual(headers_500, {})
        self.assertEqual(headers_503, {})

    def test_context(self):
        """Context is correctly set"""

        context_200, null, null = handle_redirect([], '')
        context_301, null, null = handle_redirect(['response_301'], 'testcase')
        context_302, null, null = handle_redirect(['response_302'], 'testcase')
        context_303, null, null = handle_redirect(['response_303'], 'testcase')
        context_307, null, null = handle_redirect(['response_307'], 'testcase')
        context_308, null, null = handle_redirect(['response_308'], 'testcase')
        context_400, null, null = handle_redirect(['response_400'], 'testcase')
        context_401, null, null = handle_redirect(['response_401'], 'testcase')
        context_403, null, null = handle_redirect(['response_403'], 'testcase')
        context_404, null, null = handle_redirect(['response_404'], 'testcase')
        context_410, null, null = handle_redirect(['response_410'], 'testcase')
        context_418, null, null = handle_redirect(['response_418'], 'testcase')
        context_500, null, null = handle_redirect(['response_500'], 'testcase')
        context_503, null, null = handle_redirect(['response_503'], 'testcase')

        self.assertEqual(context_200, {})
        self.assertEqual(context_301, {})
        self.assertEqual(context_302, {})
        self.assertEqual(context_303, {})
        self.assertEqual(context_307, {})
        self.assertEqual(context_308, {})
        self.assertEqual(context_400, {})
        self.assertEqual(context_401, {})
        self.assertEqual(context_403, {})
        self.assertEqual(context_404, {})
        self.assertEqual(context_410, {})
        self.assertEqual(context_418, {})
        self.assertEqual(context_500, {})
        self.assertEqual(context_503, {})
