from django import forms
from django.core.exceptions import ValidationError
from create_roll.models import Attendee

EMPTY_ERROR_MESSAGE = "You can't have an attendee without a name"
DUPLICATE_ATTENDEE_ERROR = "This name is already on the roll"


class AttendeeForm(forms.models.ModelForm):

    class Meta:
        model = Attendee
        fields = ('name',)
        widgets = {
            'name': forms.fields.TextInput(attrs={
                'placeholder': 'Enter an attendee',
                'class': 'form-control input-lg',
                }),
        }
        error_messages = {
            'name': {'required': EMPTY_ERROR_MESSAGE}
        }

    def save(self, for_roll):
        self.instance.roll = for_roll
        return super().save()


class ExistingRollAttendeeForm(AttendeeForm):
    def __init__(self, for_roll, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.roll = for_roll

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'name': [DUPLICATE_ATTENDEE_ERROR]}
            self._update_errors(e)

    def save(self):
        return forms.models.ModelForm.save(self)


class EditAttendeeForm(forms.models.ModelForm):
    def __init__(self, attendee_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance = Attendee.objects.get(id=attendee_id)

    class Meta:
        model = Attendee
        fields = ('name', 'order')
        widgets = {
            'name': forms.fields.TextInput(attrs={
                'class': 'form-inline',
                }),
            'order': forms.fields.TextInput(attrs={
                'class': 'form-inline',
                }),
        }
        error_messages = {
            'name': {'required': EMPTY_ERROR_MESSAGE}
        }

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'name': [DUPLICATE_ATTENDEE_ERROR]}
            self._update_errors(e)
