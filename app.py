import streamlit as st
import altair as alt
import pandas as pd

# returns the DataFrame corresponding to user selected country
@st.cache_data
def load_data():
   df = pd.read_csv("owid-covid-data.csv")
   df["date"] = pd.to_datetime(df["date"]) # ensure datetime
   return df

# Main function
def main():
    st.title(body="COVID-19 Cases per Country")
    st.markdown("This dashboard displays confirmed COVID-19 cases from 2020 to 2024.")
    # Setup
    df = load_data()
    locations = df["location"].unique().tolist()
    
    # user selects location
    default_index = locations.index("United States")
    selected_location = st.selectbox(label="Choose a country", options=locations, index=default_index)
    data = df[df["location"] == selected_location] # updated df based on location
    data = data[["date", "total_cases"]].copy().reset_index(drop=True)

    # hover logic
    hover = alt.selection_point(
        fields=["date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    # altair chart
    lines = (
        alt.Chart(data, title=f"Total COVID-19 Cases in {selected_location}")
        .mark_line()
        .encode(
            x=alt.X("date:T", title="Date", axis=alt.Axis(format="%Y", tickCount="year")),
            y=alt.Y("total_cases:Q", title="Total Cases")
        )
    )

    # points when hovering
    points = lines.transform_filter(hover).mark_circle(size=65)

    # tooltips when hovering
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="date:T",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("date:T", title="Date"),
                alt.Tooltip("total_cases:Q", title="Total Cases"),
            ],
        )
        .add_params(hover)
    )

    data_layer = lines + points + tooltips

    # Render updated chart
    st.altair_chart(data_layer, use_container_width=True)

if __name__ == "__main__":
  main()