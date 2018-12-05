"""
bikeshare_template.py
"""

import time
import pandas as pd
import numpy as np

city_list = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
month_list = [1,2,3,4,5,6,7,8,9,10,11,12]
filter_list = ['MONTH','DAY','NONE','BOTH']
day_list = [1,2,3,4,5,6,7]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Get user input for city (chicago, new york city, washington). 
    print('Would you like to see data for Chicago, New York or Washington?')
    city = input('Enter city: ')
    while city.lower() not in city_list:
       print('Please choose from the given cities- Chicago, New York or Washington.')
       city = input('Enter city: ')

    # Use entered city to get filename from dictionary
    city_file = city_list.get(city.lower())
    print('Picked city is', city.title()) 
    # city now contains the city file name
    city = city_file  
         
    # Get user input to filter by month, day , none or both
    print('\nWould you like to filter the data by month, day, both or none?')
    filter = input('Enter filter by: ')
    while filter.upper() not in filter_list:
       filter = input('Please enter month, day, both or none: ')

    if filter == 'none':
       print('No filter')
    else:
       print('Picked filter is by',filter)
       
    filter_by = filter.upper()
    
    # initialized filters to NULL
    month = ''
    day   = ''
    
    # Get user input for month  ( 1 for Jan, 2 for feb...12 for Dec) 
    if filter_by in ('MONTH','BOTH'):
       while month not in month_list:
         month = input('Please choose from the following (1=Jan, 2=Feb, 3=March,...,12=Dec): ')
         if month.isdigit():
            month = int(month)
       print('You picked the month of ', get_month_name(month)) 

    # The user input for day of week (e.g. 1 for Mon, 2 for Tue ... 7 for Sun)
    if filter_by in ('DAY','BOTH'): 
       while day not in day_list:
         day = input ('Please choose which day of the week (1=Mon, 2=Tue,...,7=Sun): ')
         if day.isdigit():
            day = int(day)

       day = day - 1 # Adjustment of day made - Python first day of the week is 0 for Monday,1 for Tuesday, etc.
       print('You picked', get_day_of_week(day))  

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
        filter - month, day, none or both
    """
#    try:
#        os.path.isfile(city)
    df = pd.read_csv(city)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df_month = df['Start Time'].dt.month
    df_weekday = df['Start Time'].dt.weekday
    #df['hour'] = df['Start Time'].dt.hour
    
    # set filter
    filter = 'none'
    if month is  '' and day is '':
       df_filter  = df_month != 0
       filter = 'none'
    elif month is not '' and day is '':
       df_filter  = df_month == month
       if df[df_filter].empty:
          print('No data found for the month of',get_month_name(month))
       filter = 'month'
    
    elif day is not '' and month is '':
       df_filter  = df_weekday == day
       if df[df_filter].empty:
          print('Day:',day)
          print('No data found for',get_day_of_week(day))
       filter = 'day'
    
    elif month is not '' and day is not '':
       df_filter  = (df_month == month) & (df_weekday == day)
       if df[df_filter].empty:
          print('No data found for filter - both')
       filter = 'both'
       
    return df[df_filter], filter

   
def get_month_name(month_in):
    """ Gets the corresponding month  for an  entered integer for month """
    month_data = pd.Series(data = ['January','February','March','April','May','June','July','August','September','October','November','December'], index = [1,2,3,4,5,6,7,8,9,10,11,12])
    month_name = month_data[month_in]
    return month_name; 
    
def get_day_of_week(day_in):
    """ Gets the corresponding day for an entered integer for day  """
    day_data = pd.Series( data = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'],index = [0,1,2,3,4,5,6])
    day_name = day_data[day_in]
    return day_name;

def time_stats(df, month, day, filter):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df1 = df.copy()
    df1['Start Time'] = pd.to_datetime(df1['Start Time'])
    df1['month'] = df1['Start Time'].dt.month
    df1['weekday'] = df1['Start Time'].dt.weekday
    df1['hour'] = df1['Start Time'].dt.hour
    
    df_month = df1['Start Time'].dt.month
    df_weekday = df1['Start Time'].dt.weekday
    df_hour = df1['Start Time'].dt.hour
    
    
    if filter == 'none':
       # TO DO: display the most common month
       month_mode = df_month.mode()[0]
       month_count = df1.groupby('month').count() # get record count of most common month
       print('Most common month:',get_month_name(month_mode),'| Count:',month_count.loc[month_mode,'Start Time'],'| Filter:',filter)
       # TO DO: display the most common day of week
       weekday_mode = df_weekday.mode()[0]
       weekday_count = df1.groupby('weekday').count() # get record count of most common day of week
       print('Most common day of the week:',get_day_of_week(weekday_mode),'| Count: ',weekday_count.loc[weekday_mode,'Start Time'],'| Filter:',filter)
    elif filter == 'month':
       weekday_mode = df_weekday.mode()[0]
       weekday_count = df1.groupby('weekday').count() # get record count of most common day of week
       print('Most common day of the week:',get_day_of_week(weekday_mode),'| Count: ',weekday_count.loc[weekday_mode,'Start Time'],'| Filter:',filter)
        

    # TO DO: display the most common start hour
    hour_mode = df_hour.mode()[0]
    hour_count = df1.groupby('hour').count() # get record count of most common hour
    print('Most common start hour: ',hour_mode,'| Count:',hour_count.loc[hour_mode,'Start Time'],'| Filter:',filter)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df,filter):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station_mode = df['Start Station'].mode()[0]
    start_station_count = df.groupby('Start Station').count()
    print('Most common Start Station:',start_station_mode,'| Count:',start_station_count.loc[start_station_mode,'Start Time'],'| Filter:',filter)

    # TO DO: display most commonly used end station
    end_station_mode = df['End Station'].mode()[0]
    end_station_count = df.groupby('End Station').count()
    print('Most common End Station:  ',end_station_mode,'| Count:',end_station_count.loc[end_station_mode,'Start Time'],'| Filter:',filter)

    # TO DO: display most frequent combination of start station and end station trip
    df1 = df['Start Station'] +' - '+ df['End Station']
    station_mode = df1.mode()[0]
    df1  = df[df['Start Station'] +' - '+ df['End Station']== station_mode]
    station_count = df1.count()
    print('Most common Start-End Station:',station_mode,'| Count:',station_count.loc['Start Time'],'| Filter:',filter)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df,filter):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

   # TO DO: display total travel time
    tot_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:',tot_travel_time,'| Filter:',filter)

   # TO DO: display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print('Average Time:',avg_travel_time,'| Filter:',filter)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,filter):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('Counts of each User Type:')
    print(df.groupby('User Type').count().loc[:,'Unnamed: 0'])
    print('')

    # TO DO: Display counts of gender
    print('Counts of each Gender:')
    if {'Gender'}.issubset(df.columns):
       print(df.groupby('Gender').count().loc[:,'Unnamed: 0'])
    else:
       print('Gender data do not exist for this city')
    print('')

    # TO DO: Display earliest, most recent, and most common year of birth
    print('Counts of earliest, most recent, most common year of birth:')
    if {'Birth Year'}.issubset(df.columns):
       min_birth_yr = df['Birth Year'].min()
       max_birth_yr = df['Birth Year'].max()
       mode_birth_yr = df['Birth Year'].mode()[0]
       print('Earliest Birth Year:',int(df['Birth Year'].min()))
       print('Most recent Birth Year:',int(df['Birth Year'].max()))
       print('Most most common Birth Year:',int(df['Birth Year'].mode()[0]))
    else:
       print('Birth Year data do not exist for this city')
    print('')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_data(df):
    """Displays raw data of bikeshare users. Limits to 5 rows at a time"""
    display = input('\nDo you want to display raw data? Enter yes or no.\n')
    i = 0
    while display.lower() == 'yes':
       print(df[i:i+5])
       i = i + 5
       display = input('\nDisplay more data? Enter yes or no.\n')
       
def main():
    while True:
        city, month, day = get_filters()
        df, filter = load_data(city, month, day)

        if df.empty:
           print('')#continue
        else:
           time_stats(df, month, day, filter)
           station_stats(df, filter)
           trip_duration_stats(df, filter)
           user_stats(df, filter)
           print_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
