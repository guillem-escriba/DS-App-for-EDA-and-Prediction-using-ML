import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import plotly.express as px

st.set_page_config(
    page_title="Dynamic Visualization",
    page_icon="📊",
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

# Define sections
sections = ['Maps', 'Interactive Salary Distribution Histogram', 'Boxplot of Salary Distribution by Country',
            'Boxplot of Salary Distribution by Education Level', 'Salary vs Years of Professional Experience',
            'Interactive Bubble Chart: Salary and Experience by Country']

# Sidebar for navigation
st.sidebar.title('Navigation')
selected_section = st.sidebar.radio('Go to', sections)

if selected_section == 'Maps':
    original_df = pd.read_csv("Data/survey_results_public.csv")
    original_df = original_df.rename(columns={'ConvertedCompYearly': 'Salary'})
    original_df["Country"] = original_df["Country"].dropna()
    original_df["Salary"] = original_df["Salary"].dropna()
    original_df = original_df[original_df['Salary'] < 250000]

    st.title('Welcome to the Dynamic Visualization Dashboard')
    st.write('Please select a section from the sidebar to start exploring the data.')
    
    px.defaults.template = 'plotly_dark'
    # Calculate the number of respondents by country
    country_counts = original_df['Country'].value_counts().reset_index()
    country_counts.columns = ['country', 'count']

    # Create a choropleth map
    st.subheader('Global Distribution of Survey Respondents')
    st.write("This map shows the global distribution of survey respondents. The color intensity represents the number of respondents from each country.")

    fig = px.choropleth(
        country_counts, 
        locations='country', 
        locationmode='country names', 
        color='count',
        hover_name='country',
        color_continuous_scale='RdBu',
        title='Respondents by Country',
        width=1200, 
        height=800 
    )
    st.plotly_chart(fig)

    # Calculate the average salary by country
    average_salary_by_country = original_df.groupby('Country')['Salary'].mean().reset_index()
    average_salary_by_country.columns = ['country', 'average_salary']

    # Create a choropleth map for Average Salary by Country
    st.subheader('Global Average Salary of Survey Respondents')
    st.write("This map shows the global average salary of survey respondents. The color intensity represents the average salary in each country.")

    fig = px.choropleth(
        average_salary_by_country, 
        locations='country', 
        locationmode='country names', 
        color='average_salary',
        hover_name='country',
        color_continuous_scale='rdylbu', 
        title='Average Salary by Country',
        width=1200, 
        height=800 
    )

    st.plotly_chart(fig)

if selected_section == 'Interactive Salary Distribution Histogram':
    # Dropdown to select Country
    country = st.multiselect(
        'Select Country',
        options=decoded_df['Country'].unique(),
        default=decoded_df['Country'].unique()
    )

    # Dropdown to select Education Level
    education_level = st.multiselect(
        'Select Education Level',
        options=decoded_df['EdLevel'].unique(),
        default=decoded_df['EdLevel'].unique()
    )

    # Filtering data based on selection
    filtered_df = decoded_df[
        (decoded_df['Country'].isin(country)) & 
        (decoded_df['EdLevel'].isin(education_level))
    ]
    
    # Interactive Histogram for Salary Distribution
    st.subheader('Interactive Salary Distribution Histogram')
    fig = px.histogram(
        filtered_df, 
        x='Salary', 
        nbins=50, 
        title='Salary Distribution',
        color_discrete_sequence=['indianred'] # You can choose any color you like
    )
    fig.update_layout(bargap=0.1)
    st.plotly_chart(fig)
    st.write("""
        Explore the distribution of salaries within the tech industry. Use the sidebar to filter by country and education level.
        This histogram updates dynamically based on your selections, allowing for a deeper dive into the specific segments of the dataset.
        It can provide valuable insights into salary disparities and distributions across different demographics.
    """)

if selected_section == 'Boxplot of Salary Distribution by Country':
    ## Interactive Box Plot for Salary Distribution by Country
    st.subheader("Boxplot of Salary Distribution by Country")
    selected_countries = st.multiselect('Select countries', decoded_df['Country'].unique(), default=decoded_df['Country'].unique()[:20])
    filtered_df = decoded_df[decoded_df['Country'].isin(selected_countries)]
    fig = px.box(
        filtered_df, 
        x='Country', 
        y='Salary', 
        color='Country',
        title="Salary Distribution by Country",
        labels={'Country': 'Country', 'Salary': 'Salary'},
        notched=True,  # shows the confidence interval for the median
        template='plotly_dark'
    )
    st.plotly_chart(fig, use_container_width=True)
    st.write("This box plot shows the salary distribution for each selected country, allowing for a comparison of salary ranges and identification of outliers.")


if selected_section == 'Boxplot of Salary Distribution by Education Level':
    ## Interactive Box Plot for Salary Distribution by Education Level
    st.subheader("Boxplot of Salary Distribution by Education Level")
    fig = px.box(
        decoded_df, 
        x='EdLevel', 
        y='Salary', 
        color='EdLevel',
        title="Salary Distribution by Education Level",
        labels={'EdLevel': 'Education Level', 'Salary': 'Salary'},
        notched=True,  # shows the confidence interval for the median
        template='plotly_dark'
    )
    st.plotly_chart(fig, use_container_width=True)
    st.write("The box plot provides a visual summary of the central tendency, dispersion, and skewness of the salary distribution and highlights potential outliers.")


if selected_section == 'Salary vs Years of Professional Experience':
    ## Interactive Scatter Plot for Salary vs Years of Experience
    st.subheader("Salary vs Years of Professional Experience")
    color_discrete_sequence = px.colors.qualitative.Alphabet
    fig = px.scatter(
        decoded_df, 
        x='YearsCodePro', 
        y='Salary', 
        color='Country', 
        title='Salary vs. Professional Coding Experience',
        color_discrete_sequence=color_discrete_sequence, 
        hover_name='Country', 
        size_max=10, 
        template='plotly_dark', 
        width=1200, 
        height=800  
    )
    fig.update_layout(
        xaxis_title="Years of Professional Coding",
        yaxis_title="Salary",
        legend_title="Country",
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="White"
        )
    )
    st.plotly_chart(fig)
    st.write("This interactive scatter plot allows you to explore the relationship between years of professional coding experience and salary, with data points colored by country.")


if selected_section == 'Interactive Bubble Chart: Salary and Experience by Country':
    ## Interactive Bubble Chart: Salary and Experience by Country
    # Create a new column 'count' which is a count of respondents for each 'YearsCodePro' and 'Salary' by 'Country'
    decoded_df['count'] = decoded_df.groupby(['YearsCodePro', 'Salary', 'Country'])['Country'].transform('count')
    st.subheader("Interactive Bubble Chart: Salary and Experience by Country")
    color_discrete_sequence = px.colors.qualitative.Alphabet
    fig = px.scatter(
        decoded_df,
        x="YearsCodePro",
        y="Salary",
        size="count",  
        color="Country",
        hover_name="Country",
        log_x=False, 
        size_max=60,
        title="Relationship between Professional Coding Experience, Salary, and Country",
        color_discrete_sequence=color_discrete_sequence, 
        template='plotly_dark',
        width=1200, 
        height=800  
    )
    fig.update_layout(
        xaxis_title="Years of Professional Coding",
        yaxis_title="Salary",
        legend_title="Country"
    )
    st.plotly_chart(fig)
    st.write("This bubble chart allows you to interactively explore the relationship between professional coding experience, salary, and country. Larger bubbles represent a higher concentration of respondents.")
