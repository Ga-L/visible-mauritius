import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import os
from streamlit import components

# Specify the folder where the datasets are located
folder_path = "datasets"

# List of dataset file names
dataset_files = ["detailed_results_for_all_constituencies_2019.csv"]

# Set favicon
favicon_path = "fav_icon.png"

# Define variables for filters
enable_party_filter = False
enable_community_filter = False

st.set_page_config(
    page_title="Visible Mauritius",
    layout="wide",
    page_icon=favicon_path  # Set the favicon
)

# Read the SVG image as binary
with open("logo.svg", "rb") as svg_file:
    svg_binary = svg_file.read()

# Convert the binary data to base64
import base64
svg_base64 = base64.b64encode(svg_binary).decode()

# Display the logo using HTML
st.markdown(
    f"""
    <div style="display: flex; align-items: center;">
        <img src="data:image/svg+xml;base64,{svg_base64}" width="85">
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown('<style>div.block-container{padding-top:3rem;}</style>', unsafe_allow_html=True)

# Read the dataset from the local folder into a DataFrame
file_path = "datasets/detailed_results_for_all_constituencies_2019.csv"
df = pd.read_csv(file_path, encoding='ISO-8859-1')

# Create a main container to hold the content of both columns
main_container = st.container()

# Reference the custom CSS file
st.markdown(
    """
    <style>
    @import url('style.css'); /* Replace 'style.css' with the actual path to your CSS file */
    </style>
    """,
    unsafe_allow_html=True
)

# Create a two-column layout within the main container
col1, col2 = main_container.columns(2)

# Add a constituency selection dropdown in col1
with col1:
    # Apply the custom font in your content
    st.markdown("<h2 style='font-family: Montserrat, sans-serif; font-weight: 700; font-size: 20px;'>Results for 2019 General Elections</h2>", unsafe_allow_html=True)
    selected_constituency = st.selectbox("Select a Constituency", df['Constituencies'].unique())

    # Filter the dataset based on the selected constituency
    constituency_data = df[df["Constituencies"] == selected_constituency]
    
with col1:
    # Add a card for Number of Candidates
    num_candidates = constituency_data["SURNAME AND OTHER NAMES"].count()
    st.markdown(
        f"<div style='background-color: #8ad1ba; border-radius: 5px; padding: 10px;'>"
        f"<p style='font-size: 16px; color: white; margin: 0;'><strong>Number of Candidates in {selected_constituency}:</strong> {num_candidates}</p>"
        "</div>",
        unsafe_allow_html=True
    )
    
    # Add checkboxes for filtering
    enable_party_filter = st.checkbox("Enable filter by Political party")
    enable_community_filter = st.checkbox("Enable filter by community")
    
    # Move the Number of Candidates card to col1

    # Filter by Political party if enabled
    if enable_party_filter:
        selected_parties = st.multiselect("Select Political Parties", df["PARTY"].unique(), key="party_selector")
        constituency_data = constituency_data[constituency_data["PARTY"].isin(selected_parties)]

    # Filter by Community if enabled
    if enable_community_filter:
        selected_communities = st.multiselect("Select Communities", df["COMMUNITY"].unique(), key="community_selector")
        constituency_data = constituency_data[constituency_data["COMMUNITY"].isin(selected_communities)]

    # Create a search bar in col1 (above the filters) only if both filters are not enabled
    if not (enable_party_filter or enable_community_filter):
        search_term = st.text_input("Search by Name, Community, or Party")
    else:
        search_term = ""  # Hide the search bar when filters are checked

# Search functionality
if search_term:
    search_term = search_term.lower()  # Convert the search term to lowercase for case-insensitive search
    filtered_data = constituency_data[
        constituency_data.apply(lambda row: search_term in str(row["SURNAME AND OTHER NAMES"]).lower() or
                                    search_term in str(row["COMMUNITY"]).lower() or
                                    search_term in str(row["PARTY"]).lower(), axis=1)
    ]
    if not filtered_data.empty:
        st.markdown(
            f"Search results for '{search_term}' in {selected_constituency} Constituency:",
            unsafe_allow_html=True
        )
        # Apply custom CSS to remove spacing on top
        st.markdown('<style>div[data-testid="stDataFrame"] div:first-child { margin-top: 0; }</style>', unsafe_allow_html=True)
        st.dataframe(filtered_data)  # Display the search results
    else:
        st.warning(f"No results found for '{search_term}' in {selected_constituency} Constituency")
else:
    # Display the results for the selected constituency
    if not constituency_data.empty:
        # Drop the "Constituencies" column from the result
        constituency_data = constituency_data.drop(columns=["Constituencies"])
        st.markdown(
            f"Results for {selected_constituency} Constituency:",
            unsafe_allow_html=True
        )
        # Apply custom CSS to remove spacing on top
        st.markdown('<style>div[data-testid="stDataFrame"] div:first-child { margin-top: 0; }</style>', unsafe_allow_html=True)
        st.dataframe(constituency_data)  # Display the dataframe without specifying width and height
    else:
        st.warning("Please choose appropriate filters for the selected Constituency")

with col2:
    st.markdown("<h2 style='font-size: 20px; margin-bottom: 0;'><br></h2>", unsafe_allow_html=True)
    community_ratio = constituency_data["COMMUNITY"].value_counts(normalize=True)
    
    # Define custom colors
    custom_colors = ['#FF7751', '#FFC23D', '#0EB9CB', '#027381']

    # Create a pie chart with custom colors
    fig1 = px.pie(
        community_ratio,
        values=community_ratio,
        names=community_ratio.index,
        color_discrete_sequence=custom_colors  # Apply custom colors
    )

    # Update the layout and display the chart
    fig1.update_layout(width=325, height=325)  # Adjust the width and height as needed
    st.plotly_chart(fig1, use_container_width=True)

# Create a container for the footer
footer_container = st.container()

# Display footer text in the container
with footer_container:
    st.markdown(
        "<div style='text-align: left; width: 80%; margin: 0 auto; font-size: 10px;'>"
        "Disclaimer: While Visible Mauritius endeavors to ensure the information on this website is as current and precise as possible, Visible Mauritius makes no assertions or warranties regarding the accuracy and comprehensiveness of the data on this site and explicitly disclaims responsibility for any errors and omissions in the contents of this site.</div>"
        "<div style='text-align: center; margin-top: 20px; font-size: 12px;'>"
        "2023. Visible Mauritius. Developed with good intentions.</div>",
        unsafe_allow_html=True
    )
