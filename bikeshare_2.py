import time
import pandas as pd
import numpy as np

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
    while True:
        city = input("Input the city do you want to explore: Chicago, New York or Washington? \n> \n").lower()
        if city in CITY_DATA.keys():
            break

    # get user input for month (all, january, february, ... , june)
    month = input("To provide a month name:\n e.g. all, january, february, march, april, may, june\n").lower()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Input day of the week\n").lower()

    print('-'*40)
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
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    most_common_month = df['month'].mode()[0]

    # display the most common day of week
    df['day of week'] = df['Start Time'].dt.day_name()
    most_common_day_of_week = df['day of week'].mode()[0]

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    print("The most common month: {} \nThe most common day of week: {} \nThe most common start hour: {}".format(most_common_month, most_common_day_of_week, most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station :", most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station :", most_common_end_station)

    # display most frequent combination of start station and end station trip
    frequent_stations = df.groupby(['Start Station','End Station']).size().nlargest(1)
    for index, station in enumerate(frequent_stations):
        print("Most frequent start and end station {} \n".format(frequent_stations.index[index], station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time : {} seconds or {} years".format(total_travel_time,total_travel_time/(3600*24*365)))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time : %s seconds." % mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_user_types = df['User Type'].value_counts()
    print("Counts of user types ")
    for index, user_count in enumerate(counts_user_types):
        print("  {}: {}".format(counts_user_types.index[index], user_count))

    # Display counts of gender
    if 'Gender' in df.columns:
        counts_gender = df['Gender'].value_counts()
        print("\nCounts of gender ")
        for index, gender in enumerate(counts_gender):
            print("   {}: {}".format(counts_gender.index[index], gender))
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        print('\nThe earliest year of birth : ', earliest_year)
        most_recent_year = df['Birth Year'].max()
        print('\nThe most recent year of birth :', most_recent_year)
        most_common_year = df['Birth Year'].mode()[0]
        print('\nThe most common year of birth :', most_common_year)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays raw bikeshare data."""
    k = 0
    while True:
        ask_user = input('Would you want to see more raw data for the city selected? \nPrint yes or no: ')
        if ask_user == 'yes':
            k += 1 #Adds 1 to current value
            print(df.iloc[(k-1)*5:k*5])
        elif ask_user == 'no':
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
