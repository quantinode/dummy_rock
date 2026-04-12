from django.test import SimpleTestCase, override_settings


class SeoRoutesTests(SimpleTestCase):
    @override_settings(DEBUG=False)
    def test_robots_txt_lists_public_and_private_rules(self):
        response = self.client.get('/robots.txt', secure=True, HTTP_HOST='example.com')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain; charset=utf-8')

        content = response.content.decode()
        self.assertIn('Allow: /dashboard/onboarding/', content)
        self.assertIn('Allow: /dashboard/ui-showcase/', content)
        self.assertIn('Disallow: /dashboard/', content)
        self.assertIn('Disallow: /api/', content)
        self.assertIn('Sitemap: https://example.com/sitemap.xml', content)

    @override_settings(DEBUG=True)
    def test_robots_txt_blocks_all_crawling_in_debug(self):
        response = self.client.get('/robots.txt', HTTP_HOST='localhost:8000')

        self.assertEqual(response.status_code, 200)

        content = response.content.decode()
        self.assertIn('Disallow: /', content)
        self.assertNotIn('Allow: /dashboard/onboarding/', content)
        self.assertIn('Sitemap: http://localhost:8000/sitemap.xml', content)

    def test_sitemap_lists_public_pages(self):
        response = self.client.get('/sitemap.xml', secure=True, HTTP_HOST='example.com')

        self.assertEqual(response.status_code, 200)
        self.assertIn('xml', response['Content-Type'])

        content = response.content.decode()
        self.assertIn('<loc>https://example.com/</loc>', content)
        self.assertIn('<loc>https://example.com/dashboard/onboarding/</loc>', content)
        self.assertIn('<loc>https://example.com/dashboard/ui-showcase/</loc>', content)
