import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

def user_validation(userInput,inputType):
    """
    check the validity of user input.
    userInput: is the input of the user
    inputType: is the type of input: C = city, M = month, D = day   """
    
    while True : 
        input_read = input(userInput)
        try:
            if input_read in ['chicago', 'new york city', 'washington'] and inputType == 'C':
                break
            elif input_read in ['january', 'february', 'march', 'april', 'may', 'june', 'all'] and inputType == 'M':
                break
            elif input_read in ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'] and inputType == 'D':
                break
            else:
                if inputType == 'C':
                    print('invalid input, enter one of the following cites: chicago,new york city, or washington')
                if inputType == 'M':
                    print('invalid input, enter a month from january - june ')
                if inputType == 'D':
                    print('invalid input, enter any day from sunday - saturday or all.')
        except ValueError:
            print("Sorry you entered invalid data, please try again.")  
    return input_read.lower()
    
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city = user_validation("which city data would you like to explore? Chicago, New York, or Washington?",'C')
 
    month = user_validation("is there a specific month or all?",'M')
    day = user_validation("is there a specific day or all week?",'D')

    print('-' * 40)
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

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

    # TO DO: display the most common month
    Common_Month = df['month'].mode()[0]

    # TO DO: display the most common day of week
    Common_Day = df['month'].mode()[0]

    # TO DO: display the most common start hour
    Common_Hour = df['month'].mode()[0]

    print('Most Common Start Hour:', Common_Hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('Most Start Station:', start_station)

    # TO DO: display most commonly used end station
    end_station = df['End Station'].mode()[0]
    
    print('Most End Station:',end_station)
    
    # TO DO: display most frequent combination of start station and end station trip

    group_field = df.groupby(['Start Station', 'End Station'])
    combination_station = group_field.size().sort_values(ascending=False).head(1)
    print('Most frequent combination of Start Station and End Station trip:\n', combination_station)

    print("\nThis took %s seconds." % (time.time () - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    
    print('Total Travel Time:', total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    
    print ('Mean Travel Time:', mean_travel_time)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('User Type Stats:')
    print(df['User Type'].value_counts())
    if city !='washington':
        # Display counts of gender
        print ('Gender Stats:')
        print (df['Gender'].value_counts())
         # Display earliest, most recent, and most common year of birth
        print ('Birth Year Stats:')
        common_year = df['Birth Year'].mode()[0]
        print ('Most Common Year:', common_year)
        recent_year = df['Birth Year'].max()
        print ('Most Recent Year:', recent_year)
        earliest_year = df['Birth Year'].min()
        print ('Earliest Year:', earliest_year)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def DataDisplay(df):
    start_loc= 0 
    while(start_loc < len(df.index)):
        print(df.iloc[start_loc : start_loc+5])
        start_loc += 5
        view_display = input("Do you wish to continue?: ").lower()
        if view_display == 'no': 
            break
            
def main():
    while True:
        city,month,day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
        DataDisplay (df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
