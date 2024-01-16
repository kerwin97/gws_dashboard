import streamlit as st
import pandas as pd
import plotly.express as px
import os


@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    # Additional data preprocessing if needed
    return df


def draw_graph(df, spinner_name, y_col, title):
    # Create a time graph using plotly express
    with st.spinner(spinner_name):
        fig_temp = px.line(df, x='DateTimeColumn', y=y_col,
                           color='Sensor ID', title=title)

    # Make the chart responsive
    st.plotly_chart(fig_temp, use_container_width=True)


@st.cache_data
def overall_view(df):
    st.title("Overview")
    st.write("An Overview of Time Series")

    # Convert the datetime column to datetime format if needed
    with st.spinner("Cleaning Data..."):
        df['DateTimeColumn'] = pd.to_datetime(
            df['DateTime'] + ' ' + df['DateTime2'])
    df = df.sort_values(by='DateTimeColumn')

    draw_graph(df, "Creating Moisture plot...",
               'Moisture Point (%)', 'Moisture Time Series')

    draw_graph(df, "Creating Brightness plot...",
               'Brightness (%)', 'Brightness Time Series')

    draw_graph(df, "Creating Temp plot...",
               'Temperature', 'Temperature Time Series')


def select_by_sensorID(df):
    st.title("Select by Sensor ID")
    st.write("Select a Sensor ID to look into the details")

    # Dropdown menu to select a category
    selected_category = st.selectbox(
        "Select a Category", df['Sensor ID'].unique())

    # Filter the DataFrame based on the selected category
    filtered_df = df[df['Sensor ID'] == selected_category]

    # Display the filtered data
    st.write("Filtered Data:")
    st.write(filtered_df)

    with st.spinner("Cleaning Data..."):
        filtered_df['DateTimeColumn'] = pd.to_datetime(
            filtered_df['DateTime'] + ' ' + filtered_df['DateTime2'])
    filtered_df = filtered_df.sort_values(by='DateTimeColumn')

    draw_graph(filtered_df, "Creating Moisture plot...",
               'Moisture Point (%)', 'Moisture Time Series')

    draw_graph(filtered_df, "Creating Brightness plot...",
               'Brightness (%)', 'Brightness Time Series')

    draw_graph(filtered_df, "Creating Temp plot...",
               'Temperature', 'Temperature Time Series')


def filter_by_plant_type(df):
    st.title("Multi Select Plant Type")
    st.write("Multi Select the Plant Types")
    # First column, first row
    col1, col2 = st.columns([1, 1])

    # Dropdown menu to select multiple categories
    selected_categories_1 = col1.multiselect(
        "Select Plant 1 Type", df['Plant 1 Type'].unique())

    # Dropdown menu to select multiple categories
    selected_categories_2 = col2.multiselect(
        "Select Plant 2 Type", df['Plant 2 Type'].unique())

    # Filter the DataFrame based on the selected categories
    filtered_df = df[df['Plant 1 Type'].isin(
        selected_categories_1)]
    filtered_df = filtered_df[filtered_df['Plant 2 Type'].isin(
        selected_categories_2)]

    # Display the filtered data
    st.write("Filtered Data:")
    st.write(filtered_df)

    with st.spinner("Cleaning Data..."):
        filtered_df['DateTimeColumn'] = pd.to_datetime(
            filtered_df['DateTime'] + ' ' + filtered_df['DateTime2'])
    filtered_df = filtered_df.sort_values(by='DateTimeColumn')

    draw_graph(filtered_df, "Creating Moisture plot...",
               'Moisture Point (%)', 'Moisture Time Series')

    draw_graph(filtered_df, "Creating Brightness plot...",
               'Brightness (%)', 'Brightness Time Series')

    draw_graph(filtered_df, "Creating Temp plot...",
               'Temperature', 'Temperature Time Series')


def main():
    st.title("GWS Dashboard")
    st.write("Monitor Soil Conditions")

    data_file = "data/soilSensorData.csv"
    df = load_data(data_file)

    # Remove unnamed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    df["Temperature"] = pd.to_numeric(df["Temperature"], errors='coerce')
    df["Moisture Point (%)"] = pd.to_numeric(
        df["Moisture Point (%)"], errors='coerce')
    df["Brightness (%)"] = pd.to_numeric(df["Brightness (%)"], errors='coerce')

    # Display the DataFrame
    st.write("### DataFrame:")
    st.write(df)
    st.write(df.describe())

    # Create a sidebar with tab options
    selected_tab = st.sidebar.selectbox(
        "Select Tab", ["Overall", "Select Sensor", "Select Type"])

    # Render content based on the selected tab
    if selected_tab == "Overall":
        overall_view(df)
    elif selected_tab == "Select Sensor":
        select_by_sensorID(df)
    elif selected_tab == "Select Type":
        filter_by_plant_type(df)


if __name__ == "__main__":
    main()
