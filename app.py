from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Cargar modelo entrenado y columnas en orden correcto
with open('modelo_charges.pkl', 'rb') as f:
    model = pickle.load(f)

# Este es el orden correcto de columnas:
columnas_esperadas = [
    'age', 'bmi', 'children', 'smoker_yes', 'sex_male',
    'region_northwest', 'region_southeast', 'region_southwest'
]

@app.route('/', methods=['GET', 'POST'])
def index():
    prediccion = None
    if request.method == 'POST':
        # Recibir datos del formulario
        age = int(request.form['age'])
        bmi = float(request.form['bmi'])
        children = int(request.form['children'])
        smoker = request.form['smoker']  # 'yes' o 'no'
        sex = request.form['sex']        # 'male' o 'female'
        region = request.form['region']  # 'northeast', 'northwest', etc.

        # Construir diccionario base con valores por defecto
        data = {
            'age': age,
            'bmi': bmi,
            'children': children,
            'smoker_yes': 1 if smoker == 'yes' else 0,
            'sex_male': 1 if sex == 'male' else 0,
            'region_northwest': 0,
            'region_southeast': 0,
            'region_southwest': 0
        }

        # One-hot encoding de la región
        if region == 'northwest':
            data['region_northwest'] = 1
        elif region == 'southeast':
            data['region_southeast'] = 1
        elif region == 'southwest':
            data['region_southwest'] = 1
        # northeast se deja con todos en 0

        # Crear DataFrame y reordenar columnas
        input_df = pd.DataFrame([data])
        input_df = input_df[columnas_esperadas]

        # Predecir
        prediccion = model.predict(input_df)[0]

    return render_template('index.html', prediction=prediccion)
if __name__ == '__main__':
    app.run(debug=True)