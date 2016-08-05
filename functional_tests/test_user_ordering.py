from functional_tests.base import FunctionalTest
from selenium import webdriver


class UserOrderingTest(FunctionalTest):
    def check_table_row_ordering(self, expected_order):
        """
            Asserts that the table contains the same rows as defined in
            the list 'expected_order' by order and content
        """
        table = self.browser.find_element_by_id('id_roll_table')
        rows = table.find_elements_by_tag_name('tr')
        ziplist = zip(rows, expected_order)
        for actual, expected in ziplist:
            self.assertIn(actual.text, expected)

    def test_can_reorder_roll(self):
        # John is making a roll, but wants to order it by who he likes best
        # John loads up the site
        self.browser.get(self.live_server_url)

        # John starts a new roll by adding someone to an event
        self.get_attendee_input_box().send_keys('Daveed Diggs\n')

        # John adds two new people
        self.get_attendee_input_box().send_keys('Alexander Hamilton\n')
        self.get_attendee_input_box().send_keys('Tony Soprano\n')

        # John sees that the three attendees currently have order numbers
        # created based on their creation order
        expected_order = ['Daveed Diggs', 'Alexander Hamilton', 'Tony Soprano']
        self.check_table_row_ordering(expected_order)

        # John likes Tony, so he sets him to be first in the ranking
        self.browser.find_element_by_id('edit_attendee_3').click()
        orderbox = self.browser.find_element_by_id('id_order')
        orderbox.clear()
        orderbox.send_keys('1\n')
        expected_order = ['Tony Soprano', 'Daveed Diggs', 'Alexander Hamilton']
        self.check_table_row_ordering(expected_order)

        # John hates Daveed, so he sends him to the end of the list
        self.browser.find_element_by_id('edit_attendee_2').click()
        orderbox = self.browser.find_element_by_id('id_order')
        orderbox.clear()
        orderbox.send_keys('\n')
        expected_order = ['Tony Soprano', 'Alexander Hamilton', 'Daveed Diggs']
        self.check_table_row_ordering(expected_order)

        # John logs out for now
        john_rolls_url = self.browser.current_url
        self.browser.refresh()
        self.browser.quit()

        # When he comes back, he sees that the order remained
        self.browser = webdriver.Firefox()
        self.browser.get(john_rolls_url)
        expected_order = ['Tony Soprano', 'Alexander Hamilton', 'Daveed Diggs']
        self.check_table_row_ordering(expected_order)