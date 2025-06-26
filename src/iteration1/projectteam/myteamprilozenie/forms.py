from django import forms
from .models import Patient, MedicalHistory

# Форма на основе модели Patient
class PatientForm(forms.ModelForm):
    class Meta: # Класс позволяет определять конфигурацию модели (какие поля использовать, какую модель, какие настройки полей)
        model = Patient
        fields = '__all__' # Берем все поля модели
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}), # Свободное текстовое поле
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}), # Целочисленное значение
            'gender': forms.Select(attrs={'class': 'form-select'}), # выпадающий список
            'ever_married': forms.Select(attrs={'class': 'form-select'}), # выпадающий список
            'work_type': forms.Select(attrs={'class': 'form-select'}), # выпадающий список
            'residence_type': forms.Select(attrs={'class': 'form-select'}), # выпадающий список
        }


class MedicalHistoryForm(forms.ModelForm):
    blood_pressure = forms.RegexField(
        regex=r'^\d{2,3}/\d{2,3}$', # Вводим в формате число/число
        error_messages={'invalid': 'Введите давление в формате 120/80'},
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '120/80'})
    )

    symptoms = forms.CharField(
        required=False, # Необязательное для заполнения текстовое поле
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Опишите симптомы если таковые имеются...'
        })
    )

    class Meta:
        model = MedicalHistory
        exclude = ['patient'] # Поле заполнится автоматически поэтому его исключаем
        widgets = {
            'average_glucose': forms.NumberInput(attrs={'class': 'form-control'}), # Целочисленное значение
            'bmi': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите индекс массы тела...'}),
            'hdl': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ЛПВП (хороший холестерин)...'}),
            'ldl': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ЛПНП (плохой холестерин)...'}),
            'stress_level': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '10'
            }),
            'hypertension': forms.CheckboxInput(attrs={'class': 'form-check-input'}), # чекбоксы
            'diagnosis': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'heart_disease': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'stroke_history': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'family_stroke_history': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'smoking_status': forms.Select(attrs={'class': 'form-select'}), # Выпадающий список
            'alcohol_intake': forms.Select(attrs={'class': 'form-select'}),
            'physical_activity': forms.Select(attrs={'class': 'form-select'}),
            'dietary_habits': forms.Select(attrs={'class': 'form-select'}),
        }