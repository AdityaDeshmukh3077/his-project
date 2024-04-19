import psycopg2
import pandas as pd

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
    process_patient_data['BMI'] = calculate_bmi(int(patient_data['patientWeight']),int(patient_data['patientHeight']))
    process_patient_data['highchol'] = has_high_blood_pressure(int(patient_data['patientSystolicBP']),int(patient_data['patientDiastolicBP']))
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