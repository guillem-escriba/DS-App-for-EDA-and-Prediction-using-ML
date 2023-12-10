import math
from matplotlib import pyplot as plt
import numpy as np
import streamlit as st
import pandas as pd
import pickle
import seaborn as sns
import os

st.set_page_config(
    page_title="Salary Prediction",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:guillem.escriba01@estudiant.upf.edu',
        'Report a bug': "mailto:guillem.escriba01@estudiant.upf.edu",
        'About': "# This is a *Data Science App* for the 10th Lab of Visual Analytics"
    }
)

# Obtain the absolute path of this file
script_dir = os.path.dirname(os.path.abspath(__file__))

# Go back to the previous folder (parent directory)
parent_dir = os.path.dirname(script_dir)

# Change the location of the workspace to the parent directory
os.chdir(parent_dir)

# Load the model and label encoders
with open('Models/saved_steps.pkl', 'rb') as file:
    data = pickle.load(file)
random_forest_reg = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

# Load the datasets
original_df = pd.read_csv("Data/survey_results_public.csv")
original_df = original_df.rename(columns={'ConvertedCompYearly': 'Salary'})

model_df = pd.read_csv("Data/dataset_model.csv")

countries = original_df["Country"].dropna()
education_levels = le_education.classes_

# Sidebar for user input
st.sidebar.title('User Input')

# Allow the user to select a country
country = st.sidebar.selectbox('Select a Country', countries.unique())
experience = st.sidebar.slider('Years of Experience', 0, 50, 5)
education = st.sidebar.selectbox("Education Level", education_levels)

# Display the selected options
st.sidebar.write('Selected Country:', country)
st.sidebar.write('Years of Experience:', experience)
st.sidebar.write('Education Level:', education)

# Check if country is in LE
if country not in le_country.classes_:
    # If not, set the country to 'Other'
    country = 'Other'

# Preprocess inputs
country_encoded = le_country.transform([country])
education_encoded = le_education.transform([education])

# Filter the dataset based on user input
filtered_df = model_df[(model_df['Country'] == country_encoded[0]) & (model_df['YearsCodePro'] == experience) & (model_df['EdLevel'] == education_encoded[0])]
n_results = filtered_df.shape[0]
# Display salary statistics for the selected options
st.subheader('Salary Exploration')
st.write(f"Exploring salaries for **{education}** professionals in **{country}** with **{experience}** years of experience:")
st.write(f'(**{n_results}** results)')

# Check for NaN and display appropriate message for each statistic
avg_salary = filtered_df['Salary'].mean()
if pd.isna(avg_salary):
    st.write("Minimum Salary: **No available data**")
    st.write("Average Salary: **No available data**")
    st.write("Maximum Salary: **No available data**")
else:
    min_salary = filtered_df['Salary'].min()
    max_salary = filtered_df['Salary'].max()
    std_salary = filtered_df['Salary'].std()
    st.write(f"Minimum Salary: **${min_salary}**")
    if std_salary is not None and not math.isnan(std_salary):
        st.write(f"Average Salary: **${round(avg_salary)} +- {round(std_salary)}**")
    else:
        st.write(f"Average Salary: **${avg_salary}**")
    st.write(f"Maximum Salary: **${max_salary}**")


# Predicting the salary
if st.button('Predict Salary'):

    # Check if country is in LE
    if country not in le_country.classes_:
        # If not, set the country to 'Other'
        country = 'Other'
        not_available = True

    # Preprocess inputs
    prediction = random_forest_reg.predict([[country_encoded[0], education_encoded[0], experience]])
    
    # Display the prediction
    st.write(f"The estimated salary of your selection is **${prediction[0]:.2f}**")
    st.write("The following plot contains how would the salary vary through the years.")
   
    # Set a dark background style for the plot
    plt.style.use('dark_background')

    # Generate predictions
    experience_range = np.arange(experience, experience + 11)
    predicted_salaries = [random_forest_reg.predict([[country_encoded[0], education_encoded[0], exp]])[0] for exp in experience_range]

    # Create a DataFrame
    salary_data = pd.DataFrame({
        'Years of Experience': experience_range,
        'Predicted Salary': predicted_salaries
    })

    # Set a dark background style for the plot
    plt.style.use('dark_background')

    # Generate predictions
    experience_range = np.arange(experience, experience + 11)
    predicted_salaries = [random_forest_reg.predict([[country_encoded[0], education_encoded[0], exp]])[0] for exp in experience_range]

    # Create a DataFrame
    salary_data = pd.DataFrame({
        'Years of Experience': experience_range,
        'Predicted Salary': predicted_salaries
    })

    # Calculate the corresponding years
    salary_data['Year'] = 2023 + (salary_data['Years of Experience'] - experience)

    # Identify min and max salaries
    min_salary = salary_data['Predicted Salary'].min()
    max_salary = salary_data['Predicted Salary'].max()
    min_year = salary_data[salary_data['Predicted Salary'] == min_salary]['Years of Experience'].values[0]
    max_year = salary_data[salary_data['Predicted Salary'] == max_salary]['Years of Experience'].values[0]

    # Plot using Matplotlib and Seaborn
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Matplotlib line plot for predictions
    ax1.plot(salary_data['Years of Experience'], salary_data['Predicted Salary'], color='cyan', marker='o', label='Predicted Salary')

    # Seaborn regression plot for trend line
    sns.regplot(x='Years of Experience', y='Predicted Salary', data=salary_data, scatter=False, color='yellow', label='Trend Line', ax=ax1)

    # Highlighting min and max points
    ax1.scatter([min_year, max_year], [min_salary, max_salary], color='yellow', zorder=5)

    # Adding labels for min and max
    ax1.text(min_year, min_salary, f' Min: ${min_salary:.2f}', color='yellow', ha='right')
    ax1.text(max_year, max_salary, f' Max: ${max_salary:.2f}', color='yellow', ha='right')

    ax1.set_title("Predicted Salary vs. Years of Experience", color='white')
    ax1.set_xlabel("Years of Experience", color='white')
    ax1.set_ylabel("Predicted Salary", color='white')
    ax1.legend()
    ax1.grid(True, color='gray')

    # Create secondary x-axis for the year at the top
    ax2 = ax1.twiny()
    ax2.set_xlim(ax1.get_xlim())  # Ensure the second x-axis aligns with the first x-axis
    ax2.set_xticks(salary_data['Years of Experience'])
    ax2.set_xticklabels(salary_data['Year'].astype(int))
    ax2.set_xlabel('Year', color='white')

    # Display the plot in Streamlit
    st.pyplot(fig)