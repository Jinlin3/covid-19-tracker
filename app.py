import streamlit as st
import altair as alt
import pandas as pd

# Configures DataFrame and returns the DataFrame and list of countries in the dataset
@st.cache_data
def setup_data():
    df = pd.read_csv("owid-covid-data.csv")

    df["date"] = pd.to_datetime(df["date"]) # ensure datetime
    us_df = df[df["location"] == "United States"] # choose country
    us_df = us_df[["date", "total_cases"]].copy().reset_index(drop=True)
    return us_df

# Main function
def main():
    # Setup
    us_data = setup_data()
    
    hover = alt.selection_point(
        fields=["date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(us_data, title="Total COVID-19 Cases in the United States")
        .mark_line()
        .encode(
            x="date:T",
            y="total_cases:Q",
        )
    )

    points = lines.transform_filter(hover).mark_circle(size=65)

    tooltips = (
        alt.Chart(us_data)
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

    st.altair_chart(data_layer, use_container_width=True)

if __name__ == "__main__":
  main()