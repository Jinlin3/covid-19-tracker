import streamlit as st
import altair as alt
import pandas as pd

# returns the DataFrame from the source .csv file
@st.cache_data
def load_data():
   df = pd.read_csv("owid-covid-data.csv")
   df["date"] = pd.to_datetime(df["date"]) # ensure datetime
   return df

# Main function
def main():
    st.title(body=":red[COVID-19] Cases per Country")
    st.markdown(":rainbow[By Jinlin3]")
    st.markdown("This dashboard displays confirmed COVID-19 cases throughout the years of the pandemic.")

    # Setup
    df = load_data()

    locations = df["location"].unique().tolist()

    options = [
       "New Cases",
       "Total Cases",
       "New Deaths",
       "Total Deaths"
    ]

    data_mapping = {
       "New Cases":"new_cases",
       "Total Cases":"total_cases",
       "New Deaths":"new_deaths",
       "Total Deaths":"total_deaths"
    }
    
    # user selects location
    default_locations_index = locations.index("United States")
    selected_location = st.selectbox(label="Choose a location", options=locations, index=default_locations_index)

    # user selects data
    default_selected_data_index = options.index("New Cases")
    selected_data = st.selectbox(label="What data do you want to view?", options=options, index=default_selected_data_index)

    data = df[df["location"] == selected_location] # updated df based on location
    data = data[["date", data_mapping[selected_data]]].copy().reset_index(drop=True)
    
    # chart logic and coloring
    mark = alt.Chart(data, title=f"{selected_data} in {selected_location}")
    match selected_data:
        case "Total Cases":
            mark = mark.mark_line(color="lightgreen")
        case "New Cases":
            mark = mark.mark_bar(color="blue")
        case "Total Deaths":
            mark = mark.mark_line(color="crimson")
        case "New Deaths":
            mark = mark.mark_bar(color="orange")

    chart = mark.encode(
        x=alt.X("date:T", title="Date", axis=alt.Axis(format="%Y", tickCount="year")),
        y=alt.Y(f"{data_mapping[selected_data]}:Q", title=selected_data),
        tooltip = [
           alt.Tooltip("date:T", title="Date"),
           alt.Tooltip(f"{data_mapping[selected_data]}:Q", title=selected_data)
        ]
    )

    # Render updated chart
    st.altair_chart(chart, use_container_width=True)

if __name__ == "__main__":
  main()