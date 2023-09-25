import time
import pandas as pd
import numpy as np
import random

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    time.sleep(1)
    print("Do you want to explore data for Chicago, New York City or Washington?")

    # while loop that secures correct user input
    while True:
        city = input("> ").lower()
        if city not in ["chicago", "new york city", "washington"]:
            print("Error! Please write the city name exactly as given.")
            continue
        else:
            break

    # gives user feedback of their choice
    print()
    print(f"You chose {city.capitalize()}!")
    print()

    # get user input for month (all, january, february, ... , june)
    time.sleep(1)
    print("What month do you want to explore? Please choose a month in the timeframe from January to June.")
    print("If you don't want to filter by month type 'all'.")

    # while loop that secures correct user input
    while True:
        month = input("> ").lower()
        if month not in ["all", "january", "february", "march", "april", "may", "june"]:
            print("Error! Please write the month correctly!")
            continue
        else:
            break
    print()

    # gives user feedback of their choice
    if month == "All":
        print("You selected all months.")
    else:
        print(f"You chose {month.capitalize()}!")
    print()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    time.sleep(1)
    print("What day of the week do you want to explore? Type 'Monday', 'Tuesday' (...) 'Sunday'.")
    print("If you don't want to filter by day type 'all'.")

    # while loop that secures correct user input
    while True:
        day = input("> ").lower()
        if day not in ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            print("Error! Please write a correct day!")
            continue
        else:
            break
    print()

    # gives user feedback of their choice
    if day == "All":
        print("You selected all days.")
    else:
        print(f"You chose {day.capitalize()}!")
    time.sleep(2)
    print('-'*40)

    # return variables to main function
    return city, month, day

def load_data(city, month, day):

    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month if applicable, skipped if user selected all
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1  # +1 because months are 1-based

        # Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        # Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    # return filtered dataframe
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # List of month names for conversion
    month_names = ['January', 'February', 'March', 'April', 'May', 'June']

    # display the most common month
    popular_month = df['month'].mode()[0]
    popular_month_name = month_names[popular_month - 1]
    popular_month_count = df['month'].value_counts().iloc[0]
    print(f"The most popular month is {popular_month_name} with {popular_month_count} occurrences!")

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    popular_day_count = df['day_of_week'].value_counts().iloc[0]
    print(f"The most popular day is {popular_day} with {popular_day_count} occurrences!")

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    popular_hour_count = df['hour'].value_counts().iloc[0]
    print(f"The most popular starting hour is {popular_hour} with {popular_hour_count} occurrences!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_station_start = df['Start Station'].mode()[0]
    popular_station_start_count = df['Start Station'].value_counts().iloc[0]
    print(f"The most popular start station is {popular_station_start} with {popular_station_start_count} occurrences!")

    # display most commonly used end station
    popular_station_end = df['End Station'].mode()[0]
    popular_station_end_count = df['End Station'].value_counts().iloc[0]
    print(f"The most popular end station is {popular_station_end} with {popular_station_end_count} occurrences!")

    # display most frequent combination of start station and end station trip
    df["Combination_Stations"] = df['Start Station'] + ' to ' + df['End Station']
    popular_station_combo = df['Combination_Stations'].mode()[0]
    popular_station_combo_count = df['Combination_Stations'].value_counts().iloc[0]
    print(f"The most popular station combination is {popular_station_combo} with {popular_station_combo_count} occurrences!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = (df['Trip Duration'].sum() / 60) / 60
    print(f"The total travel time is: {round(total_travel, 2)} hours or {round(total_travel/24, 2)} days!")

    # display mean travel time
    mean_travel = df['Trip Duration'].mean() / 60
    print(f"The average travel time is: {round(mean_travel, 2)} minutes!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("User Types:")
    for index, value in user_types.items():
        print(f"  {index}: {value}")
    print()

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print("Gender count:")
        for index, value in gender_count.items():
            print(f"  {index}: {value} ")
        print()

    else:
        print("Gender data is not available for this city.")
        print()

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        min_birth = int(df['Birth Year'].min())
        print(f"The earliest birth year is {min_birth}!")

        recent_birth = int(df['Birth Year'].max())
        print(f"The most recent birth year is {recent_birth}!")

        most_common_birth = int(df['Birth Year'].mode()[0])
        print(f"The most common year of birth is {most_common_birth}!")
        print()

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
        print()
    else:
        print("Birth year data is not available for this city.")
        print()

def raw_data(df):
    '''
    Asks the user if he wants to see the raw data. Shows 5 at a time and can be
    repeated.
    '''

    print("Do you want to see some raw data? Type 'yes' or 'no'.")
    raw = input("> ").lower()

    #Set index to show the first 5 rows.
    start_index = 0
    end_index = 5
    while raw == 'yes':
        # Check if there is more data to show
        if start_index >= len(df):
            print("No more data to display.")
            break

        #Show the first 5 rows
        print(df.iloc[start_index:end_index])

        #change the index
        start_index += 5
        end_index += 5

        #ask user if he wants to see the next 5 rows
        print("Do you want to see the next 5 rows? Answer 'yes' or 'no'.")
        raw = input("> ").lower()

    print("Bringing you back to main menu...")
    time.sleep(1)

def main():
    while True:
        city, month, day = get_filters()

        df = load_data(city, month, day)

        time_stats(df)

        station_stats(df)

        trip_duration_stats(df)

        user_stats(df)

        raw_data(df)

        print()
        print()
        print("Filter Summary: ")
        print(f"City: {city}, Month: {month}, Day of the week: {day}.")
        print()
        print("Shape: ")
        print(df.shape)
        print()

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
