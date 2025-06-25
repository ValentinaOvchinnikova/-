import json
import lightgbm as lgb
import pandas as pd

def predskazanie(gender: str,
                 age: int,
                 hypertension: int,
                 heart_disease: int,
                 ever_married: str,
                 work_type: str,
                 residence_type: str,
                 avg_glucose_level: float,
                 bmi: float,
                 smoking_status: str
                 ):
    """
    Принимает некоторый перечень данных и на их основе осуществляет предсказание риска возникновения инсульта
    :param gender: Пол
    :param age: Возраст
    :param hypertension: 1 - Гипертония есть; 0 - Гипертонии нет;
    :param heart_disease: 1 - Заболевания сердца есть; 0 - отсутсвуют;
    :param ever_married: Принимает в виде параметров Yes или No;
    :param work_type: Тип работы
    :param residence_type: Городской или сельский житель
    :param avg_glucose_level: Средний уровень глюкозы в крови
    :param bmi: Индекс массы тела
    :param smoking_status: Статус курения
    :return: Риск и его степень возникновения инсульта
    """

    #Создадим из поступивших данных датафрейм
    df = {
        'gender': gender,
        'age': age,
        'hypertension': hypertension,
        'heart_disease': heart_disease,
        'ever_married': ever_married,
        'work_type': work_type,
        'Residence_type': residence_type,
        'avg_glucose_level': avg_glucose_level,
        'bmi': bmi,
        'smoking_status': smoking_status
    }

    df = pd.DataFrame([df])

    #Обозначаем категориальные столбцы
    cat_features = ['gender', 'ever_married', 'work_type', 'Residence_type', 'smoking_status']
    for col in cat_features:
        df[col] = df[col].astype('category')

    #Загрузим маппинг
    with open('label_mappings.json', 'r') as f:
        json_data = json.load(f)

    #Закодим столбцы
    for colum in cat_features:
        mapping = json_data[colum]
        df[colum] = df[colum].map(mapping)

    #Загрузка модели
    model = lgb.Booster(model_file='stroke_lgbm_model.txt')
    result = model.predict(df)
    score = float(result[0])  # Достаём скаляр из массива

    # Логика интерпретации риска
    if score < 0.05:
        category = "🟢 КРАЙНЕ НИЗКИЙ риск инсульта"
        advice = "Поздравляем! Вероятность инсульта крайне мала."
    elif score < 0.20:
        category = "🟢 НИЗКИЙ риск инсульта"
        advice = "Риск инсульта низкий, но профилактика не помешает."
    elif score < 0.40:
        category = "🟡 ЗНАЧИТЕЛЬНЫЙ (умеренный) риск инсульта"
        advice = "Обратите внимание на факторы риска и профилактические меры."
    elif score < 0.70:
        category = "🟠 ВЫСОКИЙ риск инсульта"
        advice = "Рекомендуется проконсультироваться с врачом и пересмотреть образ жизни."
    else:
        category = "🔴 КРАЙНЕ ВЫСОКИЙ риск инсульта"
        advice = "Немедленно обратитесь к врачу для комплексного обследования!"

    # Один return, выводим всё что нужно
    print(f"Вероятность инсульта: {score:.1%}")
    print(category)
    print(advice)
    return score, category, advice

"""Проверка"""

high_risk = {
    'Gender': 'Female',
    'Age': 29,
    'Hypertension': 0,
    'Heart Disease': 0,
    'Ever Married': 'No',
    'Work Type': 'Never_worked',
    'Residence Type': 'Rural',
    'Avg Glucose Level': 85.0,
    'BMI': 20.2,
    'Smoking Status': 'never smoked'
}

result = predskazanie(gender=high_risk['Gender'],
             age=high_risk['Age'],
             hypertension=high_risk['Hypertension'],
             heart_disease=high_risk['Heart Disease'],
             ever_married=high_risk['Ever Married'],
             work_type=high_risk['Work Type'],
             residence_type=high_risk['Residence Type'],
             avg_glucose_level=high_risk['Avg Glucose Level'],
             bmi=high_risk['BMI'],
             smoking_status=high_risk['Smoking Status']
             )
