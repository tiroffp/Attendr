from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def check_for_row_in_roll_table(self, row_text):
        table = self.browser.find_element_by_id('id_roll_table')
        rows = table.find_elements_by_tag_name('tr')
        rows = [row.find_elements_by_tag_name('td') for row in rows]
        rows = [item for sublist in rows for item in sublist]  # flatten list
        rows = [row.find_elements_by_tag_name('p') for row in rows]
        rows = [item for sublist in rows for item in sublist]
        self.assertIn(row_text, [row.text for row in rows])

    def get_attendee_input_box(self):
        return self.browser.find_element_by_id('id_name')
