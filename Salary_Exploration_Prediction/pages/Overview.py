import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import plotly.express as px

st.set_page_config(
    page_title="Overview",
    page_icon="🧑‍💻",
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

# Load the datasets
original_df = pd.read_csv("Data/survey_results_public.csv")
original_df = original_df.rename(columns={'ConvertedCompYearly': 'Salary'})

decoded_df = pd.read_csv("Data/dataset_overview.csv")
countries = original_df["Country"].dropna()

# Set the aesthetic style of the plots
plt.style.use('dark_background')

# Sections of the menu
sections = ['Data overview', 'Country Data Distribution' , 'Average Salary by Country', 
            'Salary Progression Over Years of Experience', 'Salary Distribution by Education Level',
            'Heatmap of Salary by Country and Education Level']

# Sidebar for navigation
st.sidebar.title('Navigation')
selected_section = st.sidebar.radio('Go to', sections)

# Conditional rendering based on selected section
if selected_section == 'Data overview':
    st.title('Welcome to the Data Overview Dashboard')
    st.write('Please select a section from the sidebar to start exploring the data.')
    st.header("Overview of the survey data")
    if st.checkbox("Show Data Summary"):
        st.write("Here you can explore the dataset used for the model:")
        st.dataframe(decoded_df, width=1500, height=600)
        st.write("The numerical data has the following statistics:")
        st.write(decoded_df.describe())

if selected_section == 'Country Data Distribution':
    ## Circular Plot for 'Country' Data Percentages
    st.subheader("Country Data Distribution")
    country_counts = decoded_df['Country'].value_counts()
    plt.figure(figsize=(10, 10))
    plt.pie(country_counts, labels=country_counts.index, autopct='%1.1f%%', textprops={'color': "grey"})
    plt.title('Percentage of Data by Country')  
    st.pyplot(plt)
    st.write("This pie chart represents the distribution of survey responses by country, providing insight into the geographical diversity of the data.")

if selected_section == 'Average Salary by Country':
    ## Bar Plot for Mean 'Salary' by 'Country' including Global Average
    st.subheader("Average Salary by Country")
    plt.figure(figsize=(12, 6))
    mean_salary_by_country = decoded_df.groupby('Country')['Salary'].mean().sort_values(ascending=True)
    global_average_salary = decoded_df['Salary'].mean()
    palette = sns.color_palette("husl", len(mean_salary_by_country))
    sns.barplot(x=mean_salary_by_country.values, y=mean_salary_by_country.index, 
        hue=mean_salary_by_country.index, palette=palette, dodge=False)
    plt.legend([],[], frameon=False) 
    plt.axvline(global_average_salary, color='red', linewidth=2, linestyle='--')
    plt.text(global_average_salary, plt.gca().get_ylim()[1], f'Global Average: {global_average_salary:.2f}', 
            va='top', ha='left', color='red', fontsize=10)
    max_value = mean_salary_by_country.max()
    min_value = mean_salary_by_country.min()
    max_country = mean_salary_by_country.idxmax()
    min_country = mean_salary_by_country.idxmin()
    plt.text(max_value, mean_salary_by_country.index.get_loc(max_country), 
            f'Max: {max_value:.2f}', va='center', ha='right', color='white')
    plt.text(min_value, mean_salary_by_country.index.get_loc(min_country), 
            f'Min: {min_value:.2f}', va='center', ha='right', color='white')
    plt.xlabel('Average Salary')
    plt.ylabel('Country')
    plt.title('Average Salary by Country')
    st.pyplot(plt)
    st.write("The bar plot above illustrates the average salary in each country, highlighting regional differences in compensation. Countries are color-coded for better visual differentiation, with annotations indicating the maximum and minimum average salaries.")

if selected_section == 'Salary Progression Over Years of Experience':
    ## Line Plot for Mean 'Salary' Based on 'YearsCodePro'
    st.subheader("Salary Progression Over Years of Experience")
    plt.figure(figsize=(14, 7))
    mean_salary_by_experience = decoded_df.groupby('YearsCodePro')['Salary'].mean().reset_index()
    mean_salary_by_experience['YearsCodePro'] = mean_salary_by_experience['YearsCodePro'].astype(float)
    max_value = mean_salary_by_experience['Salary'].max()
    min_value = mean_salary_by_experience['Salary'].min()
    sns.lineplot(data=mean_salary_by_experience, x='YearsCodePro', y='Salary', label='Average Salary')
    sns.regplot(data=mean_salary_by_experience, x='YearsCodePro', y='Salary', scatter=False, color='red', label='Trend Line')
    max_point = mean_salary_by_experience.loc[mean_salary_by_experience['Salary'].idxmax()]
    plt.annotate(f'Max: ${max_point.Salary:.2f}', xy=(max_point.YearsCodePro, max_point.Salary), xytext=(5, 0), 
                textcoords='offset points', ha='center', va='bottom', color='green')
    min_point = mean_salary_by_experience.loc[mean_salary_by_experience['Salary'].idxmin()]
    plt.annotate(f'Min: ${min_point.Salary:.2f}', xy=(min_point.YearsCodePro, min_point.Salary), xytext=(5, 0), 
                textcoords='offset points', ha='center', va='top', color = 'red')
    plt.xlabel('Years of Professional Coding')
    plt.ylabel('Average Salary')
    plt.title('Average Salary by Years of Professional Coding')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)
    st.write("The line plot above depicts how the average salary changes with increasing years of professional coding experience.")

if selected_section == 'Salary Distribution by Education Level':
    ## Average Salary by Education Level
    st.subheader("Salary Distribution by Education Level")
    plt.figure(figsize=(10, 6))
    mean_salary_by_edlevel = decoded_df.groupby('EdLevel')['Salary'].mean().sort_values()
    palette = sns.color_palette("viridis", len(mean_salary_by_edlevel))
    barplot = sns.barplot(x=mean_salary_by_edlevel.index, y=mean_salary_by_edlevel.values, palette=palette)
    for index, value in enumerate(mean_salary_by_edlevel.values):
        plt.text(index, value, f'${value:.2f}', color='white', ha='center', va='bottom')
    plt.xticks(rotation=45)
    plt.xlabel('Education Level')
    plt.ylabel('Average Salary')
    plt.title('Average Salary by Education Level')
    st.pyplot(plt)
    st.write("Finally, this bar plot compares the average salary across different education levels, illustrating the influence of educational attainment on earnings.")

if selected_section == 'Heatmap of Salary by Country and Education Level':
    ## Heatmap of Salary by Country and Education Level
    st.subheader("Heatmap of Salary by Country and Education Level")
    pivot_table = decoded_df.pivot_table(index='Country', columns='EdLevel', values='Salary', aggfunc='mean')
    plt.figure(figsize=(12, 10))
    sns.heatmap(pivot_table, annot=True, fmt=".0f", cmap='coolwarm',linewidths=1,linecolor='black')
    plt.title('Heatmap of Average Salary by Country and Education Level')
    st.pyplot(plt)
    st.write("The heatmap visualizes the average salary based on both country and education level, providing a two-dimensional view of these factors' impact on earnings.")