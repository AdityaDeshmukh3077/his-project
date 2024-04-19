import psycopg2
import pandas as pd
import joblib

def check_username_password(username, password):
    try:
        conn = psycopg2.connect(
            dbname="his",
            user="dadb",
            host="127.0.0.1",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("SELECT PASSWORD FROM USERS WHERE USERID = %s", (username,))
        row = cur.fetchone()  
        if row:  
            stored_password = row[0]
            if stored_password == password:
                return True
        return False
    except psycopg2.Error as e:
        print("Database error:", e)
        return False
    finally:
        if conn:
            conn.close()


def process_data(patient_data):
    process_patient_data = {}
    list = ['patientAge', 'patientGender','patientEducation', 'patientIncome', 'patientHealthcare','patientCholCheck', 
            'patientSmoker', 'patientStroke','patientHeartDisease','patientPhysHealth', 'patientFruits',
            'patientVegetable','patientHvyAlcCon','patientNoDocBcCost','patientDiffWalk','patientGenHealth','patientPhHealth',
            'patientMentalHealth']
    for item in list:
        process_patient_data[item] = int(patient_data[item])
    process_patient_data['bmi'] = calculate_bmi(int(patient_data['patientWeight']),int(patient_data['patientHeight']))
    process_patient_data['highbp'] = has_high_blood_pressure(int(patient_data['patientSystolicBP']),int(patient_data['patientDiastolicBP']))
    process_patient_data['cholcheck'] = has_high_cholesterol(int(patient_data['patientCholesterol']))
    
    return process_patient_data

def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return bmi

def has_high_blood_pressure(systolic_bp, diastolic_bp):
    if systolic_bp >= 130 or diastolic_bp >= 80:
        return 1
    else:
        return 0
    
def has_high_cholesterol(total_cholesterol):
    if total_cholesterol >= 200:
        return 1
    else:
        return 0
    

def get_predictions(processed_data):
    clf_loaded = joblib.load('logistic_regression_model.joblib')
    columns = ['age', 'anyhealthcare', 'bmi', 'cholcheck', 'diffwalk', 'education',
       'fruitconsum', 'genhlth', 'heartdiseaseorattack', 'highbp', 'highchol',
       'hvyalcoholconsum', 'income', 'menthlth', 'nodocbccost', 'physactivity',
       'physhlth', 'sex', 'smoker', 'stroke', 'vegetableconsum']
    
    data = [processed_data['patientAge'], processed_data['patientHealthcare'], processed_data['bmi'], processed_data['patientCholCheck'],
            processed_data['patientDiffWalk'], processed_data['patientEducation'],processed_data['patientFruits'],processed_data['patientGenHealth'],
            processed_data['patientHeartDisease'], processed_data['highbp'], processed_data['cholcheck'], processed_data['patientHvyAlcCon'],
            processed_data['patientIncome'], processed_data['patientMentalHealth'], processed_data['patientNoDocBcCost'], processed_data['patientPhysHealth'],
            processed_data['patientPhHealth'],  processed_data['patientGender'], processed_data['patientSmoker'], processed_data['patientStroke'], processed_data['patientVegetable']     
    ]

    X_predict = pd.DataFrame([data], columns=columns)
    predictions = clf_loaded.predict(X_predict)
    print(predictions)
    return predictions