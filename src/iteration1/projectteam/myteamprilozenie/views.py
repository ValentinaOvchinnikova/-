from django.shortcuts import render, redirect
from django.db import transaction
from .models import Patient, MedicalHistory, Prediction
from .forms import PatientForm, MedicalHistoryForm
from .utils import predskazanie

from django.http import HttpResponse

# def home(request):
#     return HttpResponse("Сервер работает! Проверка связи.")

def home(request):
    return render(request, 'myteamprilozenie/home.html')


def register_patient(request):
    if request.method == 'POST': # Если форма отправлена то создаем форму с данными из пост
        form = PatientForm(request.POST)
        if form.is_valid(): # Если форма правильная то сохраняем данные в бд
            patient = form.save()
            request.session['patient_id'] = patient.patient_id  # сохраняем айди в сессии чтобы работать с другими формами
            return redirect('myteamprilozenie:medical_history')
    else:
        form = PatientForm()

    return render(
        request,
        'myteamprilozenie/register_patient.html',  # Полный путь
        {'form': form} # Передаем форму в шаблон
    )


def medical_history(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('register_patient')

    try:
        patient = Patient.objects.get(pk=patient_id)
    except Patient.DoesNotExist:
        return redirect('register_patient')

    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST)
        if form.is_valid():
            medical_data = form.save(commit=False)
            medical_data.patient = patient
            medical_data.save()

            # Прогнозирование
            score, risk_level, advice = predskazanie(
                gender=patient.gender,
                age=patient.age,
                hypertension=medical_data.hypertension,
                heart_disease=medical_data.heart_disease,
                ever_married=patient.marital_status,
                work_type=patient.work_type,
                residence_type=patient.residence_type,
                avg_glucose_level=float(medical_data.average_glucose),
                bmi=float(medical_data.bmi),
                smoking_status=medical_data.smoking_status
            )

            # Сохранение прогноза
            prediction = Prediction.objects.create(
                patient=patient,
                medical_history=medical_data,
                probability=score,
                risk_level=risk_level,
                advice=advice  # Добавьте это поле в модель Prediction
            )
            return redirect('myteamprilozenie:prediction_result', prediction_id=prediction.pk)

    else:
        form = MedicalHistoryForm()

    return render(request, 'myteamprilozenie/medical_history.html', {
        'form': form,
        'patient': patient
    })

# Здесь уже итоговый прогноз
def prediction_result(request, prediction_id):
    try:
        prediction = Prediction.objects.select_related('patient', 'medical_history').get(pk=prediction_id)
    except Prediction.DoesNotExist:
        return redirect('register_patient')

    return render(request, 'myteamprilozenie/predictions.html', {'prediction': prediction})