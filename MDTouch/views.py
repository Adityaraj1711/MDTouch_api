# File: views.py
# Description: This file contains Python and Django code which will form the
#              Controller element of the Model-Template-Controller (MTC) design
#              pattern.
# Author(s): Devil Corp

# imports
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from .models import Test
from .models import Patient
from .models import EmergencyContact
from .models import Doctor
from .models import Nurse
from .models import Prescription
from .models import Hospital
from .models import Appointment
from .models import LogInInfo
from .models import Administrator
from .models import Message
from .models import Event
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
import datetime
from datetime import date
import os
import csv

# This variable is for storing the username entered when a user logs-in
uname = ''


# This module handles the logging of activities by saving logs to a plaintext file which is then rendered
# in HTML for administrators to view.
def logActivity(activity):
    filename = "log.txt"
    cwd = os.getcwd()
    target = open(cwd + "\\MDTouch\\log\\" + filename, 'a')
    target.write(activity)
    target.write("\n")
    target.close()

def index(request):
    return render(request,'MDTouch/getstarted.html')

# This module handles the generic template view for the index page in which users will log-in or register
# if they have not made credentials.
class IndexView(generic.ListView):
    template_name = 'MDTouch/index.html'
    context_object_name = 'user_login_information'

    def get_queryset(self):
        return LogInInfo.objects.order_by('-username')


# This module simply renders the HTML page for the registration screen.
def registerP(request):
    return render(request, 'MDTouch/registerP.html')


# This module handles the user registration. The "LogInInfo" object is used to store their credentials in the database.
def createPLogIn(request):
    firstName = (request.POST['firstName'])
    lastName = (request.POST['lastName'])
    address = (request.POST['address'])
    number = (request.POST['number'])
    email = (request.POST['email'])
    provider = (request.POST['provider'])
    insuranceid = (request.POST['insuranceid'])
    contactfname = (request.POST['contactfname'])
    contactlname = (request.POST['contactlname'])
    contactaddress = (request.POST['contactaddress'])
    contactnumber = (request.POST['contactnumber'])
    height = (request.POST['height'])
    weight = (request.POST['weight'])
    allergies = (request.POST['allergies'])
    gender = (request.POST['gender'])
    username = (request.POST['username'])
    password = (request.POST['password'])
    try:
        logininfo = LogInInfo.objects.get(username=username)
    except ObjectDoesNotExist:
        LogInInfo.objects.create(username=username, password=password)
        #global uname
        uname = username
        request.session['uname'] = uname
        try:
            contact = EmergencyContact.objects.get(firstName=contactfname, lastName=contactlname,
                                                      address=contactaddress, number=contactnumber)
        except ObjectDoesNotExist:
            contact = EmergencyContact.objects.create(firstName=contactfname, lastName=contactlname,
                                                      address=contactaddress, number=contactnumber)
        Patient.objects.create(username=uname)
        patient = Patient.objects.get(username=uname)
        patient.firstName = firstName
        patient.lastName = lastName
        patient.address = address
        patient.number = number
        patient.email = email
        patient.provider = provider
        patient.insuranceid = insuranceid
        patient.contact = contact
        patient.height = height
        patient.weight = weight
        patient.allergies = allergies
        patient.gender = gender
        patient.password = password
        patient.save()
        import datetime
        activity = "User " + username + " registered a new account - logged on: " #+\
                   #datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
        #logActivity(activity)
        return HttpResponseRedirect(reverse('MDTouch:home', args=()))
    else:
        return render(request, 'MDTouch/registerP.html', {
            'username': username,
            'error_message': "Username already exists.",
        })


# This module simply renders the HTML page for the password change screen.
def password(request):
    return render(request, 'MDTouch/password.html')


# This module handles the changing of a user's password
def changePass(request):
    try:
        username = (request.POST["username"])
        newpass = (request.POST["password"])
        currinfo = LogInInfo.objects.get(username=username)
        pat = Patient.objects.get(username=username)
    except LogInInfo.DoesNotExist:
        return render(request, 'MDTouch/password.html', {
            'username': username,
            'error_message': "There was a problem with your username.",
            })
    else:
        currinfo.password = newpass
        pat.password = newpass
        #print(currinfo.password,pat.password,newpass,"success (((((()))))))))))")
        currinfo.save()
        pat.save()
        #s = Patient.objects.get(username=username)
        #print(s.password)
        activity = "User " + username + " changed their password - logged on: " #+\
                   #datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
        #logActivity(activity)
        return HttpResponseRedirect(reverse('MDTouch:index', args=()))


# This module handles the attempt of a user to log-in to their profile. If the username and password are valid,
# the user is redirected to their profile. If not, an error message is generated and the user is
# redirected to the index page.
def verify(request):
    username = (request.POST.get('username'))
    passwordInput = (request.POST.get('password'))

    try:
        current = LogInInfo.objects.get(username=username)
    except LogInInfo.DoesNotExist:
        return render(request, 'MDTouch/index.html', {
            'username': username,
            'error_message': "There was a problem with your username.",
        })
    else:
        passwordActual = current.password
        if passwordInput == passwordActual :
            #global uname
            uname = username
            request.session['uname'] = uname
            activity = "User " + username + " logged in - logged on: " #+ datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
            #logActivity(activity)
            return HttpResponseRedirect(reverse('MDTouch:home', args=()))
        else:
            return render(request, 'MDTouch/index.html', {
                'username': username,
                'error_message': "There was a problem with your password.",
            })


# This module simply renders the home page for a user
def home(request):
    if request.session.has_key('uname'):
        uname = request.session['uname']
    else:
        return render(request,'MDTouch/index.html', {
                'username': uname,
                'error_message': "Multiple account access",
            })
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                try:
                    a = Administrator.objects.get(username=uname)
                except Administrator.DoesNotExist:
                    return render(request, 'MDTouch/index.html', {
                        'error_message': "An error has occurred"
                        })
                else:
                    utype = "Administrator"
                    context = {'user': a,
                               'type': utype}
                    return render(request, 'MDTouch/home.html', context)
            else:
                utype = "Nurse"
                context = {'user': n,
                           'type': utype}
                return render(request, 'MDTouch/home.html', context)
        else:
            utype = "Doctor"
            context = {'user': d,
                       'type': utype}
            return render(request, 'MDTouch/home.html', context)
    else:
        utype = "Patient"
        context = {'user': p,
                   'type': utype}
        return render(request, 'MDTouch/home.html', context)


# This module simply renders the HTML page for the doctor and nurse registration screen.
def registerDN(request):
    uname = request.session['uname']
    workplaces = Hospital.objects.order_by("-name")
    admin = Administrator.objects.get(username=uname)
    context = {'workplaces': workplaces,
               'admin': admin}
    return render(request, 'MDTouch/registerDN.html', context)


# This module handles the doctor and nurse registration. The "LogInInfo" object is used to store their credentials
# in the database.
def createDNLogIn(request):
    uname = request.session['uname']
    firstName = (request.POST['firstName'])
    lastName = (request.POST['lastName'])
    type = (request.POST['type'])
    username = (request.POST['username'])
    password = (request.POST['password'])
    admin = Administrator.objects.get(username=uname)
    try:
        logininfo = LogInInfo.objects.get(username=username)
    except ObjectDoesNotExist:
        LogInInfo.objects.create(username=username, password=password)
        if type == "Doctor":
            Doctor.objects.create(username=username, firstName=firstName, lastName=lastName,password=password)
            d = Doctor.objects.get(username=username)
            d.workplace = admin.workplace
            d.save()
            activity = "Administrator " + uname + " registered a new doctor account - logged on: " #+ \
                       #datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
            #logActivity(activity)
            return HttpResponseRedirect(reverse('MDTouch:home', args=()))
        elif type == "Nurse":
            Nurse.objects.create(username=username,  firstName=firstName, lastName=lastName,password=password)
            n = Nurse.objects.get(username=username)
            n.workplace = admin.workplace
            n.save()
            activity = "Administrator " + uname + " registered a new nurse account - logged on: " #+ \
                       #datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
            #logActivity(activity)
            return HttpResponseRedirect(reverse('MDTouch:home', args=()))
        else:
            Administrator.objects.create(username=username, firstName=firstName, lastName=lastName,password=password)
            a = Administrator.objects.get(username=username)
            a.workplace = admin.workplace
            a.save()
            activity = "Administrator " + uname + " registered a new Administrator account - logged on: " #+ \
                       #datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
            #logActivity(activity)
            return HttpResponseRedirect(reverse('MDTouch:home', args=()))
    else:
        return render(request, 'MDTouch/registerDN.html', {
            'username': username,
            'workplace': Hospital.objects.order_by("-name"),
            'error_message': "Username already exists.",
        })


# This module simply renders the HTML page for the user information screen.
def information(request):
    #global uname
    uname = request.session['uname']
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                return render(request, 'MDTouch/home.html', {
                    'error_message': "An error has occurred"
                })
            else:
                utype = "Nurse"
                patients = Patient.objects.order_by("-lastName")
                patw = Patient.objects.filter(hospital=n.workplace)
                context = {'patients': patients,
                           'patw': patw,
                           'employee': n,
                           'type': utype}
                return render(request, 'MDTouch/information.html', context)
        else:
            utype = "Doctor"
            patients = Patient.objects.order_by("-lastName")
            patw = Patient.objects.filter(hospital=d.workplace)
            context = {'patients': patients,
                       'patw': patw,
                       'employee': d,
                       'type': utype}
            return render(request, 'MDTouch/information.html', context)
    else:
        utype = "Patient"
        user = Patient.objects.get(username = uname)
        tests = Test.objects.filter(patient=p)
        context = {'user':user,
                    'patient': p,
                   'type': utype,
                   'tests': tests}
        return render(request, 'MDTouch/information.html', context)


# This module simply renders the HTML page for the update profile screen.
def updatePro(request):
    #global uname
    uname = request.session['uname']
    patient = Patient.objects.get(username=uname)
    context = {'patient': patient}
    return render(request, 'MDTouch/updatePro.html', context)


# This module handles modifying the database object for a patient's profile information after retrieving POST data from
# the form submission. After the object is updated and saved, the user is redirected to the user information screen.
def updateProInfo(request):
    firstName = (request.POST['firstName'])
    lastName = (request.POST['lastName'])
    address = (request.POST['address'])
    number = (request.POST['number'])
    email = (request.POST['email'])
    provider = (request.POST['provider'])
    insuranceid = (request.POST['insuranceid'])
    contactfname = (request.POST['contactfname'])
    contactlname = (request.POST['contactlname'])
    contactaddress = (request.POST['contactaddress'])
    contactnumber = (request.POST['contactnumber'])
    try:
        contact = EmergencyContact.objects.get(firstName=contactfname, lastName=contactlname, address=contactaddress,
                                               number=contactnumber)
    except ObjectDoesNotExist:
        contact = EmergencyContact.objects.create(firstName=contactfname, lastName=contactlname, address=contactaddress,
                                                  number=contactnumber)
    uname = request.session['uname']
    patient = Patient.objects.get(username=uname)
    patient.firstName = firstName
    patient.lastName = lastName
    patient.address = address
    patient.number = number
    patient.email = email
    patient.provider = provider
    patient.insuranceid = insuranceid
    patient.contact = contact
    patient.save()
    activity = "User " + patient.username #+ " updated their profile information - logged on: " +\
               #datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    #logActivity(activity)
    return HttpResponseRedirect(reverse('MDTouch:information', args=()))


# This module simply renders the HTML page for the update medical information screen.
def updateMed(request, pat_id):
    #global uname
    uname = request.session['uname']
    patient = Patient.objects.get(id=pat_id)
    context = {'patient': patient}
    return render(request, 'MDTouch/updateMed.html', context)


# This module handles modifying the database object for a patient's medical information after retrieving POST data from
# the form submission. After the object is updated and saved, the user is redirected to the user information screen.
def updateMedInfo(request, pat_id):
    uname = request.session['uname']
    height = (request.POST['height'])
    weight = (request.POST['weight'])
    allergies = (request.POST['allergies'])
    gender = (request.POST['gender'])
    patient = Patient.objects.get(id=pat_id)
    patient.height = height
    patient.weight = weight
    patient.allergies = allergies
    patient.gender = gender
    patient.save()
    activity = "User " + uname + " updated Patient " + patient.username + "'s medical information - logged on: " #+\
               #datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    #logActivity(activity)
    return HttpResponseRedirect(reverse('MDTouch:information', args=()))


# This module when activated, downloads the current patient's information onto their current computer in a .csv file.
def export(request):
    #global uname
    uname = request.session['uname']
    patient = Patient.objects.get(username=uname)
    testResults = Test.objects.filter(patient=patient, released=True)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="PatientInfo.csv"'
    filewriter = csv.writer(response)
    filewriter.writerow(['', 'Name', 'Email', 'Address', 'Phone Number', 'Insurance ID', 'Insurance Provider'])
    filewriter.writerow(['Patient Profile Info:', patient.lastName + "," + patient.firstName, patient.email, patient.address, patient.number, patient.insuranceid, patient.provider])
    filewriter.writerow([''])
    filewriter.writerow(['', 'Name', 'Address', 'Phone Number'])
    filewriter.writerow(['Patient Emergency Contact:', patient.contact.lastName + ", " + patient.contact.firstName, patient.contact.address, patient.contact.number])
    filewriter.writerow([''])
    filewriter.writerow(['', 'Height', 'Weight', 'Allergies', 'Gender'])
    filewriter.writerow(['Patient Medical Information:', patient.height, patient.weight, patient.allergies, patient.gender])
    filewriter.writerow([''])
    filewriter.writerow(['Patient Test Information', 'Name', 'Doctor Notes', 'Doctor Name'])
    count = 1
    for test in testResults:
        filewriter.writerow(['Test ' + str(count), test.name, test.description, test.doctor])
        count += 1
    activity = "User " + patient.username + " exported their information - logged on: " #+\
               #datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    #logActivity(activity)
    return response


# This module handles discharging a patient from a hospital.
def discharge(request, pat_id):
    patient = Patient.objects.get(id=pat_id)
    patient.hospital = None
    patient.save()
    return HttpResponseRedirect(reverse('MDTouch:information', args=()))


# This module handles admitting a patient to a hospital.
def admission(request, pat_id, emp_id):
    patient = Patient.objects.get(id=pat_id)
    hospital = Hospital.objects.get(id=emp_id)
    patient.hospital = hospital
    patient.save()
    return HttpResponseRedirect(reverse('MDTouch:information', args=()))


# This module handles transferring a patient from one hospital to another.
def transfer(request, pat_id, emp_id):
    patient = Patient.objects.get(id=pat_id)
    hospital = Hospital.objects.get(id=emp_id)
    patient.hospital = hospital
    patient.save()
    return HttpResponseRedirect(reverse('MDTouch:information', args=()))


# This module simply renders the HTML page for the Tests screen.
def tests(request, pat_id):
    p = Patient.objects.get(id=pat_id)
    t = Test.objects.filter(patient=p)
    context = {'patient': p,
               'test': t}
    return render(request, 'MDTouch/tests.html', context)


# This module simply renders the HTML page for the Create Test screen
def createTest(request, pat_id):
    #global uname
    uname = request.session['uname']
    patient = Patient.objects.get(id=pat_id)
    context = {'patient': patient}
    return render(request, 'MDTouch/createTest.html', context)


# This module handles creating a database object for a test after retrieving POST data from the form submission.
# After the object is created and saved, the user is redirected to the main Tests screen.
def createTestInfo(request, pat_id):
    #global uname
    uname = request.session['uname']
    name = (request.POST['name'])
    t = Test.objects.create()
    description = (request.POST['description'])
    try:
        if request.FILES['file']:
            file = request.FILES['file']
    except MultiValueDictKeyError:
        placeholder = ""
        t.testResults = placeholder
    else:
        t.testResults = file
    patient = Patient.objects.get(id=pat_id)
    doctor = Doctor.objects.get(username=uname)
    t.name = name
    t.description = description

    t.doctor = doctor
    t.patient = patient
    t.save()
    #activity = "Doctor " + doctor.username + " created a new test for Patient " + patient.username + " - logged on: " +\
               #datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    #logActivity(activity)
    return HttpResponseRedirect(reverse('MDTouch:tests', args=pat_id))


# This module handles releasing a previously unreleased test for a patient. Afterwards, the user is redirected
# to the main Tests page
def releaseTest(request, test_id):
    t = Test.objects.get(id=test_id)
    t.released = True
    t.save()
    #activity = "Patient " + t.patient.username + "'s test results were released by Doctor " + t.doctor.username +\
    #           " - logged on: " + datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    #logActivity(activity)
    return HttpResponseRedirect(reverse('MDTouch:tests', args=(t.patient.id,)))


# This module simply renders the HTML page for patients to view the details of a released test
def testDetails(request, test_id):
    #global uname
    uname = request.session['uname']
    test = Test.objects.get(id=test_id)
    context = {'test': test}
    return render(request, 'MDTouch/testDetails.html', context)


# This module simply renders the HTML page for the appointments screen.
def appointments(request):
    #global uname
    uname = request.session['uname']
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n= Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                return render(request, 'MDTouch/home.html', {
                    'error_message': "An error has occurred"
                })
            else:
                utype = "Nurse"
                # Nurses can create and update an appointment with a Doctor at the location they work.
                # Nurses cannot cancel appointments.
                appointments = Appointment.objects.filter(location=n.workplace)
                context = {'appointments': appointments,
                           'employee': n,
                           'type': utype}
                return render(request, 'MDTouch/appointments.html', context)
        else:
            utype = "Doctor"
            # Doctors can create and update an appointment with a Doctor at a location they work.
            # Doctors can cancel THEIR appointments.
            appointments = Appointment.objects.filter(location=d.workplace)
            this_appointments = Appointment.objects.filter(doctor=d)
            context = {'appointments': appointments,
                       'this_appointments': this_appointments,
                       'employee': d,
                       'type': utype}
            return render(request, 'MDTouch/appointments.html', context)
    else:
        utype = "Patient"
        # Patients can create an appointment with any Doctor
        # Patients can update THEIR appointments
        # Patients can cancel THEIR appointments
        appointments = Appointment.objects.filter(patient=p)
        context = {'appointments': appointments,
                   'user': p,
                   'type': utype}
        return render(request, 'MDTouch/appointments.html', context)


# This module simply renders the HTML page for the create appointment screen.
def createAppt(request):
    #global uname
    uname = request.session['uname']
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                return render(request, 'MDTouch/home.html', {
                    'error_message': "An error has occurred"
                })
            else:
                utype = "Nurse"
                # Nurses can create an appointment with any patient and any Doctor from their workplace.
                patients = Patient.objects.order_by("-lastName")
                doctors = Doctor.objects.filter(workplace=n.workplace)
                context = {'patients': patients,
                           'doctors': doctors,
                           'type': utype}
                return render(request, 'MDTouch/createAppt.html', context)
        else:
            utype = "Doctor"
            # Doctors can create an appointment with any patient with themselves.
            patients = Patient.objects.order_by("-lastName")
            context = {'patients': patients,
                       'doctor': d,
                       'type': utype}
            return render(request, 'MDTouch/createAppt.html', context)
    else:
        utype = "Patient"
        # Patients can create an appointment with any Doctor
        doctors = Doctor.objects.order_by("-lastName")
        context = {'patient': p,
                   'doctors': doctors,
                   'type': utype}
        return render(request, 'MDTouch/createAppt.html', context)

from django.utils import timezone

# This module handles creating a database object for an appointment after retrieving POST data from the form submission.
# After the object is created and saved, the user is redirected to the appointments screen.
def createApptInfo(request):
    uname = request.session['uname']
    patient = Patient.objects.get(id=(request.POST['patient']))
    doctor = Doctor.objects.get(id=(request.POST['doctor']))
    appointmentdate = (request.POST['appointmentdate'])
    appttime = (request.POST['appttime'])
    phase = (request.POST['phase'])
    message = (request.POST['message'])
    location = doctor.workplace
    try:
        appointment = Appointment.objects.get(appttime=appttime, doctor=doctor, appointmentdate = appointmentdate, phase=phase)
    except Appointment.DoesNotExist:
        hp = Appointment.objects.create()
        hp.patient = patient
        hp.doctor = doctor
        hp.appointmentdate = appointmentdate
        hp.appttime = appttime
        hp.phase = phase
        hp.location = location
        hp.message = message
        hp.dateofrequest = timezone.now()
        hp.save()
        #activity = "User " + uname + " created an appointment @ " + location.name + " on " + appointmentdate + "," + appttime + " " + phase + " - logged on: " + datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
        #logActivity(activity)
        return HttpResponseRedirect(reverse('MDTouch:appointments', args=()))
    else:
        try:
            p = Patient.objects.get(username=uname)
        except Patient.DoesNotExist:
            try:
                d = Doctor.objects.get(username=uname)
            except Doctor.DoesNotExist:
                try:
                    n = Nurse.objects.get(username=uname)
                except Nurse.DoesNotExist:
                    return render(request, 'MDTouch/home.html', {
                        'error_message': "An error has occurred"
                    })
                else:
                    utype = "Nurse"
                    # Nurses can create an appointment with any patient and any Doctor from their workplace.
                    patients = Patient.objects.order_by("-lastName")
                    doctors = Doctor.objects.filter(workplace=n.workplace)
                    context = {'patients': patients,
                               'doctors': doctors,
                               'type': utype,
                               'error_message': "The appointment could not be created, the doctor is busy at that time."}
                    return render(request, 'MDTouch/createAppt.html', context)
            else:
                utype = "Doctor"
                # Doctors can create an appointment with any patient with themselves.
                patients = Patient.objects.order_by("-lastName")
                context = {'patients': patients,
                           'doctor': d,
                           'type': utype,
                           'error_message': "The appointment could not be created, the doctor is busy at that time."}
                return render(request, 'MDTouch/createAppt.html', context)
        else:
            utype = "Patient"
            # Patients can create an appointment with any Doctor
            doctors = Doctor.objects.order_by("-lastName")
            context = {'patient': p,
                       'doctors': doctors,
                       'type': utype,
                       'error_message': "The appointment could not be created, the doctor is busy at that time."}
            return render(request, 'MDTouch/createAppt.html', context)


# This module simply renders the HTML page for the update appointment screen.
def updateAppt(request, appt_id):
    #global uname
    uname = request.session['uname']
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                return render(request, 'MDTouch/home.html', {
                    'error_message': "An error has occurred"
                })
            else:
                utype = "Nurse"
                # Nurses can update an appointment to be with any Doctor from their workplace
                appointment = Appointment.objects.get(id=appt_id)
                patient = appointment.patient
                doctors = Doctor.objects.filter(workplace=n.workplace)
                context = {'appointment': appointment,
                           'patient': patient,
                           'doctors': doctors,
                           'type': utype}
                return render(request, 'MDTouch/updateAppt.html', context)
        else:
            utype = "Doctor"
            # Doctors can update an appointment to be with any Doctor from their workplace
            appointment = Appointment.objects.get(id=appt_id)
            patient = appointment.patient
            doctors = Doctor.objects.filter(workplace=d.workplace)
            context = {'appointment': appointment,
                       'patient': patient,
                       'doctors': doctors,
                       'type': utype}
            return render(request, 'MDTouch/updateAppt.html', context)
    else:
        utype = "Patient"
        # Patients can update an appointment to be with any Doctor
        appointment = Appointment.objects.get(id=appt_id)
        doctors = Doctor.objects.order_by("-lastName")
        context = {'appointment': appointment,
                   'patient': p,
                   'doctors': doctors,
                   'type': utype}
        return render(request, 'MDTouch/updateAppt.html', context)


# This module handles modifying the database object for an appointment after retrieving POST data from the form
# submission. After the object is updated and saved, the user is redirected to their appointments screen.
def updateApptInfo(request, appt_id):
    uname = request.session['uname']
    doctor = Doctor.objects.get(id=(request.POST['doctor']))
    appointmentdate = (request.POST['appointmentdate'])
    appttime = (request.POST['appttime'])
    phase = (request.POST['phase'])
    location = doctor.workplace
    try:
        appointment = Appointment.objects.get(appttime=appttime, doctor=doctor, appointmentdate = appointmentdate, phase=phase)
    except Appointment.DoesNotExist:
        appt = Appointment.objects.get(id=appt_id)
        appt.doctor = doctor
        appt.appointmentdate = appointmentdate
        appt.appttime = appttime
        appt.phase = phase
        appt.location = location
        appt.save()
        #activity = "User " + uname + " updated Appointment #" + appt_id + " - logged on: " + \
        #           datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
        #logActivity(activity)
        return HttpResponseRedirect(reverse('MDTouch:appointments', args=()))
    else:
        try:
            p = Patient.objects.get(username=uname)
        except Patient.DoesNotExist:
            try:
                d = Doctor.objects.get(username=uname)
            except Doctor.DoesNotExist:
                try:
                    n = Nurse.objects.get(username=uname)
                except Nurse.DoesNotExist:
                    return render(request, 'MDTouch/home.html', {
                        'error_message': "An error has occurred"
                    })
                else:
                    utype = "Nurse"
                    # Nurses can update an appointment to be with any Doctor from their workplace
                    appointment = Appointment.objects.get(id=appt_id)
                    patient = appointment.patient
                    doctors = Doctor.objects.filter(workplace=n.workplace)
                    context = {'appointment': appointment,
                               'patient': patient,
                               'doctors': doctors,
                               'type': utype,
                               'error_message': "The appointment could not be created, the doctor is busy at that time."}
                    return render(request, 'MDTouch/updateAppt.html', context)
            else:
                utype = "Doctor"
                # Doctors can update an appointment to be with any Doctor from their workplace
                appointment = Appointment.objects.get(id=appt_id)
                patient = appointment.patient
                doctors = Doctor.objects.filter(workplace=d.workplace)
                context = {'appointment': appointment,
                           'patient': patient,
                           'doctors': doctors,
                           'type': utype,
                           'error_message': "The appointment could not be created, the doctor is busy at that time."}
                return render(request, 'MDTouch/updateAppt.html', context)
        else:
            utype = "Patient"
            # Patients can update an appointment to be with any Doctor
            appointment = Appointment.objects.get(id=appt_id)
            doctors = Doctor.objects.order_by("-lastName")
            context = {'appointment': appointment,
                       'patient': p,
                       'doctors': doctors,
                       'type': utype,
                       'error_message': "The appointment could not be created, the doctor is busy at that time."}
            return render(request, 'MDTouch/updateAppt.html', context)


# This module handles deleting the database object for an appointment. Afterwards, the user is redirected to
# their appointments screen.
def cancelAppt(request, appt_id):
    uname = request.session['uname']
    Appointment.objects.get(id=appt_id).delete()
    #activity = "User " + uname + " cancelled Appointment #" + appt_id + " - logged on: " +\
    #           datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    #logActivity(activity)
    return HttpResponseRedirect(reverse('MDTouch:appointments', args=()))


# This module simply loads the HTML page for the prescriptions screen.
def prescriptions(request):
    uname = request.session['uname']
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                return render(request, 'MDTouch/home.html', {
                    'error_message': "An error has occurred"
                })
            else:
                utype = "Nurse"
                pres = Prescription.objects.filter(patient__hospital = n.workplace)
                context = {
                            'prescriptions': pres,
                           'type': utype,
                           'employee': n}
                return render(request, 'MDTouch/prescriptions.html', context)
        else:
            pres = Prescription.objects.filter(doctor=d)
            presatw = Prescription.objects.filter(patient__hospital=d.workplace)
            utype = "Doctor"
            context = {'prescriptions': pres,
                       'presatw': presatw,
                       'type': utype,
                       'employee': d}
            return render(request, 'MDTouch/prescriptions.html', context)
    else:
        utype = "Patient"
        user = Patient.objects.get(username=uname)
        pres = Prescription.objects.filter(patient=p)
        context = {'user': user,
                    'prescriptions': pres,
                   'type': utype,
                   'patient': p}
        return render(request, 'MDTouch/prescriptions.html', context)


# This module simply renders the HTML page for the create prescription screen.
def createPres(request):
    patients = Patient.objects.order_by("-lastName")
    context = {'patients': patients}
    return render(request, 'MDTouch/createPres.html', context)


# This module handles creating a database object for a prescription after retrieving POST data from the form submission.
#  After the object is created and saved, the user is redirected to the prescriptions screen.
def createPresInfo(request):
    #global uname
    uname = request.session['uname']
    name = (request.POST['name'])
    dosage = (request.POST['dosage'])
    patient = Patient.objects.get(id=(request.POST['patient']))
    doctor = Doctor.objects.get(username=uname)
    pre = Prescription.objects.create()
    pre.name = name
    pre.dosage = dosage
    pre.doctor = doctor
    pre.patient = patient
    pre.save()
    #activity = "Doctor " + doctor.username + " created a prescription for Patient " + patient.username +\
    #           " - logged on: " + datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    #logActivity(activity)
    return HttpResponseRedirect(reverse('MDTouch:prescriptions', args=()))


# This module simply renders the HTML page for the update prescriptions screen.
def updatePres(request, pres_id):
    p = Prescription.objects.get(id=pres_id)
    patients = Patient.objects.order_by("-lastName")
    context = {'patients': patients,
               'prescription': p}
    return render(request, 'MDTouch/updatePres.html', context)


# This module handles modifying the database object after retrieving POST data from the form submission.
# After the object is updated and saved, the doctor is redirected to their prescriptions screen.
def updatePresInfo(request, pres_id):
    uname = request.session['uname']
    name = (request.POST['name'])
    dosage = (request.POST['dosage'])
    patient = Patient.objects.get(id=(request.POST['patient']))
    doctor = Doctor.objects.get(username=uname)
    pre = Prescription.objects.get(id=pres_id)
    pre.name = name
    pre.dosage = dosage
    pre.doctor = doctor
    pre.patient = patient
    pre.save()
    #activity = "Doctor " + doctor.username + " updated Prescription #" + pres_id + " for Patient " + patient.username +\
    #           " - logged on: " + datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    #logActivity(activity)
    return HttpResponseRedirect(reverse('MDTouch:prescriptions', args=()))


# This module handles deleting the database object for a prescription. Afterwards, the doctor is redirected to
# their prescriptions screen.
def removePres(request, pres_id):
    uname = request.session['uname']
    Prescription.objects.get(id=pres_id).delete()
    #activity = "Doctor " + uname + " removed Prescription #" + pres_id + " - logged on: " +\
    #           datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    #logActivity(activity)
    return HttpResponseRedirect(reverse('MDTouch:prescriptions', args=()))


# This module simply renders the HTML page for the calendar screen.
def calendar(request):
    #global uname
    uname = request.session['uname']
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                return render(request, 'MDTouch/home.html', {
                    'error_message': "An error has occurred"
                })
            else:
                utype = "Nurse"
                # Nurses can view all appointments for the day and week between patients and doctors, in their workplace
                appts = Appointment.objects.filter(location=n.workplace)
                context = {'appointments': appts,
                           'user': n,
                           'type': utype}
                return render(request, 'MDTouch/calendar.html', context)
        else:
            utype = "Doctor"
            # Doctors can view all of their appointments on the calendar
            appts = Appointment.objects.filter(doctor=d)
            context = {'appointments': appts,
                           'user': d,
                           'type': utype}
            return render(request, 'MDTouch/calendar.html', context)
    else:
        utype = "Patient"
        # Patients can view all of their appointments on the calendar
        appts = Appointment.objects.filter(patient=p)
        context = {'appointments': appts,
                           'user': p,
                           'type': utype}
        return render(request, 'MDTouch/calendar.html', context)


# This module simply renders the activity log for an administrator account
def log(request):
    filename = "log.txt"
    cwd = os.getcwd()
    target = open(cwd + "\\MDTouch\\log\\" + filename, 'r')
    appString = target.readline()
    logString = []
    while appString != "":
        logString.append(appString)
        appString = target.readline()
    target.close()
    context = {'logString': logString}
    return render(request, 'MDTouch/log.html', context)


# This module simply renders the statistics page for an administrator account
def statistics(request):
    admins = Administrator.objects.count()
    doctors = Doctor.objects.count()
    nurses = Nurse.objects.count()
    patients = Patient.objects.count()
    appts = Appointment.objects.count()
    pres = Prescription.objects.count()
    context = {'admins': admins,
               'doctors': doctors,
               'nurses': nurses,
               'patients': patients,
               'appointments': appts,
               'prescriptions': pres}
    return render(request, 'MDTouch/statistics.html', context)


# This module simply renders the main messaging page for a user. All of their received and sent message are displayed
# on the page, with various options for the user to choose from.
def messages(request):
    #global uname
    uname = request.session['uname']
    try:
        m = Message.objects.filter(receiverDelete=False)
        mess = m.filter(receiverName=uname)
    except Message.DoesNotExist:
        mess = Null
    try:
        sm = Message.objects.filter(senderDelete=False)
        sendmess = sm.filter(senderName=uname)
    except Message.DoesNotExist:
        sendmess = Null
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                utype = "Administrator"
            else:
                utype = "Nurse"
        else:
            utype = "Doctor"
    else:
        utype = "Patient"
    user = Patient.objects.get(username = uname)
    context = {
                'user' : user,
                'messages': mess,
               'type': utype,
               'sendMessages': sendmess}
    return render(request, 'MDTouch/messages.html', context)


# This module simply renders the create message page for a user.
def createMess(request):
    #global uname
    uname = request.session['uname']
    logins = LogInInfo.objects.all()
    context = {'logins': logins}
    return render(request, 'MDTouch/createMess.html', context)


# This module simply renders the reply message page for a user.
def replyMess(request, mess_id):
    #global uname
    uname = request.session['uname']
    logins = LogInInfo.objects.all()
    context = {'logins': logins,
               'message': Message.objects.get(id=mess_id)}
    return render(request, 'MDTouch/replyMess.html', context)


# This module handles creating a database object for a message after retrieving POST data from the form submission.
# After the object is created and saved, the user is redirected to the main messages page.
def createMessInfo(request, mess_id):
    #global uname
    uname = request.session['uname']
    subject = (request.POST['subject'])
    description = (request.POST['message'])
    m = Message.objects.create()
    if mess_id != "-1":
        replyMess = Message.objects.get(id=mess_id)
        if replyMess.senderName == uname:
            m.receiverName = replyMess.receiverName
            m.subjectLine = "RE - " + subject
        else:
            m.receiverName = replyMess.senderName
            m.subjectLine = "RE - " + subject
    else:
        username = LogInInfo.objects.get(id=(request.POST['users'])).username
        m.receiverName = username
        m.subjectLine = subject
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                try:
                    a = Administrator.objects.get(username=uname)
                except Administrator.DoesNotExist:
                    return render(request, 'MDTouch/home.html', {
                        'error_message': "An error has occurred"
                        })
                else:
                    utype = "Administrator"
            else:
                utype = "Nurse"
        else:
            utype = "Doctor"
    else:
        utype = "Patient"
    m.senderName = uname
    m.senderType = utype
    m.date = date.today()
    m.message = description
    m.save()
    #activity = utype + " " + uname + " sent a message to " + m.receiverName + " - logged on: " + \
    #           datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    #logActivity(activity)
    return messages(request)


# This module simply displays the View Message page for a user when they select the option to view a received/sent
# message.
def viewMess(request, mess_id):
    #global uname
    uname = request.session['uname']
    mess = Message.objects.get(id=mess_id)
    context = {'message': mess}
    return render(request, 'MDTouch/viewMess.html', context)


# This module handles deleting a preexisting message from a user's inbox.
def deleteMess(request, mess_id):
    global uname
    mess = Message.objects.get(id=mess_id)
    if uname == mess.senderName:
        mess.senderDelete = True
        mess.save()
    else:
        mess.receiverDelete = True
        mess.save()

    if mess.senderDelete is True and mess.receiverDelete is True:
        mess.delete()

    #activity = uname + " deleted message# " + mess_id + " - logged on: " + \
     #          datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    #logActivity(activity)
    return HttpResponseRedirect(reverse('MDTouch:messages', args=()))


# This module handles logging-out a user. Afterwards the user is redirected to the index screen.
def logOut(request):
    #global uname
    uname = request.session['uname']
    #activity = "User " + uname + " logged out - logged on: " + datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    request.session['uname'] = ''
    #logActivity(activity)
    return HttpResponseRedirect(reverse('MDTouch:index', args=()))
from .models import Event
def getevents(request):
    uname = request.session['uname']
    patient = Patient.objects.get(username = uname)
    events = Event.objects.all()
    context = {'events':events,'user':patient}
    return render(request,'MDTouch/events.html',context)

##############################################################################################################
##############################################################################################################
################################           API and Calls              ########################################
##############################################################################################################
##############################################################################################################

from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import status

@csrf_exempt
def hospital_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        hospital = Hospital.objects.all()
        hospital = HospitalSerializer(hospital, many=True)
        return JsonResponse(hospital.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        hospital = HospitalSerializer(data=data)
        if hospital.is_valid():
            hospital.save()
            return JsonResponse(hospital.data, status=201)
        return JsonResponse(hospital.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def hospital_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        album = Hospital.objects.get(pk=pk)
    except Hospital.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = HospitalSerializer(album)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = HospitalSerializer(album, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        album.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def emergencycontact_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        emergencycontact = EmergencyContact.objects.all()
        emergencycontact = EmergencyContactSerializer(emergencycontact, many=True)
        return JsonResponse(emergencycontact.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        emergencycontact = EmergencyContactSerializer(data=data)
        if emergencycontact.is_valid():
            emergencycontact.save()
            return JsonResponse(emergencycontact.data, status=201)
        return JsonResponse(emergencycontact.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def emergencycontact_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        emergencycontact = EmergencyContact.objects.get(pk=pk)
    except EmergencyContact.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EmergencyContactSerializer(emergencycontact)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EmergencyContactSerializer(emergencycontact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        emergencycontact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def patient_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        patient = Patient.objects.all()
        patient = PatientSerializer(patient, many=True)
        return JsonResponse(patient.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        patient = PatientSerializer(data=data)
        if patient.is_valid():
            patient.save()
            return JsonResponse(patient.data, status=201)
        return JsonResponse(patient.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def patient_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        patient = Patient.objects.get(pk=pk)
    except EmergencyContact.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PatientSerializer(patient)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def specialization_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        specialization = Specialization.objects.all()
        specialization = SpecializationSerializer(patient, many=True)
        return JsonResponse(specialization.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        specialization = SpecializationSerializer(data=data)
        if specialization.is_valid():
            specialization.save()
            return JsonResponse(specialization.data, status=201)
        return JsonResponse(specialization.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def specialization_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        specialization = Specialization.objects.get(pk=pk)
    except Specialization.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SpecializationSerializer(specialization)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SpecializationSerializer(specialization, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        specialization.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def qualification_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        qualification = Qualification.objects.all()
        qualification = QualificationSerializer(qualification, many=True)
        return JsonResponse(qualification.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        qualification = QualificationSerializer(data=data)
        if qualification.is_valid():
            qualification.save()
            return JsonResponse(qualification.data, status=201)
        return JsonResponse(qualification.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def qualification_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        qualification = Qualification.objects.get(pk=pk)
    except EmergencyContact.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = QualificationSerializer(qualification)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = QualificationSerializer(qualification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        qualification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def doctor_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        doctor = Doctor.objects.all()
        doctor = DoctorSerializer(doctor, many=True)
        return JsonResponse(doctor.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        doctor = DoctorSerializer(data=data)
        if doctor.is_valid():
            doctor.save()
            return JsonResponse(doctor.data, status=201)
        return JsonResponse(doctor.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def doctor_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        doctor = Doctor.objects.get(pk=pk)
    except Doctor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DoctorSerializer(doctor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        doctor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def administrator_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        administrator = Administrator.objects.all()
        administrator = AdministratorSerializer(administrator, many=True)
        return JsonResponse(administrator.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        administrator = AdministratorSerializer(data=data)
        if administrator.is_valid():
            administrator.save()
            return JsonResponse(administrator.data, status=201)
        return JsonResponse(administrator.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def administrator_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        administrator = Administrator.objects.get(pk=pk)
    except Administrator.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AdministratorSerializer(administrator)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AdministratorSerializer(administrator, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        administrator.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def prescription_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        prescription = Prescription.objects.all()
        prescription = PrescriptionSerializer(prescription, many=True)
        return JsonResponse(prescription.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        prescription = PrescriptionSerializer(data=data)
        if prescription.is_valid():
            prescription.save()
            return JsonResponse(prescription.data, status=201)
        return JsonResponse(prescription.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def prescription_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        prescription = Prescription.objects.get(pk=pk)
    except Prescription.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PrescriptionSerializer(prescription)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PrescriptionSerializer(prescription, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        prescription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def test_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        test = Test.objects.all()
        test = TestSerializer(test, many=True)
        return JsonResponse(test.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        test = PrescriptionSerializer(data=data)
        if test.is_valid():
            test.save()
            return JsonResponse(test.data, status=201)
        return JsonResponse(test.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def test_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        test = Test.objects.get(pk=pk)
    except Test.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TestSerializer(test)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TestSerializer(test, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        test.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def appointment_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        appointment = Appointment.objects.all()
        appointment = AppointmentSerializer(appointment, many=True)
        return JsonResponse(appointment.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        appointment = AppointmentSerializer(data=data)
        if appointment.is_valid():
            appointment.save()
            return JsonResponse(appointment.data, status=201)
        return JsonResponse(appointment.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def appointment_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        appointment = Appointment.objects.get(pk=pk)
    except Appointment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AppointmentSerializer(appointment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def message_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        message = Message.objects.all()
        message = MessageSerializer(message, many=True)
        return JsonResponse(message.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        message = MessageSerializer(data=data)
        if message.is_valid():
            message.save()
            return JsonResponse(message.data, status=201)
        return JsonResponse(message.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def message_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        message = Message.objects.get(pk=pk)
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MessageSerializer(message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def logininfo_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        logininfo = LogInInfo.objects.all()
        logininfo = LoginInInfoSerializer(logininfo, many=True)
        return JsonResponse(logininfo.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        logininfo = LoginInInfoSerializer(data=data)
        if logininfo.is_valid():
            logininfo.save()
            return JsonResponse(logininfo.data, status=201)
        return JsonResponse(logininfo.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def logininfo_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        logininfo = LogInInfo.objects.get(pk=pk)
    except LogInInfo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LoginInInfoSerializer(logininfo)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = LoginInInfoSerializer(logininfo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        logininfo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def emergencyservices_list(request):
    """
    List all code snisppets, or create a new snippet.
    """
    if request.method == 'GET':
        emergencyservices = EmergencyService.objects.all()
        emergencyservices = EmergencyServiceSerializer(emergencyservices, many=True)
        return JsonResponse(emergencyservices.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        emergencyservices = EmergencyServiceSerializer(data=data)
        if emergencyservices.is_valid():
            emergencyservices.save()
            return JsonResponse(emergencyservices.data, status=201)
        return JsonResponse(emergencyservices.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def emergencyservices_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        emergencyservices = EmergencyService.objects.get(pk=pk)
    except EmergencyService.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EmergencyServiceSerializer(emergencyservices)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EmergencyServiceSerializer(emergencyservices, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        emergencyservices.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def ambulance_list(request):
    """
    List all code snisppets, or create a new snippet.
    """
    if request.method == 'GET':
        ambulance = Ambulance.objects.all()
        ambulance = AmbulanceSerializer(ambulance, many=True)
        return JsonResponse(ambulance.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        ambulance = AmbulanceSerializer(data=data)
        if ambulance.is_valid():
            ambulance.save()
            return JsonResponse(ambulance.data, status=201)
        return JsonResponse(ambulance.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def ambulance_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        ambulance = Ambulance.objects.get(pk=pk)
    except Ambulance.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AmbulanceSerializer(ambulance)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AmbulanceSerializer(ambulance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        ambulance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def login_list(request):
    """
    List all code snisppets, or create a new snippet.
    """
    if request.method == 'GET':
        login = Login.objects.all()
        login = LoginSerilizer(login, many=True)
        return JsonResponse(login.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        login = LoginSerilizer(data=data)
        if login.is_valid():
            login.save()
            return JsonResponse(login.data, status=201)
        return JsonResponse(login.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def login_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        login = Login.objects.get(pk=pk)
    except Login.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LoginSerilizer(login)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = LoginSerilizer(login, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        login.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def bloodbankcenter_list(request):
    """
    List all code snisppets, or create a new snippet.
    """
    if request.method == 'GET':
        bloodbankcenter = BloodBankCenter.objects.all()
        bloodbankcenter = BloodBankCenterSerializer(bloodbankcenter, many=True)
        return JsonResponse(bloodbankcenter.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        bloodbankcenter = BloodBankCenterSerializer(data=data)
        if bloodbankcenter.is_valid():
            bloodbankcenter.save()
            return JsonResponse(bloodbankcenter.data, status=201)
        return JsonResponse(bloodbankcenter.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def bloodbankcenter_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        bloodbankcenter = BloodBankCenter.objects.get(pk=pk)
    except BloodBankCenter.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BloodBankCenterSerializer(bloodbankcenter)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BloodBankCenterSerializer(bloodbankcenter, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        bloodbankcenter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def dispensaries_list(request):
    """
    List all code snisppets, or create a new snippet.
    """
    if request.method == 'GET':
        dispensaries = Dispensaries.objects.all()
        dispensaries = DispensariesSerializer(dispensaries, many=True)
        return JsonResponse(dispensaries.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        dispensaries = DispensariesSerializer(data=data)
        if dispensaries.is_valid():
            dispensaries.save()
            return JsonResponse(dispensaries.data, status=201)
        return JsonResponse(dispensaries.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def dispensaries_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        dispensaries = Dispensaries.objects.get(pk=pk)
    except Dispensaries.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DispensariesSerializer(dispensaries)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DispensariesSerializer(dispensaries, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        dispensaries.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def event_list(request):
    """
    List all code snisppets, or create a new snippet.
    """
    if request.method == 'GET':
        event = Event.objects.all()
        event = EventSerializer(event, many=True)
        return JsonResponse(event.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        event = EventSerializer(data=data)
        if event.is_valid():
            event.save()
            return JsonResponse(event.data, status=201)
        return JsonResponse(event.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def event_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def bloodbilling_list(request):
    """
    List all code snisppets, or create a new snippet.
    """
    if request.method == 'GET':
        bloodbilling = BloodBilling.objects.all()
        bloodbilling = BloodBillingSerializer(bloodbilling, many=True)
        return JsonResponse(bloodbilling.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        bloodbilling = BloodBillingSerializer(data=data)
        if bloodbilling.is_valid():
            bloodbilling.save()
            return JsonResponse(bloodbilling.data, status=201)
        return JsonResponse(bloodbilling.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def bloodbilling_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        bloodbilling = BloodBilling.objects.get(pk=pk)
    except BloodBilling.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BloodBillingSerializer(bloodbilling)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BloodBillingSerializer(bloodbilling, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        bloodbilling.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def bloodwaste_list(request):
    """
    List all code snisppets, or create a new snippet.
    """
    if request.method == 'GET':
        bloodwaste = BloodWaste.objects.all()
        bloodwaste = BloodWasteSerializer(bloodwaste, many=True)
        return JsonResponse(bloodwaste.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        bloodwaste = BloodWasteSerializer(data=data)
        if bloodwaste.is_valid():
            bloodwaste.save()
            return JsonResponse(bloodwaste.data, status=201)
        return JsonResponse(bloodwaste.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def bloodwaste_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        bloodwaste = BloodWaste.objects.get(pk=pk)
    except BloodWaste.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BloodWasteSerializer(bloodwaste)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BloodWasteSerializer(bloodwaste, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        bloodwaste.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def medicine_list(request):
    """
    List all code snisppets, or create a new snippet.
    """
    if request.method == 'GET':
        medicine = Medicine.objects.all()
        medicine = MedicineSerializer(medicine, many=True)
        return JsonResponse(medicine.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        medicine = MedicineSerializer(data=data)
        if medicine.is_valid():
            medicine.save()
            return JsonResponse(medicine.data, status=201)
        return JsonResponse(medicine.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def medicine_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        medicine = Medicine.objects.get(pk=pk)
    except Medicine.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MedicineSerializer(medicine)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MedicineSerializer(medicine, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        medicine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def dispensarybilling_list(request):
    """
    List all code snisppets, or create a new snippet.
    """
    if request.method == 'GET':
        dispensarybilling = DispensaryBilling.objects.all()
        dispensarybilling = DispensaryBillingSerializer(dispensarybilling, many=True)
        return JsonResponse(dispensarybilling.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        dispensarybilling = DispensaryBillingSerializer(data=data)
        if dispensarybilling.is_valid():
            dispensarybilling.save()
            return JsonResponse(dispensarybilling.data, status=201)
        return JsonResponse(dispensarybilling.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def dispensarybilling_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        dispensarybilling = DispensaryBilling.objects.get(pk=pk)
    except DispensaryBilling.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DispensaryBillingSerializer(dispensarybilling)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DispensaryBillingSerializer(dispensarybilling, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        dispensarybilling.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def ambulancebilling_list(request):
    """
    List all code snisppets, or create a new snippet.
    """
    if request.method == 'GET':
        ambulancebilling = AmbulanceBilling.objects.all()
        ambulancebilling = AmbulanceBillingSerializer(ambulancebilling, many=True)
        return JsonResponse(ambulancebilling.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        ambulancebilling = AmbulanceBillingSerializer(data=data)
        if ambulancebilling.is_valid():
            ambulancebilling.save()
            return JsonResponse(ambulancebilling.data, status=201)
        return JsonResponse(ambulancebilling.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def ambulancebilling_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        ambulancebilling = AmbulanceBilling.objects.get(pk=pk)
    except AmbulanceBilling.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AmbulanceBillingSerializer(ambulancebilling)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AmbulanceBillingSerializer(ambulancebilling, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        ambulancebilling.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def testservices_list(request):
    """
    List all code snisppets, or create a new snippet.
    """
    if request.method == 'GET':
        testservices = TestServices.objects.all()
        testservices = TestServicesSerializer(testservices, many=True)
        return JsonResponse(testservices.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        testservices = TestServicesSerializer(data=data)
        if testservices.is_valid():
            testservices.save()
            return JsonResponse(testservices.data, status=201)
        return JsonResponse(testservices.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def testservices_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        testservices = TestServices.objects.get(pk=pk)
    except TestServices.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TestServicesSerializer(testservices)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AmbulanceBillingSerializer(testservices, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        testservices.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def testcentre_list(request):
    """
    List all code snisppets, or create a new snippet.
    """
    if request.method == 'GET':
        testcentre = TestCentre.objects.all()
        testcentre = TestCentreSerializer(testcentre, many=True)
        return JsonResponse(testcentre.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        testcentre = TestCentreSerializer(data=data)
        if testcentre.is_valid():
            testcentre.save()
            return JsonResponse(testcentre.data, status=201)
        return JsonResponse(testcentre.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def testcentre_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        testcentre = TestCentre.objects.get(pk=pk)
    except TestCentre.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TestCentreSerializer(testcentre)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TestCentreSerializer(testcentre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        testcentre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def notice_list(request):
    """
    List all code snisppets, or create a new snippet.
    """
    if request.method == 'GET':
        notice = Notice.objects.all()
        notice = NoticeSerializer(notice, many=True)
        return JsonResponse(notice.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        notice = NoticeSerializer(data=data)
        if notice.is_valid():
            notice.save()
            return JsonResponse(notice.data, status=201)
        return JsonResponse(notice.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def notice_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        notice = Notice.objects.get(pk=pk)
    except Notice.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = NoticeSerializer(notice)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = NoticeSerializer(notice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        notice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def webcarousel_list(request):
    """
    List all code snisppets, or create a new snippet.
    """
    if request.method == 'GET':
        webcarousel = WebCarousel.objects.all()
        webcarousel = WebCarouselSerializer(webcarousel, many=True)
        return JsonResponse(webcarousel.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        webcarousel = WebCarouselSerializer(data=data)
        if webcarousel.is_valid():
            webcarousel.save()
            return JsonResponse(webcarousel.data, status=201)
        return JsonResponse(webcarousel.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def webcarousel_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        webcarousel = WebCarousel.objects.get(pk=pk)
    except WebCarousel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = WebCarouselSerializer(webcarousel)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = WebCarouselSerializer(webcarousel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        webcarousel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
