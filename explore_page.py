import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st


def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def clean_experience(x):
    if x == "More than 50 years":
        return 50
    if x == "Less than 1 year":
        return 0.5
    return float(x)


# %%
def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x:
        return 'Post Grad'
    return 'Less than a Bachelors'


@st.cache_data
def load_data():
    l_data = pd.read_csv(
        "C:\\Users\\tekno asya\\Downloads\\stack-overflow-developer-survey-2023\\survey_results_public.csv")
    l_data = l_data[['Country', 'EdLevel', 'YearsCodePro', 'Employment', 'ConvertedCompYearly']]
    l_data = l_data.rename({'ConvertedCompYearly': 'Salary'}, axis=1)
    l_data = l_data[l_data["Salary"].notnull()]
    l_data = l_data.dropna()
    l_data = l_data[l_data['Employment'] == 'Employed, full-time']
    l_data = l_data.drop('Employment', axis=1)

    country_map = shorten_categories(l_data.Country.value_counts(), 400)
    l_data['Country'] = l_data["Country"].map(country_map)
    l_data = l_data[l_data['Salary'] <= 200000]
    l_data = l_data[l_data['Country'] != "Other"]
    l_data['EdLevel'] = l_data['EdLevel'].apply(clean_education)
    l_data['YearsCodePro'] = l_data['YearsCodePro'].apply(clean_experience)

    return l_data


data = load_data()


def show_explore_page():
    st.title("""EXPLORE FACTS AND FIGURES ABOUT SOFTWARE ENGINEER SALARIES WORLDWIDE\n\n""")
    st.header("""_Stack Overflow Developer Survey 2023_ \n\n""")

    st.write("""#  Exploration by Country\n""")

    st.subheader(""" Percentage of Software Engineers per Country""")
    country_data = data['Country'].value_counts()
    labels = country_data.index
    # Explode values
    explode = []
    for i in range(len(labels)):
        explode.append(0.05)
        if country_data.iloc[i] == max(country_data.value_counts()):
            explode[i] = 0.75

    fig1, ax1 = plt.subplots(figsize=(60, 70), facecolor='none')

    # Plot pie chart on ax
    ax1.pie(country_data, labels=labels, autopct='%1.1f%%', textprops={'weight': "bold", 'fontsize': 60},
            radius=4, shadow=True, startangle=180, labeldistance=1.1, pctdistance=0.8, explode=explode,
            colors=plt.cm.Blues(np.linspace(1, 0.5, len(labels))))
    ax1.axis('equal')
    st.pyplot(fig1)

    st.subheader(""" Mean Salary Based On Country""")
    mean_salary_data_country = data.groupby(["Country"])["Salary"].mean().sort_values(ascending=False).round(2)
    st.table(mean_salary_data_country)

    st.subheader("""Education Level based on Country""")
    fig8, ax8 = plt.subplots(figsize=(12, 8), facecolor='none')

    sns.countplot(data=data, x="EdLevel", hue="Country", palette='pastel', ax=ax8)
    ax8.set_title("Relationship between Country and Education Level", fontweight='bold')
    ax8.set_xlabel("Education Level", fontweight='bold')
    ax8.set_ylabel("Number of Software Engineers", fontweight='bold')
    ax8.set_xticklabels(ax8.get_xticklabels(), rotation=45, ha='right', fontsize=10)
    ax8.legend(title="Education Level", title_fontsize='13')
    st.pyplot(fig8)

    st.write("""# Exploration by Education Level""")
    st.subheader("""Qualifications of Software Engineers""")

    fig4, ax4 = plt.subplots(facecolor='none')

    EdLevel_data = data['EdLevel'].value_counts()
    x = EdLevel_data.index
    y = EdLevel_data.values

    bars = ax4.barh(x, y, color=plt.cm.Blues(np.linspace(1, 0.8, len(x))))
    ax4.set_xlabel('Number of Software Engineers', fontweight='bold')

    # Set the y-axis label
    ax4.set_ylabel('Education Level', fontweight='bold', labelpad=30)

    def format_with_comma(val):
        return '{:,.0f}'.format(val)

    # Add data labels to the bars
    for bar, value in zip(bars, y):
        ax4.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, format_with_comma(value),
                 va='center', ha='left', fontsize=12)

    fig4.tight_layout()
    st.pyplot(fig4)

    st.subheader("Distribution of Salary based on Education Level")

    fig7, ax7 = plt.subplots(facecolor='none')
    sns.kdeplot(data=data, x="Salary", hue="EdLevel", fill=True)
    ax7.set_title("Density Plot of Salary Based on Education Level", fontweight='bold')
    ax7.set_xlabel("Salary", fontweight='bold')
    ax7.set_ylabel("Density", fontweight='bold')

    def format_usd(x, pos):
        return f'${x:,.0f}'

    formatter = ticker.FuncFormatter(format_usd)
    ax7.xaxis.set_major_formatter(formatter)
    st.pyplot(fig7)

    st.write("""# Exploration by Years of Experience\n""")
    st.subheader("""Distribution of Years of Experience""")

    fig5, ax5 = plt.subplots(facecolor='none')
    sns.kdeplot(data=data['YearsCodePro'], fill=True)
    ax5.set_xlabel('Years of Experience', fontweight='bold')
    ax5.set_ylabel('Density', fontweight='bold')
    ax5.set_title('Density Plot of Years of Experience')
    st.pyplot(fig5)

    st.write("""# Mean Salary Based On Experience""")
    mean_salary_data_exp = data.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    fig6, ax6 = plt.subplots(facecolor='none')
    sns.lineplot(data=mean_salary_data_exp, x=mean_salary_data_exp.index, y=mean_salary_data_exp.values, color='red')
    ax6.set_title('Average Salary vs Years of Experience')
    ax6.set_xlabel('Years of Experience', fontweight='bold')
    ax6.set_ylabel('Average Salary', fontweight='bold')

    def format_usd(x, pos):
        return f'${x:,.0f}'
    formatter = ticker.FuncFormatter(format_usd)
    ax6.yaxis.set_major_formatter(formatter)
    st.pyplot(fig6)
