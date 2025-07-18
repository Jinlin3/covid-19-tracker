import streamlit as st
import altair as alt
import pandas as pd

# returns the DataFrame from the source .csv file
@st.cache_data
def load_data():
   df = pd.read_csv("owid-covid-data.csv")
   df["date"] = pd.to_datetime(df["date"]) # ensure datetime
   df = df.sort_values(by=["location", "date"])

   return df

# Main function
def main():
    st.title(body="Global :red[COVID-19] Tracker")
    st.markdown(":rainbow[By Jinlin3]")
    st.markdown("This dashboard displays graphical data regarding the spread of COVID-19 and its effects on populations across the globe.")

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
    selected_locations = st.multiselect(
        "Select one or more countries", options=locations, default=["United States"]
    )

    # user selects data
    selected_data = st.selectbox(label="What data do you want to view?", options=options, index=0)

    column_key = data_mapping[selected_data]

    # update df based on locations selected
    filtered_data = df[df["location"].isin(selected_locations)].copy()

    # trim the dataset columns to date, location, and the selected data
    filtered_data = filtered_data[["date", "location", column_key]].copy().reset_index(drop=True)
    
    # title
    chart_title = f"{selected_data} Comparison"

    # chart logic and coloring
    mark = alt.Chart(filtered_data, title=chart_title)
    match selected_data:
        case "Total Cases":
            mark = mark.mark_line()
        case "New Cases":
            mark = mark.mark_bar()
        case "Total Deaths":
            mark = mark.mark_line()
        case "New Deaths":
            mark = mark.mark_bar()

    # create chart
    chart = mark.encode(
        x=alt.X("date:T", title="Date", axis=alt.Axis(format="%Y", tickCount="year")),
        y=alt.Y(f"{column_key}:Q", title=selected_data),
        color=alt.Color("location:N", title="Country"),
        tooltip = [
           alt.Tooltip("date:T", title="Date"),
           alt.Tooltip(f"{column_key}:Q", title=selected_data),
           alt.Tooltip("location:N", title="Country")
        ]
    )

    # Render updated chart
    st.altair_chart(chart, use_container_width=True)

    # Download CSV button
    st.download_button(
        label="Download CSV",
        data=filtered_data.to_csv(index=False),
        file_name=f"{'_'.join(selected_locations)}_{column_key}.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
  main()