from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):
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
        #Dracula has heard about a new online to-do list app. He opens his browser and enters the url to check it out.
        self.browser.get('http://localhost:8000')

        #Unsurprisingly, he notices the page title and header mention to-do lists.
        self.assertIn('To-Do', self.browser.title)
        headerText = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', headerText)

        #He is invited to enter a to-do item straight away.
        inputBox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual('Enter a to-do item', inputBox.get_attribute('placeholder'))

        #He types "Buy fresh virgin blood online" as his first entry.
        inputBox.send_keys('Buy fresh virgin blood online')

        #When he hits enter, the page updates, and now the page lists:
        #"1: Buy fresh virgin blood online".
        inputBox.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('1: Buy fresh virgin blood online')

        #There's still a text box inviting him to enter another item.
        #He enters "Sharpen the teeth".
        inputBox = self.browser.find_element_by_id('id_new_item')
        inputBox.send_keys('Sharpen the teeth')
        inputBox.send_keys(Keys.ENTER)

        #The page updates again and now shows both items on the list.
        self.check_for_row_in_list_table('1: Buy fresh virgin blood online')
        self.check_for_row_in_list_table('2: Sharpen the teeth')

        #Dracula is concerned if the site will remember his to-do list. Then he notices that the site has generated
        #a unique URL for him. There's some text explaining that on the page.
        self.fail('Finish the test!')
        #Dracula opens that link in a new window and sees that all his entries are still in place.

        #Satisfied, he goes back to sleep.

if __name__ == '__main__':
    unittest.main()
