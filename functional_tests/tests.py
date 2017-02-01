from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Dracula has heard about a new online to-do list app. He opens his browser and enters the url to check it out.
        self.browser.get(self.live_server_url)

        # Unsurprisingly, he notices the page title and header mention to-do lists.
        self.assertIn('To-Do', self.browser.title)
        headerText = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', headerText)

        # He is invited to enter a to-do item straight away.
        inputBox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual('Enter a to-do item', inputBox.get_attribute('placeholder'))

        # He types "Buy fresh virgin blood online" as his first entry.
        inputBox.send_keys('Buy fresh virgin blood online')

        # When he hits enter, he is taken to a new URL,
        # and now the page lists "1: Buy fresh virgin blood online"
        # as an item in a to-do list table
        inputBox.send_keys(Keys.ENTER)
        dracula_list_url = self.browser.current_url
        self.assertRegex(dracula_list_url,'/lists/.+')
        self.check_for_row_in_list_table('1: Buy fresh virgin blood online')

        # There's still a text box inviting him to enter another item.
        # He enters "Sharpen the teeth".
        inputBox = self.browser.find_element_by_id('id_new_item')
        inputBox.send_keys('Sharpen the teeth')
        inputBox.send_keys(Keys.ENTER)

        # The page updates again and now shows both items on the list.
        self.check_for_row_in_list_table('1: Buy fresh virgin blood online')
        self.check_for_row_in_list_table('2: Sharpen the teeth')

        # Now a new user, Cinderella comes along to the site

        ## We are using a new browser session to make sure that no information
        ## leaks from previous user's session via cookies etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Cinderella visits the home page, there's no sign of Dracula's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy fresh virgin blood online', page_text)
        self.assertNotIn('Sharpen the teeth', page_text)

        # Cinderella starts a new list by entering text.
        # Good thing she didn't see Dracula's list.
        # As it appears she's been into vampire-hunting lately:
        inputBox = self.browser.find_element_by_id('id_new_item')
        inputBox.send_keys('Buy military-grade wooden stakes')
        inputBox.send_keys(Keys.ENTER)

        # Cinderella gets her own unique URL
        cinderella_list_url = self.browser.current_url
        self.assertRegex(cinderella_list_url, 'lists/.+')
        self.assertNotEqual(cinderella_list_url, dracula_list_url)

        # Again, there's no trace of Dracula's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy fresh virgin blood online', page_text)
        self.assertNotIn('Sharpen the teeth', page_text)
        self.assertIn('1: Buy military-grade wooden stakes', page_text)

        # Satisfied, they both go back to sleep
   # self.fail('Finish the test!')