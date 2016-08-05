from django.test import TestCase
from create_roll.forms import (
    AttendeeForm,
    EMPTY_ERROR_MESSAGE,
    DUPLICATE_ATTENDEE_ERROR,
    ExistingRollAttendeeForm)
from create_roll.models import Attendee, Roll


class AttendeeFormTest(TestCase):

    def test_form_renders_text_input(self):
            form = AttendeeForm()
            self.assertIn('placeholder="Enter an attendee"', form.as_p())
            self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_attendees(self):
            form = AttendeeForm(data={'name': ''})
            self.assertFalse(form.is_valid())
            self.assertEqual(form.errors['name'],
                             [EMPTY_ERROR_MESSAGE]
                             )

    def test_form_save_handles_saving_to_a_roll(self):
        roll = Roll.objects.create()
        form = AttendeeForm(data={'name': 'do me'})
        new_attendee = form.save(for_roll=roll)
        self.assertEqual(new_attendee, Attendee.objects.first())
        self.assertEqual(new_attendee.name, 'do me')
        self.assertEqual(new_attendee.roll, roll)


class ExistingRollAttendeeFormTest(TestCase):

    def test_form_renders_attendee_name_input(self):
        roll = Roll.objects.create()
        form = ExistingRollAttendeeForm(for_roll=roll)
        self.assertIn('placeholder="Enter an attendee"', form.as_p())

    def test_form_validation_for_blank_attendees(self):
        roll = Roll.objects.create()
        form = ExistingRollAttendeeForm(for_roll=roll, data={'name': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'],
                         [EMPTY_ERROR_MESSAGE]
                         )

    def test_form_validation_for_duplicate_attendees(self):
        roll = Roll.objects.create()
        Attendee.objects.create(roll=roll, name='no twins!')
        form = ExistingRollAttendeeForm(for_roll=roll, data={'name': 'no twins!'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], [DUPLICATE_ATTENDEE_ERROR])

    def test_form_save(self):
        roll = Roll.objects.create()
        form = ExistingRollAttendeeForm(for_roll=roll, data={'name': 'hi'})
        new_attendee = form.save()
        self.assertEqual(new_attendee, Attendee.objects.all()[0])
