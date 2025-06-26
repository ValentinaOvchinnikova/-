import json
import pandas as pd
import lightgbm as lgb
from django.conf import settings
import os

def predskazanie(gender: str, age: int, hypertension: bool, heart_disease: bool,
                 ever_married: str, work_type: str, residence_type: str,
                 avg_glucose_level: float, bmi: float, smoking_status: str):
    """
    Предсказывает риск инсульта на основе входных данных.
    Возвращает: (score, category, advice)
    """
    # Загрузка маппинга
    model_dir = os.path.join(settings.BASE_DIR, 'myteamprilozenie', 'model')
    with open(os.path.join(model_dir, 'label_mappings.json'), 'r') as f:
        mappings = json.load(f)

    # Подготовка данных
    data = {
        'gender': mappings['gender'][gender],
        'age': age,
        'hypertension': int(hypertension),
        'heart_disease': int(heart_disease),
        'ever_married': mappings['ever_married'][ever_married],
        'work_type': mappings['work_type'][work_type],
        'Residence_type': mappings['Residence_type'][residence_type],
        'avg_glucose_level': avg_glucose_level,
        'bmi': bmi,
        'smoking_status': mappings['smoking_status'][smoking_status]
    }
    df = pd.DataFrame([data])

    # Обозначаем категориальные столбцы
    cat_features = ['gender', 'ever_married', 'work_type', 'Residence_type', 'smoking_status']
    for col in cat_features:
        df[col] = df[col].astype('category')


    # Загрузка модели
    model_path = os.path.join(model_dir, 'stroke_lgbm_model.txt')
    model = lgb.Booster(model_file=model_path)
    score = float(model.predict(df)[0])

    # Определение уровня риска
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
