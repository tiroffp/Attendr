from functional_tests.base import FunctionalTest
from selenium import webdriver


class EditingRollTest(FunctionalTest):
    def check_table_row_ordering(self, expected_order):
        """
            Asserts that the table contains the same rows as defined in
            the list 'expected_order' by order and content
        """
        table = self.browser.find_element_by_id('id_roll_table')
        rows = table.find_elements_by_tag_name('tr')
        ziplist = zip(rows, expected_order)
        for actual, expected in ziplist:
            self.assertIn(expected, actual.text)

    def test_can_edit_attendees_already_on_roll(self):
        # John is making a roll, but wants to order it by who he likes best
        # John loads up the site
        self.browser.get(self.live_server_url)

        # John starts a new roll by adding someone to an event
        self.get_attendee_input_box().send_keys('Daveed Diggs\n')

        # John adds two new people
        self.get_attendee_input_box().send_keys('Alexander Hamilton\n')
        self.get_attendee_input_box().send_keys('Tony Tiger\n')

        # He notes that the list sorts the members alphabetically, as they currently have no order
        self.check_table_row_ordering(['Alexander Hamilton', 'Daveed Diggs', 'Tony Tiger'])

        # John remembers that Tony Soprano, not Tony Tiger agreed to come to his
        # meeting. He decides its easier to edit the Tiger's entry, rather than
        # create a new one
        self.browser.find_element_by_id('edit_attendee_3').click()
        namebox = self.browser.find_element_by_id('id_edit_name')
        namebox.clear()
        namebox.send_keys('Tony Soprano\n')
        self.check_for_row_in_roll_table('Tony Soprano')
        try:
            self.check_for_row_in_roll_table('Tony Tiger')  # should not find
            self.assertFalse(True)
        except AssertionError:
            self.assertTrue(True)
        # John assigns each a roll number based on how much he likes them. They automatically order
        # on save
        # John likes Tony, so he sets him to be first in the ranking
        self.browser.find_element_by_id('edit_attendee_3').click()
        orderbox = self.browser.find_element_by_id('id_edit_order')
        orderbox.clear()
        orderbox.send_keys('1\n')
        expected_order = ['Tony Soprano', 'Alexander Hamilton', 'Daveed Diggs']
        self.check_table_row_ordering(expected_order)

        #The program prevents him from assigning a duplicate ordering number
        self.browser.find_element_by_id('edit_attendee_1').click()
        orderbox = self.browser.find_element_by_id('id_edit_order')
        orderbox.clear()
        orderbox.send_keys('1\n')
        expected_order = ['Tony Soprano', 'Alexander Hamilton', 'Daveed Diggs']
        self.check_table_row_ordering(expected_order)

        # John hates Alex, so he sends him to the end of the list
        self.browser.find_element_by_id('edit_attendee_2').click()
        orderbox = self.browser.find_element_by_id('id_edit_order')
        orderbox.clear()
        orderbox.send_keys('\n')
        expected_order = ['Tony Soprano', 'Daveed Diggs', 'Alexander Hamilton']
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

        # John wants to add more people to his roll, but he still hates Alex so he wants
        # to make sure Alex stays at the end. He clicks "Give new attendees order numbers"
        self.fail('Do I want to do this? If I plan on just making a seperate attendee creator, that will render this mostly useless')
        # He then adds a new attendee

        # The app assigns the attendee the next lowest available roll number, and shows the member
        # below all others with numbers, but above those without
