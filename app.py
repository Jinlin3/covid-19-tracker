import pandas as pd
import matplotlib.pyplot as plt

def main():
  # Setup
  df = pd.read_csv("owid-covid-data.csv")
  list_of_countries = df["location"].unique().tolist()

  while(True):
    # User selects a country
    is_a_country = False
    print("Please select a country.")
    while (is_a_country == False):
      country = input()
      if (country not in list_of_countries):
        print("Please try again.")
      else:
          is_a_country = True

    print(f'You have selected {country}.')
    print(f'Here is covid data relating to {country}.')

    # Selecting specific country
    country_df = df[df["location"] == country].copy()
    # Converting date into datetime objects and sorting data by date
    country_df["date"] = pd.to_datetime(country_df["date"])
    country_df = country_df.sort_values(by="date")

    # Plot daily new cases
    plt.figure(figsize=(10,4))
    plt.plot(country_df["date"], country_df["new_cases"], label="New Cases", color="blue")
    plt.plot(country_df["date"], country_df["new_deaths"], label="New Deaths", color="red")
    plt.title(f"Daily COVID-19 Cases and Deaths in {country}")
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
  main()