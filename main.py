import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

from streamlit import components 


#Set favicon
favicon_path = "fav_icon.png"

st.set_page_config(
    page_title="Visible Mauritius",
    layout="wide",
    page_icon=favicon_path  # Set the favicon
)

# Read the dataset from the local folder into a DataFrame
file_path = "datasets/by_constituency_2016_2022.csv"
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
    # Calculate the sum of registered voters for the selected year
# Calculate the sum of registered voters for the selected year
    total_registered_voters = df[selected_year].replace({',': ''}, regex=True).astype(int).sum()
    
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
            
            df[unique_years] = df[unique_years].replace({',': ''}, regex=True).astype(int)
            
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