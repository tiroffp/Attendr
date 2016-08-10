from django.shortcuts import render, redirect
from create_roll.models import Roll, Attendee
from create_roll.forms import (AttendeeForm,
                               ExistingRollAttendeeForm,
                               EditAttendeeForm)


def home_page(request):
    return render(request, 'home.html', {'form': AttendeeForm()})


def view_roll(request, roll_id):
    roll = Roll.objects.get(id=roll_id)
    form = ExistingRollAttendeeForm(for_roll=roll)
    if request.method == 'POST':
        form = ExistingRollAttendeeForm(for_roll=roll, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(roll)
    attendees = roll.attendee_set.order_by('id')
    return render(request,
                  'roll.html',
                  {'roll': roll, 'attendees': attendees, 'form': form})


def new_roll(request):
    form = AttendeeForm(data=request.POST)
    if form.is_valid():
        roll = Roll.objects.create()
        form.save(for_roll=roll)
        return redirect(roll)
    else:
        return render(request, 'home.html', {"form": form})


def edit_roll(request, roll_id, attendee_id):
    roll = Roll.objects.get(id=roll_id)
    attendee_id = int(attendee_id)
    if request.method == 'POST':
        edit_form = EditAttendeeForm(attendee_id=attendee_id,
                                     data=request.POST)
        if edit_form.is_valid():
            edit_form.save()
            return redirect(roll)
    attendees = roll.attendee_set.order_by('id')
    form = ExistingRollAttendeeForm(for_roll=roll)
    attendee_model = Attendee.objects.get(id=attendee_id)
    edit_data = {'name': attendee_model.name}
    edit_attendee_form = EditAttendeeForm(data=edit_data, attendee_id=attendee_id)
    edit_attendee_form.name = 'Johnny'
    return render(request,
                  'edit_roll.html',
                  {'roll': roll,
                   'attendees': attendees,
                   'edit_attendee_id': attendee_id,
                   'edit_attendee_form': edit_attendee_form,
                   'form': form})
