import streamlit as st
import pickle
import numpy as np


def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data


data = load_model()

regressor = data['model']
le_country = data['le_country']
le_education = data['le_education']


def show_predict_page():
    st.title("Software Development Salary Prediction")
    st.write("""### We need some information to predict the salary""")

    Countries = ('United States of America',
                 'Germany',
                 'United Kingdom of Great Britain and Northern Ireland',
                 'Canada',
                 'India',
                 'France',
                 'Netherlands',
                 'Australia',
                 'Brazil',
                 'Spain'
                 )

    Education = ('Bachelor’s degree',
                 'Less than a Bachelors',
                 'Master’s degree',
                 'Post Grad'
                 )
    country = st.selectbox("Country", Countries)
    education = st.selectbox("Education Level", Education)
    experience = st.slider("Years of Experience",0,50,3)

    ok=st.button("Calculate Salary")
    if ok:
        X = np.array([[country, education, experience]])
        X[:, 0] = le_country.transform(X[:, 0])
        X[:, 1] = le_education.transform(X[:, 1])
        X.astype(float)

        salary=regressor.predict(X)
        st.subheader(f"The estimated Salary is ${salary[0].round(2)}")

