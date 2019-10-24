"""

Notifications tools for sending users information regarding their appointments
for cancellations, bookings, reminders, etc

"""
from django.core.mail import send_mail
from models import PatientAppointmentSlot
from datetime import datetime, timedelta
from django.template import Context
import boto3


def send_reminder_text(appt):
	'''
	Send a text message to the patient if 30 min in advance
	'''

	sns = boto3.client('sns')
	message = get_template('notifications/appointment_text.html').render(
		Context({
			'appointment' : appt
		}))
	response = sns.publish(PhoneNumber=appt.patient.info.phone_number, Message=message)
	appt.last_notification = datetime.utcnow()
	appt.save()
	return response['HttpStatusCode'] == 200
	

def send_appointment_email(appt, template='notifications/appointment_reminder.html', 
								subject='Virtudent Appointment Redminder'):
	'''
	Send an email
	'''
	message = get_template(template).render(
		Context({
			'appointment' : appt
		}))
	print message
	send_mail(
	    subject,
	    message,
	    'no-reply@myvirtudent.com',
	    appt.patient.user.email,
	    fail_silently=False,
	)
	

def send_reminder_notifications():
	'''
	Send notifications to all users depending on how far in advance
	we are from their next appointment
	'''

	now = datetime.utcnow()
	max_ahead = now + timedelta(days=8)
	appointments = PatientAppointmentSlot.objects.filter(start__gte=now,
									is_booked=True, start_lte=max_ahead)
	for appt in appointments:

		appt.refresh_from_db()
		time_till_appt = appt.start - now
		notif_delta = appt.start - appt.last_notification

		if notif_delta > timedelta(days=7) and time_till_appt < timedelta(days=7)
			send_reminder_email(appt)
			appt.last_notification = datetime.utcnow()
			appt.save()
		if notif_delta > timedelta(days=1) and time_till_appt < timedelta(days=1)
			send_reminder_email(appt)
			appt.last_notification = datetime.utcnow()
			appt.save()
		if notif_delta > timedelta(minutes=30) and time_till_appt < timedelta(minutes=30)
			send_text(appt)
			appt.last_notification = datetime.utcnow()
			appt.save()


