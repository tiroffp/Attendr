from django.test import TestCase
from django.utils.html import escape
from create_roll.models import Attendee, Roll
from create_roll.forms import (
    AttendeeForm,
    EMPTY_ERROR_MESSAGE,
    DUPLICATE_ATTENDEE_ERROR,
    ExistingRollAttendeeForm)


class HomePageTest(TestCase):
    maxDiff = None

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_attendee_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], AttendeeForm)


class RollViewTest(TestCase):
    def test_displays_only_attendees_for_that_roll(self):
        correct_roll = Roll.objects.create()
        Attendee.objects.create(name='attendeey 1', roll=correct_roll)
        Attendee.objects.create(name='attendeey 2', roll=correct_roll)
        other_roll = Roll.objects.create()
        Attendee.objects.create(name='other roll attendee 1', roll=other_roll)
        Attendee.objects.create(name='other roll attendee 2', roll=other_roll)

        response = self.client.get('/create_roll/%d/' % (correct_roll.id,))
        self.assertContains(response, 'attendeey 1')
        self.assertContains(response, 'attendeey 2')
        self.assertNotContains(response, 'other roll attendee 1')
        self.assertNotContains(response, 'other roll attendee 2')

    def test_uses_roll_template(self):
        roll_ = Roll.objects.create()
        response = self.client.get('/create_roll/%d/' % (roll_.id,))
        self.assertTemplateUsed(response, 'roll.html')

    def test_passes_correct_roll_to_template(self):
        correct_roll = Roll.objects.create()
        response = self.client.get('/create_roll/%d/' % (correct_roll.id,))
        self.assertEqual(response.context['roll'], correct_roll)

    def test_can_save_a_POST_request_to_an_existing_roll(self):
        Roll.objects.create()
        correct_roll = Roll.objects.create()
        self.client.post(
            '/create_roll/%d/' % (correct_roll.id,),
            data={'name': 'A new attendee for an existing roll'}
        )

        self.assertEqual(Attendee.objects.count(), 1)
        new_attendee = Attendee.objects.first()
        self.assertEqual(new_attendee.name, 'A new attendee for an existing roll')
        self.assertEqual(new_attendee.roll, correct_roll)

    def test_POST_redirects_to_roll_view(self):
        Roll.objects.create()
        correct_roll = Roll.objects.create()
        response = self.client.post(
            '/create_roll/%d/' % (correct_roll.id,),
            data={'name': 'A new attendee for an existing roll'}
        )
        self.assertRedirects(response, '/create_roll/%d/' % (correct_roll.id,))

    def post_invalid_input(self):
        roll_ = Roll.objects.create()
        return self.client.post(
            '/create_roll/%d/' % (roll_.id,),
            data={'name': ''}
        )

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Attendee.objects.count(), 0)

    def test_for_invalid_input_renders_roll_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'roll.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingRollAttendeeForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        expected_error = escape(EMPTY_ERROR_MESSAGE)
        self.assertContains(response, expected_error)

    def test_duplicate_attendee_validation_errors_end_up_on_create_roll_page(self):
        roll1 = Roll.objects.create()
        Attendee.objects.create(roll=roll1, name='nameey')
        response = self.client.post(
            '/create_roll/%d/' % (roll1.id,),
            data={'name': 'nameey'}
        )

        expected_error = escape(DUPLICATE_ATTENDEE_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'roll.html')
        self.assertEqual(Attendee.objects.all().count(), 1)

    def test_displays_attendee_form(self):
        roll_ = Roll.objects.create()
        response = self.client.get('/create_roll/%d/' % (roll_.id,))
        self.assertIsInstance(response.context['form'], ExistingRollAttendeeForm)
        self.assertContains(response, 'name="name"')

    def test_displays_attendees_in_order(self):
        roll = Roll.objects.create()
        self.client.post(
            '/create_roll/%d/' % (roll.id,),
            data={'name': 'Mister First'}
        )
        response = self.client.post(
            '/create_roll/%d/' % (roll.id,),
            data={'name': 'Mister Second'}
        )
        response = self.client.get(
            '/create_roll/%d/' % (roll.id,),
        )
        first_attendee, second_attendee = response.context['attendees']
        self.assertEqual(first_attendee.name, 'Mister First')
        self.assertEqual(second_attendee.name, 'Mister Second')


class NewRollTest(TestCase):
    def test_saving_a_POST_request(self):
        self.client.post('/create_roll/new',
                         data={'name': 'A new roll attendee'})
        self.assertEqual(Attendee.objects.count(), 1)
        new_attendee = Attendee.objects.first()
        self.assertEqual(new_attendee.name, 'A new roll attendee')

    def test_redirects_after_POST(self):
        response = self.client.post('/create_roll/new',
                                    data={'name': 'A new roll attendee'})
        new_roll = Roll.objects.first()
        self.assertRedirects(response, '/create_roll/%d/' % (new_roll.id,))

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/create_roll/new', data={'name': ''})
        self.assertEqual(response.status_code, 200)
        self. assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/create_roll/new', data={'name': ''})
        expected_error = escape(EMPTY_ERROR_MESSAGE)
        self.assertContains(response, expected_error)

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/create_roll/new', data={'name': ''})
        self.assertIsInstance(response.context['form'], AttendeeForm)

    def test_invalid_roll_attendees_arent_saved(self):
        self.client.post('create_roll/new', data={'name': ''})
        self.assertEquals(Roll.objects.count(), 0)
        self.assertEquals(Attendee.objects.count(), 0)
