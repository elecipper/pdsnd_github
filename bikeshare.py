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

    input_choice_cities = ['chicago', 'new york city', 'washington']

    while True:
        city = input('Please select one of the following cities: chicago, new york city or washington')
        if city.lower() in input_choice_cities:
            break

    # get user input for month (all, january, february, ... , june)

    input_choice_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

    while True:
        month = input('Please choose a month from january to june (or type all)')
        if month.lower() in input_choice_months:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)

    input_choice_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

    while True:
        day = input('Please choose a day of the week from monday to sunday (or type all)')
        if day.lower() in input_choice_days:
            break

    print('-'*40)
    return city.lower(), month.lower(), day.lower()


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
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

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

    # display the most common month
    df['month'] = df['Start Time'].dt.month_name()
    popular_month = df['month'].value_counts().idxmax()
    print('Most Common Month:', popular_month)

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    popular_day_of_week = df['day_of_week'].value_counts().idxmax()
    print('Most Common Day of Week:', popular_day_of_week)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].value_counts().idxmax()
    print('Most Common Start Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().idxmax()
    print('Most Common Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts().idxmax()
    print('Most Common End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['Start-End Station'] = df['Start Station'] + ' + ' +df['End Station']
    popular_start_and_end = df['Start-End Station'].value_counts().idxmax()
    print('Most Common Start-End Station:', popular_start_and_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time#
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time:', total_travel_time)

    # display mean travel time
    total_travel_time = df['Trip Duration'].mean()
    print('The mean travel time:', total_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts().dropna()
    print(user_types)


#ATTENTION, HERE WE NEED TO DO SOMETHING TO ACCOUNT FOR NOT ALL CITIES HAVING GENDER INFORMATION, washington does not have the below information

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_types = df['Gender'].value_counts().dropna()
        print(gender_types)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth = df['Birth Year'].min()
        print("Earliest birth year: ", earliest_birth)
        latest_birth = df['Birth Year'].max()
        print("Most recent birth year: ",latest_birth)
        common_birth = df['Birth Year'].value_counts().idxmax()
        print("Most common birth year: ",common_birth)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        lines_to_display = 5
        current_index = 0
        show_more = 'yes'

        while show_more.lower() == 'yes':
            end_index = current_index + lines_to_display
            print(df.iloc[current_index:end_index])

            current_index = end_index

            show_more = input('Show 5 more lines? (yes/no): ')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
