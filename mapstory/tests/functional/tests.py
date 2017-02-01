"""Functional Tests for Mapstory

Uses selenium and PhantomJS.

Install selenium with:
`pip install selenium`

Install Phantom JS inside the mapstory directory with:
`npm install PhantomJS`

"""
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from django.test import TestCase
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site

from mapstory.tests.AdminClient import AdminClient

class FunctionalTest(TestCase):
    """Generic Functional Test

    - Sets up the browser with phantomJS
    - Tears down the browser when done
    - Knows how to assert search results
    
    Attributes:
        browser (WebDriver): The Selenium headless browser
    """
    def setUp(self):
        self.browser = webdriver.PhantomJS(executable_path=r'/srv/git/mapstory/mapstory/node_modules/phantomjs/lib/phantom/bin/phantomjs')
        self.browser.implicitly_wait(1)
        self.browser.set_window_size(1120,600)

    def tearDown(self):
        self.browser.quit()


class NewVisitorTest(FunctionalTest):
    
    def test_home_has_titles(self):
        # User opens mapstory
        self.browser.get(settings.SITEURL)
        # She sees the title and confirms she is on the correct site
        self.assertIn(u'MapStory', self.browser.title)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn(u'The atlas of change anyone can edit', body )
        # She also sees sponsors
        self.assertIn(u'Our Sponsors', body )


class TestSearchFunctionality(FunctionalTest):

    def check_for_text_in_search_results(self, text):
        """Asserts if text is part of search results

        Args:
            text (string): The text to search for
        """
        table = self.browser.find_element_by_css_selector('div.clearfix.search-results')
        self.assertIsNotNone(table)
        results = table.find_elements_by_tag_name('li')
        print("This many: %d" % len(results) )

        for result in results:
            self.assertIn(text, result.text)

    def test_home_searchbar_redirect(self):
        # User opens mapstory
        self.browser.get(settings.SITEURL)
        # notices the search bar
        searchBar = self.browser.find_element_by_name('q')
        self.assertIsNotNone(searchBar, "Failed to find a search bar")
        # Types someting into search
        searchBar.send_keys('')
        searchBar.send_keys(Keys.ENTER)
        # the page changes to show results if any
        self.assertIn('search', self.browser.current_url, 'search not in URL')

    def test_home_search_story(self):
        # User opens mapstory
        self.browser.get(settings.SITEURL)
        searchBar = self.browser.find_element_by_name('q')
        # Types someting into search
        searchBar.send_keys('')
        searchBar.send_keys(Keys.ENTER)
        # the page changes to show results if any
        self.assertIn('search', self.browser.current_url, 'search not in URL')
        self.check_for_text_in_search_results(u'Lewisandclark')

class TestLayerUpload(FunctionalTest):
    def create_user(self, username, password, **kwargs):
        """
        Convenience method for creating users.
        """
        user, created = get_user_model().objects.get_or_create(username=username, **kwargs)

        if created:
            user.set_password(password)
            user.save()

        return username, password

    def test_upoad_wizard(self):
        testUsername = 'test_uploader'
        testPassword = 'test_uploader'

        # Create our test user
        self.create_user(username=testUsername, password=testPassword, is_superuser=False)

        user_model = get_user_model()
        user = user_model.objects.get(username='test_uploader')
        self.assertIsNotNone(user)

        # Get main page
        site = Site.objects.get_current().domain
        url = "http://%s:%s@%s/" % (testUsername,testPassword,site)
        self.browser.get(url)

        # Clock on login
        # loginIcon = self.browser.find_element_by_css_selector('i.fa.fa-user')
        # self.assertIsNotNone(loginIcon)
        # loginIcon.click()

        # Input Credentials and login
        # wait = WebDriverWait(self.browser, 10)
        # loginModal = wait.until(
            # EC.presence_of_element_located((By.ID,'loginModal'))
        # )
        # loginModal = self.browser.find_element_by_id('loginModal')
        # self.assertIsNotNone(loginModal)
        # usernameInput = self.browser.find_element_by_id('username')
        # passwordInput = self.browser.find_element_by_id('password')
        # self.assertIsNotNone(usernameInput)
        # self.assertIsNotNone(passwordInput)
        # usernameInput.send_keys(str(testUsername))
        # passwordInput.send_keys(str(testPassword))
        # passwordInput.send_keys(Keys.ENTER)

        # Click Create link
        createLink = self.browser.find_element_by_partial_link_text('Create')
        self.assertIsNotNone(createLink)
        createLink.click()

        self.browser.wait(10)

        # Click Import Story Layer
        importStoryLayerLink = self.browser.find_element_by_partial_link_text('Import StoryLayer')
        self.assertIsNotNone(importStoryLayerLink)
        importStoryLayerLink.click()
'''