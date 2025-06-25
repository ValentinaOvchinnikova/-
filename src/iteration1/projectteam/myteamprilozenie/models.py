from django.db import models

# Это таблицы которые я мигрировала потом в бд
class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True) # Идентификатор пациента
    name = models.CharField(max_length=100) # Имя пациента
    age = models.IntegerField() # Возраст пациента
    # Выбор пола пациента
    GENDER_CHOICES = [('Male', 'Мужской'), ('Female', 'Женский')]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    # Выбор семейного положения
    MARITAL_CHOICES = [
        ('Single', 'Холост/Не замужем'),
        ('Married', 'Женат/Замужем'),
        ('Divorced', 'Разведен(а)')
    ]
    marital_status = models.CharField(max_length=15, choices=MARITAL_CHOICES)
    # Выбор типа работы пациента
    WORK_TYPE_CHOICES = [
        ('Private', 'Частный сектор'),
        ('Self-employed', 'Самозанятый'),
        ('Government', 'Госслужащий'),
        ('Never_worked', 'Не работал(а)')
    ]
    work_type = models.CharField(max_length=20, choices=WORK_TYPE_CHOICES)
    # Выбор места жительства пациента
    RESIDENCE_CHOICES = [('Urban', 'Город'), ('Rural', 'Село')]
    residence_type = models.CharField(max_length=10, choices=RESIDENCE_CHOICES)
    # Когда был добавлен пациент
    created_at = models.DateTimeField(auto_now_add=True)
    # Для строкового выведения и админки
    def __str__(self):
        return f"{self.name} (ID: {self.patient_id})"

# Содержит медицинские данные пациента
class MedicalHistory(models.Model):
    # Статус курильщика
    SMOKING_CHOICES = [
        ('Non-smoker', 'Не курит'),
        ('Formerly smoked', 'Бывший курильщик'),
        ('Currently smokes', 'Курит')
    ]
    # Частота приема алкоголя
    ALCOHOL_CHOICES = [
        ('Never', 'Никогда'),
        ('Rarely', 'Редко'),
        ('Social Drinker', 'Умеренно'),
        ('Frequent Drinker', 'Часто')
    ]
    # Физическая активность
    ACTIVITY_CHOICES = [
        ('Low', 'Низкая'),
        ('Moderate', 'Умеренная'),
        ('High', 'Высокая')
    ]
    # Тип диеты пациента
    DIET_CHOICES = [
        ('Vegan', 'Веган'),
        ('Vegetarian', 'Вегетарианец'),
        ('Pescatarian', 'Пескетарианец'),
        ('Paleo', 'Палеодиета'),
        ('Gluten-Free', 'Без глютена'),
        ('Non-Vegetarian', 'Не вегетарианец')
    ]
    # Связь один-к-одному с моделью Patients
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    # Гипертония да/нет
    hypertension = models.BooleanField(default=False)
    # Болезни сердца да/нет
    heart_disease = models.BooleanField(default=False)
    # Средний уровень глюкозы (десятичное число)
    average_glucose = models.DecimalField(max_digits=6, decimal_places=2)
    # Индекс массы тела (десятичное число)
    bmi = models.DecimalField(max_digits=5, decimal_places=2)
    # Статус курения (то что выбрали в SMOKING_CHOICES)
    smoking_status = models.CharField(max_length=20, choices=SMOKING_CHOICES)
    # Частота употребления алкоголя (то что выбрали в ALCOHOL_CHOICES)
    alcohol_intake = models.CharField(max_length=20, choices=ALCOHOL_CHOICES)
    # Физическая активность (то что выбрали в ACTIVITY_CHOICES)
    physical_activity = models.CharField(max_length=10, choices=ACTIVITY_CHOICES)
    # История инсультов у пациента да/нет
    stroke_history = models.BooleanField(default=False)
    # История инсультов в семье да/нет
    family_stroke_history = models.BooleanField(default=False)
    # Кровяное давление в формате 120/80
    blood_pressure = models.CharField(max_length=10)
    # Липопротеины высокой плотности ("хороший холестерин")
    hdl = models.IntegerField()
    # Липопротеины низкой плотности ("плохой холестерин")
    ldl = models.IntegerField()
    # Пищевые привычки (то что выбрали в DIET_CHOICES)
    dietary_habits = models.CharField(max_length=20, choices=DIET_CHOICES)
    # Уровень стресса (десятичное число)
    stress_level = models.DecimalField(max_digits=3, decimal_places=2)
    # Сопутствующие симптомы (необязательное поле)
    symptoms = models.TextField(blank=True)
    # Сопутствующие диагнозы да/нет
    diagnosis = models.BooleanField(default=False)
    # Для строкового выведения и админки
    def __str__(self):
        return f"Медкарта {self.patient.name}"

# Модель которая содержит результаты оценки риска инсульта
class Prediction(models.Model):
    # Уровни риска
    RISK_LEVELS = [
        ('VL', 'Очень низкий'),
        ('L', 'Низкий'),
        ('M', 'Умеренный'),
        ('H', 'Высокий'),
        ('VH', 'Очень высокий')
    ]
    # Связь многие-к-одному
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    # Связь многие-к-одному
    medical_history = models.ForeignKey(MedicalHistory, on_delete=models.CASCADE)
    # Вероятность инсульта
    probability = models.DecimalField(max_digits=5, decimal_places=4)
    # Уровень риска (то что выбрали в RISK_LEVELS)
    risk_level = models.CharField(max_length=2, choices=RISK_LEVELS)
    # Дата создания прогноза
    created_at = models.DateTimeField(auto_now_add=True)
    advice = models.TextField()  # Рекомендации

    def get_risk_level_color(self):
        colors = {'VL': 'success', 'L': 'info', 'M': 'warning', 'H': 'danger', 'VH': 'dark'}
        return colors.get(self.risk_level, 'secondary')
    # Для строкового выведения и админки
    def __str__(self):
        return f"Прогноз для {self.patient.name} - {self.get_risk_level_display()}"