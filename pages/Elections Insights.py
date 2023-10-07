import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import os
from streamlit import components

# Specify the folder where the datasets are located
folder_path = "datasets"

# List of dataset file names
dataset_files = [ "detailed_results_for_all_constituencies_2019.csv"]

# Set favicon
favicon_path = "fav_icon.png"

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

# Create a two-column layout
col1, col2, = st.columns(2)

with col1:
    st.markdown("<h2 style='font-size: 20px;'>Results for 2019 General Elections</h2>", unsafe_allow_html=True)

# Add a constituency selection dropdown in col1
selected_constituency = col1.selectbox("Select a Constituency", df['Constituencies'].unique())

# Add checkboxes for filtering

enable_party_filter = col1.checkbox("Enable filter by Political party")
enable_community_filter = col1.checkbox("Enable filter by community")

# Filter the dataset based on the selected constituency
constituency_data = df[df["Constituencies"] == selected_constituency]

# Filter by Political party if enabled
if enable_party_filter:
    selected_parties = col1.multiselect("Select Political Parties", df["PARTY"].unique(), key="party_selector")
    constituency_data = constituency_data[constituency_data["PARTY"].isin(selected_parties)]
    # Hide the search bar
    search_term = ""

# Filter by Community if enabled
if enable_community_filter:
    selected_communities = col1.multiselect("Select Communities", df["COMMUNITY"].unique(), key="community_selector")
    constituency_data = constituency_data[constituency_data["COMMUNITY"].isin(selected_communities)]
    # Hide the search bar
    search_term = ""

# Create a search bar in col2
with col2:
    st.markdown("<h2 style='font-size: 20px;'><br>" "</h2>", unsafe_allow_html=True)
    if enable_party_filter or enable_community_filter:
        st.write("Search bar can't be used when filters are active.")
        search_term = ""
    else:
        search_term = st.text_input("Search by Name, Community, or Party")
        
    

# Search functionality
if search_term:
    search_term = search_term.lower()  # Convert the search term to lowercase for case-insensitive search
    filtered_data = constituency_data[
        constituency_data.apply(lambda row: search_term in str(row["SURNAME AND OTHER NAMES"]).lower() or
                                           search_term in str(row["COMMUNITY"]).lower() or
                                           search_term in str(row["PARTY"]).lower(), axis=1)
    ]
    if not filtered_data.empty:
        st.write(f"Search results for '{search_term}' in {selected_constituency} Constituency:")
        st.dataframe(filtered_data)  # Display the search results
    else:
        col1.warning(f"No results found for '{search_term}' in {selected_constituency} Constituency")
else:
    # Display the results for the selected constituency
    if not constituency_data.empty:
        # Drop the "Constituencies" column from the result
        constituency_data = constituency_data.drop(columns=["Constituencies"])
        st.write(f"Results for {selected_constituency} Constituency:")
        st.dataframe(constituency_data)  # Display the dataframe taking full width
    else:
        col1.warning("Please choose appropriate filters for the selected Constituency")


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

