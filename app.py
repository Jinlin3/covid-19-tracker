import pandas as pd

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
    print(df[df["location"] == country].head(n=20))

if __name__ == "__main__":
  main()