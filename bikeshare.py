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
    city = input("Which city are you interested in: Chicago, New York City, or Washington? ").lower()
    while city not in ["chicago", "new york city", "washington"]:
        city = input("Please choose a city from this list: Chicago, New York City, or Washington? ").lower()
        
    # get user input for month (all, january, february, ... , june)
    month = input("Which month are you interested in? Please enter a month between January and June, or All! ").lower()
    while month not in ["all", "january", "february", "march", "april", "may", "june"]:
        month = input("That seems to throw an error: please enter a month between January and June, or All! ").lower()
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Which day of the week are you interested in? Choose either a specific day or All! ").title()
    while day not in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "All"]:
        day = input("Unfortunately, that didn't seem to work; please choose a specific day of the week or All! ").title()
    
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
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'All':
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day = days.index(day)
        df = df[df['day_of_week'] == day]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    months = ['january', 'february', 'march', 'april', 'may', 'june']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # display the most common month
    most_popular_month = df['month'].mode()[0]
    print("The most popular month is: ",months[most_popular_month-1].title())
    
    # display the most common day of week
    most_popular_day = df['day_of_week'].mode()[0]
    print("The most popular day of the week is: ",days[most_popular_day])
    
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_popular_hour = df['hour'].mode()[0]
    print("The most popular hour is: ",most_popular_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_popular_start = df['Start Station'].mode()[0]
    print("The most popular station to begin a trip is: ",most_popular_start)
    
    # display most commonly used end station
    most_popular_end = df['End Station'].mode()[0]
    print("The most popular station to end a trip is: ",most_popular_end)
    
    # display most frequent combination of start station and end station trip
    most_popular_trip = df.groupby(['Start Station','End Station']).size().sort_values(ascending=False)[0:1]
    print("The most popular trip is shown below: \n",most_popular_trip)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print("The total time traveled, in seconds, is: ",total_time)
    
    # display mean travel time
    avg_time = df['Trip Duration'].mean().round(2)
    print("The average time traveled per trip, in seconds, is: ",avg_time)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Following are counts of each User Type: \n",user_types)
    
    # Display counts of gender
    try:
        genders = df['Gender'].value_counts(dropna=True)
        print("Following are counts of each Gender: \n",genders)
    except:
        print("Unfortunately, gender information is not available for this city; apologies for the inconvenience!")
    
    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year = df['Birth Year'].min()
        print("The oldest person who has taken a rideshare trip was born in: ",int(earliest_year))
    
        most_recent_year = df['Birth Year'].max()
        print("The youngest person who has taken a rideshare trip was born in: ",int(most_recent_year))
   
        most_common_year = df['Birth Year'].mode()[0]
        print("The most common birth year of individuals who have taken a rideshare trip is: ",int(most_common_year))
    except:
        print("Unfortunately, birth year information is not available for this city; apologies for the inconvenience!")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays raw data upon user request, and continues until the user no longer wants to view additional data."""
    
    row_counter = 0
    display = input("Would you like to display 5 rows of raw data? (Y/N) ").title()
    while display == "Y":
        print("Good choice! Raw data is fun! \n",df.iloc[row_counter:row_counter+5])
        row_counter += 5
        display = input("Would you like to display 5 more rows of raw data? (Y/N) ").title()
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? (Y/N)\n').title()
        if restart.lower() != 'Y':
            break

if __name__ == "__main__":
	main()
