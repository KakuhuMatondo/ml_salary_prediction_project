import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_categories(categories, cutoff):
    categorical_map={}
    for i in range( len(categories)):
        if categories.values[i]>=cutoff:
            categorical_map[categories.index[i]]=categories.index[i]
        else:
            categorical_map[categories.index[i]]='Other'
    return categorical_map
def clean_experience(x):
    if x=="More than 50 years":
        return 50
    if x=="Less than 1 year":
        return 0.5
    return float(x)
#%%
def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if  'Master’s degree' in x:
        return 'Master’s degree'
    if  'Professional degree' in x:
        return 'Post Grad'
    return 'Less than a Bachelors'
@st.cache_data
def load_data():
    data = pd.read_csv(
        "C:\\Users\\tekno asya\\Downloads\\stack-overflow-developer-survey-2023\\survey_results_public.csv")
    data = data[['Country', 'EdLevel', 'YearsCodePro', 'Employment', 'ConvertedCompYearly']]
    data = data.rename({'ConvertedCompYearly': 'Salary'}, axis=1)
    data = data[data["Salary"].notnull()]
    data = data.dropna()
    data = data[data['Employment'] == 'Employed, full-time']
    data = data.drop('Employment', axis=1)

    country_map = shorten_categories(data.Country.value_counts(), 400)
    data['Country'] = data["Country"].map(country_map)
    data = data[data['Salary'] <= 200000]
    data = data[data['Country']!="Other"]
    data['EdLevel'] = data['EdLevel'].apply(clean_education)
    data['YearsCodePro'] = data['YearsCodePro'].apply(clean_experience)

    return data
data=load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write("""### Stack Overflow Developer Survey 2023""")
    country_data=data['Country'].value_counts()

    fig1,ax1=plt.subplots()
    ax1.pie(country_data,labels=country_data.index,autopct='%1.1f%%',shadow=True,startangle=90)
    ax1.axis('equal')

    st.write("""#### Number of Data by Country""")
    st.pyplot(fig1)

    st.write("""### Mean Salary Based On Country""")
    mean_salary_data_country=data.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(mean_salary_data_country)

    st.write("""### Mean Salary Based On Experience""")
    mean_salary_data_exp = data.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(mean_salary_data_exp)



