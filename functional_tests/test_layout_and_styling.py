from functional_tests.base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # Mary goes to the homepage
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1034, 768)

        # She notices the input box is nicely centered
        inputbox = self.get_attendee_input_box()
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2,
                               512, delta=5)
        # She starts a new roll and sees the input box remains nicely centered
        inputbox.send_keys('testing\n')
        inputbox = self.get_attendee_input_box()
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2,
                               512, delta=5)
