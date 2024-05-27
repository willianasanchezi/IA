import pickle
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm

# Cargar el modelo desde el archivo .pkl
with open('modelo.pkl', 'rb') as f:
    model = pickle.load(f)

# Cargar el vectorizador desde el archivo .pkl
with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# Encabezado y descripción del formulario
st.title("Clasificador de Áreas")
st.write("Ingrese un texto para clasificarlo en una de las siguientes áreas: finanzas, recursos humanos, mercadeo o compras.")

# Obtener la entrada del usuario
text_input = st.text_input("Texto:", "")

# Realizar la predicción
if st.button("Predecir"):
    if text_input.strip() == "":
        st.warning("Por favor, ingrese un texto válido.")
    else:
        # Vectorizar el texto utilizando el vectorizador ya ajustado
        text_input_vectorized = vectorizer.transform([text_input])
        
        # Obtener las puntuaciones de decisión
        decision_scores = model.decision_function(text_input_vectorized)[0]
        
        # Obtener las etiquetas en orden de importancia (mayor puntuación de decisión primero)
        sorted_labels = [label for _, label in sorted(zip(decision_scores, model.classes_), reverse=True)]
        
        # Obtener la primera opción, su puntaje de decisión y las otras opciones en orden de importancia
        first_option = sorted_labels[0]
        first_option_score = decision_scores[model.classes_.tolist().index(first_option)]
        other_options = sorted_labels[1:]
        
        # Mostrar la primera opción, su puntaje de decisión y las otras opciones en orden de importancia
        st.success("La primera opción es: {} (Puntaje de decisión: {:.2f})".format(first_option, first_option_score))
        st.write("Otras opciones en orden de importancia:")
        for option in other_options:
            option_score = decision_scores[model.classes_.tolist().index(option)]
            st.write("- {} (Puntaje de decisión: {:.2f})".format(option, option_score))
