import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import os
from streamlit import components 
import seaborn as sns

# Specify the folder where the datasets are located
#folder_path = "datasets"

# List of dataset file names
#dataset_files = [
    #"by_constituency_2016_2022.csv",
    #"by_constituency_2015_2008.csv",
    #"by_constituency_2007_2000.csv",
    #"by_constituency_1999_1992.csv",
    #"by_constituency_1991_1982.csv"]

# Initialize an empty DataFrame to hold the merged data
#merged_data = pd.DataFrame()

# Loop through the list of dataset files and merge the data
#for file in dataset_files:
    #file_path = os.path.join(folder_path, file)
    #if os.path.exists(file_path):
        # Read the dataset, skipping the first column
        #df = pd.read_csv(file_path, usecols=lambda col: col != 'Unnamed: 0')
        # Merge the data into the combined DataFrame
        #merged_data = pd.concat([merged_data, df], axis=1)

# Save the merged data to a new CSV file
#merged_output_file = "merged_datasets.csv"
#merged_data.to_csv(merged_output_file, index=False)

#print("Merged dataset created and saved as", merged_output_file)

# Set favicon
favicon_path = "fav_icon.png"

st.set_page_config(
    page_title="Visible Mauritius",
    layout="wide",
    page_icon=favicon_path  # Set the favicon
)

# Read the dataset from the local folder into a DataFrame
file_path = "datasets/merged_datasets.csv"
df = pd.read_csv(file_path)

# Extract the unique years from the DataFrame
unique_years = df.columns[1:]

# Title and CSS styling
st.title("Visible Mauritius")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Select Year
selected_year = st.selectbox("Select a Year", unique_years, key="year_picker", format_func=lambda x: x, help="")

# Apply custom CSS to the select box
st.markdown(
    """
    <style>
        /* Reduce font size of select box */
        .Selectbox {
            font-size: 12px;
        }

        /* Adjust padding and margin to compact the select box */
        .Selectbox {
            padding: 4px 2px;
            margin: 0;
            width: 80px;  /* You can adjust the width as needed */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Check if a year has been selected before displaying the table
if selected_year:
    # Remove commas and convert to integers
    df[unique_years] = df[unique_years].replace({',': ''}, regex=True)
    df[unique_years] = df[unique_years].fillna('0').astype(int)
    
    # Calculate the sum of registered voters for the selected year
    total_registered_voters = df[selected_year].sum()
    
    # Display the total sum of registered voters for the selected year
    st.write(f"Total Registered Voters in {selected_year}: {total_registered_voters}")

    col1, col2 = st.columns(2)
    
    # Display the filtered DataFrame in the first column
    with col1:
        st.header(f"Registered Voters in {selected_year}")
        # Filter the DataFrame based on the selected year
        filtered_df = df[["Constituency Name", selected_year]]
        st.dataframe(filtered_df, height=400)
        
        # Display data source link with CSS styling
    st.markdown(
        "<p style='text-align:center; margin-top: 10px; font-size: 12px;'>"
        "Data Source: <a href='https://electoral.govmu.org/oec/?page_id=625' target='_blank'>Electoral Commission of Mauritius</a>"
        "</p>",
        unsafe_allow_html=True
    )

    # Filters for Comparative Analysis in the second column
    with col2:
        st.sidebar.header("Constituency Filters")
        # Select only 2 Constituencies for Comparison
        selected_constituencies = st.sidebar.multiselect("Select Constituencies (Max 2)", df["Constituency Name"], default=None, max_selections=2)
        
        # Display Plus/Minus Analysis and Bar Chart
        if len(selected_constituencies) == 2:
            constituency_a = selected_constituencies[0]
            constituency_b = selected_constituencies[1]
            
            voters_a = df[df["Constituency Name"] == constituency_a][selected_year].values[0]
            voters_b = df[df["Constituency Name"] == constituency_b][selected_year].values[0]
            
            voters_diff = voters_b - voters_a
            
            st.write(f"Difference in Registered Voters between {constituency_a} and {constituency_b}: {voters_diff}")
            
            # Create Bar Chart using Plotly
            fig = px.bar(df, x=[constituency_a, constituency_b], y=[voters_a, voters_b], labels={'x': 'Constituencies', 'y': 'Registered Voters'},
                         title='Registered Voters Comparison', color_discrete_sequence=['#FFFFFF', '#FFFFFF'])
            fig.update_traces(texttemplate='%{y}', textposition='outside')  # Display values on bars
            fig.update_layout(
                plot_bgcolor='#0E1117',  # Transparent background
                paper_bgcolor='#0E1117',  # Transparent background of the plot area
                font_color='#FFFFFF',  # Font color
                width=500,  # Width of the bar chart
                height=400,  # Height of the bar chart
                margin=dict(l=0, r=0, t=50, b=0)  # Margins to align with the data table
            )
            st.plotly_chart(fig)
            
# Select a Constituency for Evolution Analysis
selected_constituency_evolution = st.selectbox("Select a Constituency for Evolution Analysis", df["Constituency Name"], key="constituency_evolution_picker")

# Create a placeholder for the highlights
highlights_placeholder = st.empty()

# Display the evolution of registered voters for the selected constituency
if selected_constituency_evolution:
    # Filter the DataFrame based on the selected constituency
    constituency_data = df[df["Constituency Name"] == selected_constituency_evolution]
    # Extract years and corresponding registered voter data
    years = constituency_data.columns[1:]
    registered_voters = constituency_data.iloc[0, 1:].values
    
    # Create a line chart using Plotly Express
    fig_evolution = px.line(x=years, y=registered_voters, labels={'x': 'Year', 'y': 'Registered Voters'},
                            title=f"Evolution of Registered Voters for {selected_constituency_evolution}",
                            line_shape="linear")
    fig_evolution.update_layout(
        plot_bgcolor='#0E1117',  # Transparent background
        paper_bgcolor='#0E1117',  # Transparent background of the plot area
        font_color='#FFFFFF',  # Font color
        width=700,  # Width of the line chart
        height=400,  # Height of the line chart
        margin=dict(l=50, r=50, t=50, b=0)  # Margins
    )
    st.plotly_chart(fig_evolution)
    
    # Calculate the highlights (highest year, lowest year, and average value)
    highest_year = years[registered_voters.argmax()]
    lowest_year = years[registered_voters.argmin()]
    avg_registered_voters = registered_voters.mean()

    # Display the highlights next to each other
    col1, col2, col3 = highlights_placeholder.columns(3)
    with col1:
        st.markdown(f"<p style='font-size: 16px; font-weight: bold;'>Highest Year:</p><p style='font-size: 20px;'>{highest_year}</p>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<p style='font-size: 16px; font-weight: bold;'>Lowest Year:</p><p style='font-size: 20px;'>{lowest_year}</p>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<p style='font-size: 16px; font-weight: bold;'>Average Value:</p><p style='font-size: 20px;'>{avg_registered_voters:.2f}</p>", unsafe_allow_html=True)

else:
    st.warning("Please select a year to view the table.")

# Create a container for the footer
footer_container = st.container()

# Display footer text in the container
with footer_container:
    st.markdown(
        "<p style='text-align:center; margin-top: 20px; font-size: 10px;'>"
        "2023. Visible Mauritius. Developed with good intentions."
        "</p>",
        unsafe_allow_html=True
    )