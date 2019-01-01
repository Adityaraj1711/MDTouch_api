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

def aboutpage(request):
    return render(request,'MDTouch/about.html')

def eventpage(request):
    events = Event.objects.all()
    context = {'events':events}
    return render(request,'MDTouch/event.html',context)

def eventdetailview(request,event_id):
    event = Event.objects.get(id = event_id)
    context = {'event':event}
    return render(request,'MDTouch/eventdetail.html',context)

def servicepage(request):
    return render(request,'MDTouch/services.html')

# This module simply renders the HTML page for the registration screen.
def registerP(request):
    return render(request, 'MDTouch/registerP.html')


# This module handles the user registration. The "LogInInfo" object is used to store their credentials in the database.
def createPLogIn(request):
    firstName = (request.POST.get('firstName'))
    lastName = (request.POST.get('lastName'))
    address = (request.POST.get('address'))
    number = (request.POST.get('number'))
    email = (request.POST.get('email'))
    provider = (request.POST.get('provider'))
    insuranceid = (request.POST.get('insuranceid'))
    contactfname = (request.POST.get('contactfname'))
    contactlname = (request.POST.get('contactlname'))
    contactaddress = (request.POST.get('contactaddress'))
    contactnumber = (request.POST.get('contactnumber'))
    height = (request.POST.get('height'))
    weight = (request.POST.get('weight'))
    allergies = (request.POST.get('allergies'))
    gender = (request.POST.get('gender'))
    username = request.POST.get('username')
    password = (request.POST.get('password'))
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
from django_filters.rest_framework import DjangoFilterBackend,OrderingFilter
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import status,filters
import django_filters

class HospitalList(generics.ListCreateAPIView):
    serializer_class = HospitalSerializer
    queryset = Hospital.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter)
    filter_fields = '__all__'
    ordering_fields = '__all__'

class HospitalDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer


class EmergencycontactList(generics.ListCreateAPIView):
    serializer_class = EmergencyContactSerializer
    queryset = EmergencyContact.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'
    ordering_fields = '__all__'

class EmergencycontactDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmergencyContact.objects.all()
    serializer_class = EmergencyContactSerializer

class PatientList(generics.ListCreateAPIView):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter)
    filter_fields = '__all__'
    search_fields = ('firstName','lastName','id','pin')
    ordering_fields = '__all__'


class PatientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class SpecializationList(generics.ListCreateAPIView):
    serializer_class = SpecializationSerializer
    queryset = Specialization.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'
    ordering_fields = '__all__'


class SpecializationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer

class QualificationList(generics.ListCreateAPIView):
    serializer_class = QualificationSerializer
    queryset = Qualification.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'
    ordering_fields = '__all__'


class QualificationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer

class DoctorList(generics.ListCreateAPIView):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter)
    filter_fields = '__all__'
    ordering_fields = '__all__'



class DoctorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class AdministratorList(generics.ListCreateAPIView):
    serializer_class = AdministratorSerializer
    queryset = Administrator.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'
    ordering_fields = '__all__'


class AdministratorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Administrator.objects.all()
    serializer_class = SpecializationSerializer

class PrescriptionList(generics.ListCreateAPIView):
    serializer_class = PrescriptionSerializer
    queryset = Prescription.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'
    ordering_fields = '__all__'


class PrescriptionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer


class TestFilter(django_filters.rest_framework.FilterSet):
    date = django_filters.DateFromToRangeFilter(field_name="date",lookup_expr='gt')

    class Meta:
        model = Test
        fields = [
            'date',
        ]


class TestList(generics.ListCreateAPIView):
    serializer_class = TestSerializer
    queryset = Test.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'
    #filter_class = TestFilter
    ordering_fields = '__all__'

class TestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class AppointmentFilter(django_filters.rest_framework.FilterSet):
    appointmentdate = django_filters.DateFromToRangeFilter(field_name="appointmentdate",lookup_expr='gt')
    dateofrequest = django_filters.DateFromToRangeFilter(field_name="dateofrequest",lookup_expr='gt')
    class Meta:
        model = Appointment
        fields = [
            'appointmentdate','dateofrequest'
        ]


class AppointmentList(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'
    #filter_class = AppointmentFilter
    ordering_fields = '__all__'

class AppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class MessageFilter(django_filters.rest_framework.FilterSet):
    date = django_filters.DateFromToRangeFilter(field_name="date",lookup_expr='gt')

    class Meta:
        model = Message
        fields = [
            'date',
        ]


class MessageList(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'
    #filter_class = MessageFilter
    ordering_fields = '__all__'

class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class LogInInfoList(generics.ListCreateAPIView):
    serializer_class = LoginInInfoSerializer
    queryset = LogInInfo.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'
    ordering_fields = '__all__'


class LogInInfoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LogInInfo.objects.all()
    serializer_class = LoginInInfoSerializer

class EmergencyServicesList(generics.ListCreateAPIView):
    serializer_class = EmergencyServiceSerializer
    queryset = EmergencyService.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'
    ordering_fields = '__all__'

class EmergencyServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmergencyService.objects.all()
    serializer_class = EmergencyServiceSerializer

class AmbulanceList(generics.ListCreateAPIView):
    serializer_class = AmbulanceSerializer
    queryset = Ambulance.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'
    ordering_fields = '__all__'


class AmbulanceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ambulance.objects.all()
    serializer_class = AmbulanceSerializer

class LoginList(generics.ListCreateAPIView):
    serializer_class = LoginSerilizer
    queryset = Login.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'
    ordering_fields = '__all__'


class LoginDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Login.objects.all()
    serializer_class = LoginSerilizer

class BloodBankCenterList(generics.ListCreateAPIView):
    serializer_class = BloodBankCenterSerializer
    queryset = BloodBankCenter.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'
    ordering_fields = '__all__'


class BloodBankCenterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BloodBankCenter.objects.all()
    serializer_class = BloodBankCenterSerializer

class DispensaryList(generics.ListCreateAPIView):
    serializer_class = DispensariesSerializer
    queryset = Dispensaries.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'
    ordering_fields = '__all__'

class DispensaryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dispensaries.objects.all()
    serializer_class = DispensariesSerializer

class EventFilter(django_filters.rest_framework.FilterSet):
    dateofevent = django_filters.DateFromToRangeFilter(field_name="dateofevent",lookup_expr='gt')
    dateofcreation = django_filters.DateFromToRangeFilter(field_name="dateofcreation",lookup_expr='gt')
    class Meta:
        model = Event
        #filter_fields = '__all__'
        fields = [
            'dateofevent','dateofcreation'
        ]

class EventList(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'
    ##filter_class = EventFilter
    ordering_fields = '__all__'

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class BloodBillingFilter(django_filters.rest_framework.FilterSet):
    date = django_filters.DateFromToRangeFilter(field_name="date",lookup_expr='gt')

    class Meta:
        model = BloodBilling
        fields = [
            'date',
        ]

class BloodBillingList(generics.ListCreateAPIView):
    queryset = BloodBilling.objects.all()
    serializer_class = BloodBillingSerializer
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'
    ##filter_class = BloodBillingFilter
    ordering_fields = '__all__'

class BloodBillingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BloodBilling.objects.all()
    serializer_class = BloodBillingSerializer

class AmbulanceBillingFilter(django_filters.rest_framework.FilterSet):
    datetime = django_filters.DateFromToRangeFilter(field_name="date",lookup_expr='gt')
    class Meta:
        model = AmbulanceBilling
        fields = [
            'datetime',
        ]

class AmbulanceBillingList(generics.ListCreateAPIView):
    serializer_class = AmbulanceBillingSerializer
    queryset = AmbulanceBilling.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'
    #filter_class = AmbulanceBillingFilter
    ordering_fields = '__all__'

class AmbulanceBillingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AmbulanceBilling.objects.all()
    serializer_class = AmbulanceBillingSerializer

class BloodWasteFilter(django_filters.rest_framework.FilterSet):
    date = django_filters.DateFromToRangeFilter(field_name="date",lookup_expr='gt')
    class Meta:
        model = BloodWaste
        fields = [
            'date',
        ]

class BloodWasteList(generics.ListCreateAPIView):
    serializer_class = BloodWasteSerializer
    queryset = BloodWaste.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'
    #filter_class = BloodWasteFilter
    ordering_fields = '__all__'

class BloodWasteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BloodWaste.objects.all()
    serializer_class = BloodWasteSerializer

class MedicineFilter(django_filters.rest_framework.FilterSet):
    manufacturedate = django_filters.DateFromToRangeFilter(field_name="manufacturedate",lookup_expr='gt')
    expirydate = django_filters.DateFromToRangeFilter(field_name="expirydate",lookup_expr='gt')

    class Meta:
        model = Medicine
        fields = [
            'manufacturedate','expirydate',
        ]

class MedicineList(generics.ListCreateAPIView):
    serializer_class = MedicineSerializer
    queryset = Medicine.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'
    #filter_class = MedicineFilter
    ordering_fields = '__all__'

class MedicineDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

class DispensaryBillingFilter(django_filters.rest_framework.FilterSet):
    date = django_filters.DateFromToRangeFilter(field_name="date",lookup_expr='gt')

    class Meta:
        model = DispensaryBilling
        fields = [
            'date',
        ]

class DispensaryBillingList(generics.ListCreateAPIView):
    serializer_class = DispensariesSerializer
    queryset = Dispensaries.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'
    #filter_class = DispensaryBillingFilter
    ordering_fields = '__all__'

class DispensaryBillingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dispensaries.objects.all()
    serializer_class = DispensariesSerializer


class TestServicesList(generics.ListCreateAPIView):
    serializer_class = TestServicesSerializer
    queryset = TestServices.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'

class TestServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestServices.objects.all()
    serializer_class = TestServicesSerializer

class TestCentreList(generics.ListCreateAPIView):
    serializer_class = TestCentreSerializer
    queryset = TestCentre.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'
    ordering_fields = '__all__'

class TestCentreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestCentre.objects.all()
    serializer_class = TestCentreSerializer

class NoticeFilter(django_filters.rest_framework.FilterSet):
    date = django_filters.DateFromToRangeFilter(field_name="date",lookup_expr='gt')
    class Meta:
        model = Notice
        fields = [
            'date',
        ]

class NoticeList(generics.ListCreateAPIView):
    serializer_class = NoticeSerializer
    queryset = Notice.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'
    #filter_class = NoticeFilter
    ordering_fields = '__all__'

class NoticeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

class BroadcastFilter(django_filters.rest_framework.FilterSet):
    date = django_filters.DateFromToRangeFilter(field_name="date",lookup_expr='gt')
    class Meta:
        model = Broadcast
        fields = [
            'date',
        ]


class BroadcastList(generics.ListCreateAPIView):
    serializer_class = BroadcastSerializer
    queryset = Broadcast.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'
    #filter_class = BroadcastFilter
    ordering_fields = '__all__'

class BroadcastDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Broadcast.objects.all()
    serializer_class = BroadcastSerializer


class AmbulanceRequestList(generics.ListCreateAPIView):
    serializer_class = AmbulanceRequestSerializer
    queryset = AmbulanceRequest.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'
    ordering_fields = '__all__'

class AmbulanceRequestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AmbulanceRequest.objects.all()
    serializer_class = AmbulanceRequestSerializer

class BedList(generics.ListCreateAPIView):
    serializer_class = BedSerializer
    queryset = Bed.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'
    ordering_fields = '__all__'

class BedDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bed.objects.all()
    serializer_class = BedSerializer

class BedBillingtList(generics.ListCreateAPIView):
    serializer_class = BedBillingSerializer
    queryset = BedBilling.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'
    ordering_fields = '__all__'

class BedBillingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BedBilling.objects.all()
    serializer_class = BedBillingSerializer

class MaintainenceBedList(generics.ListCreateAPIView):
    serializer_class = MaintainenceBedSerializer
    queryset = MaintainenceBed.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'
    ordering_fields = '__all__'

class MaintainenceBedDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MaintainenceBed.objects.all()
    serializer_class = MaintainenceBedSerializer

class HospitalBillingList(generics.ListCreateAPIView):
    serializer_class = HospitalBillingSerializer
    queryset = HospitalBilling.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = '__all__'
    ordering_fields = '__all__'

class HospitalBillingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = HospitalBilling.objects.all()
    serializer_class = HospitalBillingSerializer

class HospitalFacilitiesList(generics.ListCreateAPIView):
    serializer_class = HospitalFacilitiesSerializer
    queryset = HospitalFacilities.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter,)
    filter_fields = '__all__'
    ordering_fields = '__all__'
    search_fields = ('facilities',)

class HospitalFacilitiesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = HospitalFacilities.objects.all()
    serializer_class = HospitalFacilitiesSerializer

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

###################################################################################################################
#############################
############################################3
from django.db.models import Q
def search(request):
    query = request.GET.get('q')
    if query is not None:
        result = HospitalFacilities.objects.filter(Q(facilities__icontains=query))
        print(result,"sfdgfhffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        context = {
            'items' : result,
        }
        return render(request,'MDTouch/search-form.html',context)
    else:
        return render(request, 'MDTouch/search-form.html')