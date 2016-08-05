from django.shortcuts import render, redirect
from create_roll.models import Roll
from create_roll.forms import AttendeeForm, ExistingRollAttendeeForm


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
