from django.test import TestCase
from django.core.exceptions import ValidationError
from create_roll.models import Attendee, Roll


class ModelTest(TestCase):

    def test_default_text(self):
        attendee = Attendee()
        self.assertEqual(attendee.name, '')

    def test_attendee_is_related_to_roll(self):
        roll = Roll.objects.create()
        attendee = Attendee()
        attendee.roll = roll
        attendee.save()
        self.assertIn(attendee, roll.attendee_set.all())

    def test_cannot_save_empty_roll_attendees(self):
        roll = Roll.objects.create()
        attendee = Attendee(roll=roll, name='')
        with self.assertRaises(ValidationError):
            attendee.save()
            attendee.full_clean()

    def test_dupliacte_attendees_are_invalid(self):
        roll = Roll.objects.create()
        Attendee.objects.create(roll=roll, name='bla')
        with self.assertRaises(ValidationError):
            attendee = Attendee(roll=roll, name='bla')
            attendee.full_clean()

    def test_CAN_save_attendee_to_different_create_roll(self):
        roll1 = Roll.objects.create()
        roll2 = Roll.objects.create()
        Attendee.objects.create(roll=roll1, name='bla')
        attendee = Attendee(roll=roll2, name='bla')
        attendee.full_clean()  # should not raise


class RollModelTest(TestCase):

    def test_get_absolute_url(self):
        roll = Roll.objects.create()
        self.assertEqual(roll.get_absolute_url(), '/create_roll/%d/' % (roll.id,))
