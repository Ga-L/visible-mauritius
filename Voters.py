import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import os
from streamlit import components

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


# Specify the folder where the datasets are located
folder_path = "datasets"

# List of dataset file names
dataset_files = [
    "by_constituency_2016_2022.csv",
    "by_constituency_2015_2008.csv",
    "by_constituency_2007_2000.csv",
    "by_constituency_1999_1992.csv",
    "by_constituency_1991_1982.csv"]

# Initialize an empty DataFrame to hold the merged data
merged_data = pd.DataFrame()

# Loop through the list of dataset files and merge the data
for file in dataset_files:
    file_path = os.path.join(folder_path, file)
    if os.path.exists(file_path):
        # Read the dataset, skipping the first column
        df = pd.read_csv(file_path, usecols=lambda col: col != 'Unnamed: 0')
        # Merge the data into the combined DataFrame
        merged_data = pd.concat([merged_data, df], axis=1)

# Save the merged data to a new CSV file
merged_output_file = "merged_datasets.csv"
merged_data.to_csv(merged_output_file, index=False)

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
dataset_path = 'datasets/voters_electors_by_election.csv'
df2 = pd.read_csv(dataset_path)

# Extract the unique years from the DataFrame
unique_years = df.columns[1:]

# Title and CSS styling
st.title("Visible Mauritius")
st.subheader("Voters Data")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

# Create a two-column layout
col1, col2 = st.columns(2)

# Display the "Registered Voters in 2023" header and "Select a Year" picker in col1
with col1:
    st.markdown("<h2 style='font-size: 25px;'>Registered Voters 2023</h2>", unsafe_allow_html=True)

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

        # Display the filtered DataFrame in col1
        filtered_df = df[["Constituency Name", selected_year]]
        st.dataframe(filtered_df, height=400)

        # Display data source link with CSS styling
        st.markdown(
            "<p style='text-align:center; margin-top: 10px; font-size: 12px;'>"
            "Data Source: <a href='https://electoral.govmu.org/oec/?page_id=625' target='_blank'>Electoral Commission of Mauritius</a>"
            "</p>",
            unsafe_allow_html=True
        )
                 # Add a separator line
        st.markdown("---")  # Inserts a horizontal rule

# Display the "Difference in Registered Voters by constituency" subtitle in col2
with col2:
    st.markdown("<h2 style='font-size: 25px;'>Difference in Registered Voters</h2>", unsafe_allow_html=True)

    # Select only 2 Constituencies for Comparison
    selected_constituencies_comparison = st.multiselect("Select Constituencies (Max 2)", df["Constituency Name"], default=None, max_selections=2, key="comparison_multiselect")

    if len(selected_constituencies_comparison) == 2:
        constituency_a = selected_constituencies_comparison[0]
        constituency_b = selected_constituencies_comparison[1]

        voters_a = df[df["Constituency Name"] == constituency_a][selected_year].values[0]
        voters_b = df[df["Constituency Name"] == constituency_b][selected_year].values[0]
        difference = voters_a - voters_b  # Calculate the difference

        # Create Bar Chart using Plotly
        fig = px.bar(df, x=[constituency_a, constituency_b], y=[voters_a, voters_b], labels={'x': 'Constituencies', 'y': 'Registered Voters'},
                     title=f'Registered Voters Comparison\nDifference: {difference}', color_discrete_sequence=['#FFFFFF', '#FFFFFF'])
        fig.update_traces(texttemplate='%{y}', textposition='outside')  # Display values on bars
        fig.update_layout(
            plot_bgcolor='#0E1117',  # Transparent background
            paper_bgcolor='#0E1117',  # Transparent background of the plot area
            font_color='#FFFFFF',  # Font color
            width=475,  # Width of the bar chart
            height=500,  # Height of the bar chart
            margin=dict(l=0, r=0, t=50, b=0)  # Margins to align with the data table
        )
        st.plotly_chart(fig)
    

    
# Select a Constituency for Evolution Analysis
st.markdown("<h2 style='font-size: 25px;'>Select a Constituency for Evolution Analysis</p>", unsafe_allow_html=True)
selected_constituency_evolution = st.selectbox("", df["Constituency Name"], key="constituency_evolution_picker")

# Add a checkbox for toggling the comparative feature
toggle_comparative_checkbox = st.checkbox("Toggle Comparative Feature")

# Create a placeholder for the new constituency picker
new_constituency_picker_placeholder = st.empty()

# Create a placeholder for the highlights
highlights_placeholder = st.empty()

# Create a placeholder for the evolution of registered voters graph
evolution_graph_placeholder = st.empty()

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
                            line_shape="linear",
                            color_discrete_sequence=["#4CAF50"])  # Specify a color for the main line
    fig_evolution.update_layout(
        plot_bgcolor='#0E1117',  # Transparent background
        paper_bgcolor='#0E1117',  # Transparent background of the plot area
        font_color='#FFFFFF',  # Font color
        width=800,  # Width of the line chart
        height=400,  # Height of the line chart
        margin=dict(l=50, r=50, t=50, b=0),  # Margins
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)  # Legend position
    )
    
    # Set the legend label for the main line
    fig_evolution.data[0].name = selected_constituency_evolution
    
    evolution_graph_placeholder.plotly_chart(fig_evolution)
    
     # Initialize variables for highest and lowest years
    highest_year_selected = years[registered_voters.argmax()]
    lowest_year_selected = years[registered_voters.argmin()]
    
      # Initialize avg_registered_voters outside the conditional block
    avg_registered_voters = registered_voters.mean()

    # Check if the comparative feature checkbox is checked
    if toggle_comparative_checkbox:
        # Hide the highlights placeholder
        highlights_placeholder.empty()
        # Create a placeholder for the table
        table_placeholder = st.empty()

        # Display a new constituency picker for comparative analysis
        new_constituency = new_constituency_picker_placeholder.selectbox("Select a Constituency for Comparative Analysis", df["Constituency Name"], key="new_constituency_picker")

        # Create a dynamic title for comparative analysis
        if new_constituency:
            # Change the title based on the selected constituencies
            comparative_title = f"Comparative {selected_constituency_evolution} & {new_constituency}"
            fig_evolution.update_layout(title=comparative_title)  # Update the graph title

            voters_new = df[df["Constituency Name"] == new_constituency][years].values[0]

            # Add the comparative line to the chart
            fig_evolution.add_scatter(x=years, y=registered_voters, mode="lines",
                          name=selected_constituency_evolution,  # Label for the blue line
                          line=dict(color="#4CAF50"))  # Specify color for the blue line
            
            fig_evolution.add_scatter(x=years, y=voters_new, mode="lines",
                                      name=new_constituency,  # Set the name for the legend
                                      line=dict(color="#2196F3"))  # Specify a different color for the comparative line
            evolution_graph_placeholder.plotly_chart(fig_evolution)

            # Calculate the average value for the selected constituency
            avg_registered_voters_new = voters_new.mean()

        # Display a table for the data of the selected constituencies
            data_table = pd.DataFrame({
            selected_constituency_evolution: [highest_year_selected, lowest_year_selected, round(avg_registered_voters)],
            new_constituency: [years[voters_new.argmax()], years[voters_new.argmin()], round(avg_registered_voters_new)]
        }, index=['Highest Year', 'Lowest Year', 'Average Value'])

            # Display the table in the same column as the graph
            with table_placeholder:
                st.table(data_table)
    else:
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
    
# Load the Excel file for voters vs turnouts
@st.cache_resource  # Cache the loaded data for improved performance
def load_data(file_path):
    xls = pd.ExcelFile(file_path)
    data = {}
    for sheet_name in xls.sheet_names:
        data[sheet_name] = pd.read_excel(file_path, sheet_name=sheet_name)
    return data

# Main function
def main():
    
    
    # Adding a subtitle using markdown
    st.markdown("### Electors, Voters, and Valid Votes Breakdown")

    # Load data from the Excel file
    file_path = "datasets/voters_electors_by_election_1983_2019.xlsx"  # Update with your file path
    data = load_data(file_path)

    # Create a list of available years (sheet names)
    available_years = list(data.keys())
    selected_year = st.selectbox("Select a Year", available_years)

    # Enable Filters checkbox
    enable_filters = st.checkbox("Enable Filters")

    # Define the specified column names as filters
    specified_filters = [
        'Electors',
        'Voters',
        'Valid votes',
    ]

    if enable_filters:
        # Allow the user to select filters
        selected_filters = st.multiselect("Select Filters", specified_filters, default=specified_filters)

        # Check if the selected year exists in the data dictionary
        if selected_year in data:
            selected_data = data[selected_year]

            # Check if the selected filters exist in the DataFrame's columns
            existing_columns = selected_data.columns
            selected_filters = [filter for filter in selected_filters if filter in existing_columns]

            # Filter by constituencies
            selected_constituencies = st.multiselect("Select Constituencies", selected_data['Constituencies'])

            if selected_filters:
                # Apply filters to the data
                selected_data = selected_data[selected_data['Constituencies'].isin(selected_constituencies)]

                # Create a single bar chart for all selected filters
                if not selected_data.empty:
                    fig = px.bar(selected_data, x='Constituencies', y=selected_filters,
                                 title=f'Selected Filters by Constituency')
                    st.plotly_chart(fig)
                # No need to display a message if there's no data to show
            else:
                # No selected filters exist in the data for the selected year.
                st.warning("No selected filters exist in the data for the selected year.")

    else:
        # If Enable Filters is not checked, display the data without any filtering
        if selected_year in data:
            selected_data = data[selected_year]
            st.write(f"Data for {selected_year}:")
            st.write(selected_data)
        else:
            st.warning("Please select a year to view the data.")

if __name__ == "__main__":
    main()

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
    

    
