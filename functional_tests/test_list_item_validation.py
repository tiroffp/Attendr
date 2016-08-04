from functional_tests.base import FunctionalTest
# from unittest import skip


class AttendeeValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_roll_attendees(self):
        # Mary goes to the home page and accidentally tries to submit
        # an empty roll attendee. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.get_attendee_input_box().send_keys('\n')
        # The home page refreshes, and there is an error message saying
        # that roll attendees cannot be blank
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an attendee without a name")
        # She tries again with some text for the attendee, which now works
        self.get_attendee_input_box().send_keys('Buy milk\n')
        self.check_for_row_in_roll_table('1: Buy milk')
        # Perversely, she now decides to submit a second blank roll attendee
        self.get_attendee_input_box().send_keys('\n')
        # She receives a similar warning on the roll page
        self.check_for_row_in_roll_table('1: Buy milk')
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an attendee without a name")
        # And she can correct it by filling some text in
        self.get_attendee_input_box().send_keys('Make tea\n')
        self.check_for_row_in_roll_table('1: Buy milk')
        self.check_for_row_in_roll_table('2: Make tea')

    def test_cannot_add_duplicate_attendees(self):
        # Mary goes to the home page and starts a new roll
        self.browser.get(self.live_server_url)
        self.get_attendee_input_box().send_keys('Buy wellies\n')
        self.check_for_row_in_roll_table('1: Buy wellies')

        # She accidentally tries to enter a duplicate attendee
        self.get_attendee_input_box().send_keys('Buy wellies\n')
        error = self.get_error_element()
        self.assertEqual(error.text, "This name is already on the roll")

    def test_error_messages_are_cleared_on_input(self):
        # Mary starts a new roll in a way that causes a validation error
        self.browser.get(self.live_server_url)
        self.get_attendee_input_box().send_keys('\n')
        error = self.get_error_element()
        self.assertTrue(error.is_displayed())

        # She starts typing in the input box to clear the error
        self.get_attendee_input_box().send_keys('a')

        # She is pleased to see the error message disappears
        error = self.get_error_element()
        self.assertFalse(error.is_displayed())
