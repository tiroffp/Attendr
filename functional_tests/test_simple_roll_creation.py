from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from functional_tests.base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_roll_and_retrieve_it_later(self):
        # Mary has been losing track of all the people she needs to keep track of
        # and sees an ad for an attendance site. She goes to check out the
        # homepage
        self.browser.get(self.live_server_url)

        # She notices that the title mentions creating roll, so she
        # knows shes on the right site
        self.assertIn('Attendr', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn("Create", header_text)
        self.assertIn("Roll", header_text)

        # She is invited to make a roll right away
        inputbox = self.get_attendee_input_box()
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter an attendee')

        # She types "Mary Man"
        inputbox.send_keys('Mary Man')

        # When she hits enter, the page updates, and the page now
        # lists "1: Mary Man" as an attendee on a roll
        inputbox.send_keys(Keys.ENTER)
        mary_roll_url = self.browser.current_url
        self.assertRegex(mary_roll_url, '/create_roll/.+')
        self.check_for_row_in_roll_table('Mary Man')

        # There is still a textbox inviting here to enter another attendee
        # she enters "David Dad"
        inputbox = self.get_attendee_input_box()
        inputbox.send_keys('David Dad')
        inputbox.send_keys(Keys.ENTER)

        # the page updates again, showing both her inputs
        self.check_for_row_in_roll_table('Mary Man')
        self.check_for_row_in_roll_table('David Dad')

        # now a new user, Frank, comes along to the site

        # # We use a new browser session to make sure that no information
        # # of Mary's is coming through cookies, etc
        self.browser.refresh()
        self.browser.quit()
        WebDriverWait(self.browser, 10)
        self.browser = webdriver.Firefox()

        # Frank visits the home page. There is no sign of Mary's roll
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Mary Man', page_text)
        self.assertNotIn('David Dad', page_text)

        # Frank starts a new roll by entering a new attendee
        inputbox = self.get_attendee_input_box()
        inputbox.send_keys('Frank Furt')
        inputbox.send_keys(Keys.ENTER)

        # Frank gets his own unique URL
        frank_rolls_url = self.browser.current_url
        self.assertRegex(frank_rolls_url, '/create_roll/.+')
        self.assertNotEqual(frank_rolls_url, mary_roll_url)

        # Again, there is no trace of Mary's roll
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Mary Man', page_text)
        self.assertIn('Frank Furt', page_text)

        # Satisified, he leaves the page
