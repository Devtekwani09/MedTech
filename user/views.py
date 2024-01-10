from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from project import settings
from django.core.mail import send_mail
import joblib
import sklearn
from .models import doctor
from math import ceil
from django.shortcuts import render, get_object_or_404


# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        Email = request.POST['Email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if User.objects.filter(username = username):
            messages.error(request, "Username already exist! Try using differnt username")

        if User.objects.filter(email = Email):
            messages.error(request, "Email already registered! Try using differnt username")

        if len(username)>10:
            messages.error(request, "Username can not exceed 10 letters")

        if (password != confirm_password):
            messages.error(request, "Password does not match confirm password")
        myuser = User.objects.create_user(username, Email, password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.confirm_password = confirm_password

        myuser.save()

        messages.success(request, "Your Account has been created successfully.")


        #welcome email

        # subject = "Welcome to MedTech - Service at your phone"
        # message = "Hello" + myuser.first_name + "!! \n Thank you for visiting our website \n We have also sent you a confirmaton email, Please confirm your email for using our services. \n\n Thanks and Regards \n Team Medtech"
        # from_email = settings.EMAIL_HOST_USER
        # to_list = [myuser.email]
        # send_mail(subject, message, from_email, to_list, fail_silently=True )

        return redirect('signin')




    return render(request, "authentication/signup.html")

def signin(request):
    if request.method == "POST":
        user = request.POST['username']
        pass1 = request.POST['password']

        user = authenticate(username = user, password = pass1)


        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname': fname})

        else:
            messages.error(request, "Wrong Username Or Password")
            return redirect('home')

    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')

def doctors(request):
    doc = doctor.objects.all()
    print(doc)
    # n = len(doc) 
    # params = {'no_of_slides' : nslides, 'range' : range(nslides),'doctor' : doc}
    # nslides = n // 3 + ceil((n/3)-(n//3))
    return render(request, "authentication/doctors.html", {'doctors':doc})

all_symptoms = [
            'itching','skin_rash','nodal_skin_eruptions','continuous_sneezing','shivering','chills','joint_pain',
            'stomach_pain','acidity','ulcers_on_tongue','muscle_wasting','vomiting','burning_micturition','spotting_ urination','fatigue',
            'weight_gain','anxiety','cold_hands_and_feets','mood_swings','weight_loss','restlessness','lethargy','patches_in_throat',
            'irregular_sugar_level','cough','high_fever','sunken_eyes','breathlessness','sweating','dehydration','indigestion',
            'headache','yellowish_skin','dark_urine','nausea','loss_of_appetite','pain_behind_the_eyes','back_pain','constipation',
            'abdominal_pain','diarrhoea','mild_fever','yellow_urine','yellowing_of_eyes','acute_liver_failure','fluid_overload',
            'swelling_of_stomach','swelled_lymph_nodes','malaise','blurred_and_distorted_vision','phlegm','throat_irritation',
            'redness_of_eyes','sinus_pressure','runny_nose','congestion','chest_pain','weakness_in_limbs','fast_heart_rate',
            'pain_during_bowel_movements','pain_in_anal_region','bloody_stool','irritation_in_anus','neck_pain','dizziness','cramps',
            'bruising','obesity','swollen_legs','swollen_blood_vessels','puffy_face_and_eyes','enlarged_thyroid','brittle_nails',
            'swollen_extremeties','excessive_hunger','extra_marital_contacts','drying_and_tingling_lips','slurred_speech','knee_pain','hip_joint_pain',
            'muscle_weakness','stiff_neck','swelling_joints','movement_stiffness','spinning_movements','loss_of_balance','unsteadiness','weakness_of_one_body_side',
            'loss_of_smell','bladder_discomfort','foul_smell_of urine','continuous_feel_of_urine','passage_of_gases','internal_itching','toxic_look_(typhos)',
            'depression','irritability','muscle_pain','altered_sensorium','red_spots_over_body','belly_pain','abnormal_menstruation','dischromic _patches',
            'watering_from_eyes','increased_appetite','polyuria','family_history','mucoid_sputum','rusty_sputum','lack_of_concentration','visual_disturbances',
            'receiving_blood_transfusion','receiving_unsterile_injections','coma','stomach_bleeding','distention_of_abdomen','history_of_alcohol_consumption',
            'fluid_overload','blood_in_sputum','prominent_veins_on_calf','palpitations','painful_walking','pus_filled_pimples','blackheads','scurring','skin_peeling',
            'silver_like_dusting','small_dents_in_nails','inflammatory_nails','blister','red_sore_around_nose','yellow_crust_ooze'
        ]

def predict(request):
    print('fun called')
    cls = joblib.load('final_model.sav')
    

    if request.method == "POST":
        # Get user-selected symptoms from the form
        print("Code is executing!")
        s1 = request.POST['s1']
        s2 = request.POST['s2']
        s3 = request.POST['s3']
        s4 = request.POST['s4']
        s5 = request.POST['s5']

        # Create a list to store the user-selected symptoms
        user_selected_symptoms = [s1, s2, s3, s4, s5]

        # Create a binary vector representation
        symptom_vector = [1 if symptom in user_selected_symptoms else 0 for symptom in all_symptoms]

        # Convert the symptom_vector to a 2D list (required for model.predict)
        symptom_vector = [symptom_vector]

        # Now you can use the loaded model to make predictions
        prediction = cls.predict(symptom_vector)
        print("Symptom Vector:", symptom_vector)
        print("Prediction:", prediction)

        # Replace this part with your code to map prediction to a disease name
        # You might need a mapping table or dictionary for this
        disease_name = prediction  # Replace with the actual disease name

        # Example: Pass prediction and disease_name to the template
        return render(request, "authentication/predict.html", {'prediction': disease_name})

    # Handle the case when the form is not submitted or symptoms are not selected
    return render(request, "authentication/predict.html")

    
def view_profile(request, doctor_username):
    doctor_instance = get_object_or_404(doctor, doctor_username = doctor_username)  # Retrieve the doctor object or show a 404 page if not found
    return render(request, 'authentication/profile.html', {'doctor': doctor_instance})


