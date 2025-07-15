import streamlit as st
import altair as alt
import pandas as pd

# returns the DataFrame from the source .csv file
@st.cache_data
def load_data():
   df = pd.read_csv("owid-covid-data.csv")
   df["date"] = pd.to_datetime(df["date"]) # ensure datetime
   df = df.sort_values(by=["location", "date"])

   # compute smoothing for total_cases and total_deaths
   to_smooth = {
       "total_cases": "total_cases_smoothed",
       "total_deaths": "total_deaths_smoothed"
   }
   
   for orig_col, smooth_col in to_smooth.items():
       if smooth_col not in df.columns:
           df[smooth_col] = df.groupby("location")[orig_col].transform(
               lambda x: x.rolling(window=7, min_periods=1).mean()
           )

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

    # Checkbox for smoothed data
    use_smoothed = st.checkbox("Show 7-day rolling average (smoothed data)")
    column_key = data_mapping[selected_data]
    if use_smoothed:
        column_key += "_smoothed"

    # update df based on location
    data = df[df["location"] == selected_location]

    # update df based on selected data
    data = data[["date", column_key]].copy().reset_index(drop=True)
    
    # title
    chart_title = f"{selected_data} in {selected_location}"
    if use_smoothed:
        chart_title += " (Smoothed)"

    # chart logic and coloring
    mark = alt.Chart(data, title=chart_title)
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
        y=alt.Y(f"{column_key}:Q", title=selected_data),
        tooltip = [
           alt.Tooltip("date:T", title="Date"),
           alt.Tooltip(f"{column_key}:Q", title=selected_data)
        ]
    )

    # Render updated chart
    st.altair_chart(chart, use_container_width=True)

    # Download CSV button
    st.download_button(
        label="Download CSV",
        data=data.to_csv(index=False),
        file_name=f"{selected_location}_{column_key}.csv",
        mime="text/csv"
    )


if __name__ == "__main__":
  main()