
from matplotlib import pyplot as plt
import numpy as np
import streamlit as st
import pandas as pd
import pickle
import seaborn as sns


st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:guillem.escriba01@estudiant.upf.edu',
        'Report a bug': "mailto:guillem.escriba01@estudiant.upf.edu",
        'About': "# This is a *Data Science App* for the 10th Lab of Visual Analytics"
    }
)

# Home Page
st.title('🏠 HR Data Insights Home Page')

# Application Description
st.markdown("""
Welcome to HR Data Insights, the interactive web application designed to deliver in-depth analysis and predictions for HR consultancy firms. 
Our platform provides a comprehensive visualization of the technology industry's salary trends, enabling data-driven decision-making for both professionals and employers.
""")

# The Goal of the App
st.header('🎯 The Goal of the App')
st.write("""
The primary goal of this application is to:

- Offer an exploration tool that allows users to analyze through salary data based on various criteria such as country, experience, and education level.
- Provide a predictive feature that estimates potential salaries using a machine learning model trained on extensive survey data from the tech industry.
""")

# Explanation of the Dataset
st.header('📖 About the Dataset')
st.write("""
The dataset that powers this application is derived from the annual Stack Overflow Developer Survey. 
It includes responses from tens of thousands of developers across the globe and encompasses a variety of data points such as:

- Personal demographics
- Professional experience and education
- Employment type
- Programming languages proficiency
- Salary information

This rich dataset allows us to extract valuable trends and patterns that inform our predictive analytics.
""")

# Additional Comments
st.header('💡 Additional Comments')
st.write("""
Here are some things to keep in mind:

- The salary prediction is based on historical data and might not capture real-time changes in the job market.
- Data visualization is a powerful tool to understand complex data, but it's equally important to interpret these visualizations within the appropriate context.
- We encourage users to explore various filters and options to best understand the changes of the tech industry's salary landscape.
""")

# Footer
st.markdown("---")
st.subheader('Get Started')
st.write("Navigate to the 'Overview', 'Dynamic Visualization' and 'Salary Prediction' pages using the sidebar to begin your analysis.")