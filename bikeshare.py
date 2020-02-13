import time
import pandas as pd
import numpy as np
from tabulate import tabulate

#Show all columns of the grid
pd.set_option('display.max_columns', None)

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#Create a list each for the cities, months, days of week, and time of day.  They will be used as index values
months= ['january', 'february', 'march', 'april', 'may', 'june']
days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
time_of_day= ['12 AM','1 AM','2 AM','3 AM','4 AM','5 AM','6 AM','7 AM','8 AM','9 AM','10 AM','11 AM',
            '12 PM','1 PM','2 PM','3 PM','4 PM','5 PM','6 PM','7 PM','8 PM','9 PM','10 PM','11 PM']
    
def get_filters():

    print('Hello! Let\'s explore some US bikeshare data!')

    #Declare city, month, and day as global variables, so they can be seen outside th scope of this function
    global city
    global month
    global day
    
    #Obtain input for city
    city= input('\nWould you like to see bike statistics for Chicago, New York City, or Washington? ').lower()
    
    #If the input is not one of the 3 cities in the list, then initiate a while loop 
    while city not in ['chicago', 'new york city', 'washington']:
            city = input('That was not a valid choice.  Would you like to see bike statistics for Chicago, New York City, or Washington? ').lower()

    print('\nYou have chosen bike statistics for the great city of {}!'.format(city.title()))
    time.sleep(1)

    filter_date= input('\nWould you like to filter by Month, Day, or both (enter \'none\' for no filter)? ').lower()
    #If the input is not month, day, both, or none initiate a while loop
    while filter_date not in ['month','day','both','none']:
            filter_date= input('\nThat is not a valid choice.  Would you like to filter by Month, Day, or both (enter \'none\' for no filter)? ').lower()
    
    #Create a conditional flow based on the input for the date filter
    #If the input is both
    if filter_date == 'both':
        month= input('\nPlease enter the month to filter by (January thru June): ').lower()
        
        #If the input is not all or one of the months in the list, then initiate a while loop
        while month not in months:
            month= input('That was not a valid choice. Please enter the month to filter by: ').lower()
        day= input('\nPlease enter the day of week to filter by: ').lower()
        #If the input is not all or one of the days of the week in the list, then initiate a while loop
        while day not in days_of_week:
                day= input('That was not a valid choice.  Please enter the day of week to filter by: ').lower()
                
    #If the input is month         
    elif filter_date == 'month':
        month= input('\nPlease enter the month to filter by: ').lower()
        #If the input is not all or one of the months in the list, then initiate a while loop
        while month not in months:
            month= input('That was not a valid choice. Please enter the month to filter by: ').lower()
        day= 'all'

    #If the input is day
    elif filter_date == 'day':
        day= input('\nPlease select the day of week to filter by: ').lower()
        #If the input is not all or one of the days of the week in the list, then initiate a while loop
        while day not in days_of_week:
                day= input('That was not a valid choice.  Please enter the day of week to filter by: ').lower()
        month= 'all'

    #If the input is none
    elif filter_date == 'none':
        month= 'all'
        day= 'all'

    if filter_date in ['month','day','both']:
        print('\nApplying filter now...')
        print('*'*80)
        time.sleep(1)

    else:
        print('*'*80)
        
    return city, month, day


def load_data(city, month, day):

    #Load the csv into a dataframe based on the city inputed by user
    df= pd.read_csv(CITY_DATA[city])

    #Convert the Start Time column to a datetime type in order to extract time components
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Create two new columns month and day_of_week that store the month and day of week as integers, respectively
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    #If month is not all, then filter the dataframe to only include data for the month inputed by user
    if month!= 'all':
        #Converts the month into an integer based on the index in the months list
        month = months.index(month.lower()) + 1
        df = df[df['month'] == month]

    #If day of week is not all, then filter the dataframe to only include data for the month inputed by user
    if day!= 'all':
        #Converts the day of week into an integer based on the index in the days_of_week list
        day= days_of_week.index(day.lower())
        df = df[df['day_of_week'] == day]
            
    return df
    

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('Calculating The Most Frequent Times of Travel...\n')
    time.sleep(2)
    start_time = time.time()

    #Only calculate most popular month if a specific month is not inputed by user
    if month== 'all':
        #Uses the mode method on the month column to extract the most occurring value
        popular_month= months[df['month'].mode()[0]-1]
        print('Most popular month: {}'.format(popular_month.title()))

    #Only calculate most popular month if a specific monnth is not inputed by user
    if day== 'all':
        #Uses the mode method on the day_of_week column to extract the most occurring value
        popular_day= days_of_week[df['day_of_week'].mode()[0]].title()
        print('Most popular day: {}'.format(popular_day))

    #Creates a new column called hour that stores the hour value of Start Time as integer
    df['hour']= df['Start Time'].dt.hour

    #Uses the mode method on the hour column to extract the most occurring value
    popular_hour= time_of_day[df['hour'].mode()[0]]
    print('Most popular time of day: {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*80)

  

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('Calculating The Most Popular Stations and Trip...\n')
    time.sleep(2)
    start_time = time.time()

    #Uses the mode method on the Start Station column to extract the most occurring value
    popular_start_station = df['Start Station'].mode()[0]
    print('Most popular start station: {}'.format(popular_start_station))

    #Uses the mode method on the End  Station column to extract the most occurring value
    popular_end_station= df['End Station'].mode()[0]
    print('Most popular end station: {}'.format(popular_end_station))

    #Create a new column called Start & End Station that concatenates the values of Start and End station in order to find the most occurring combo
    df['Combo Station']= 'Start Station: ' + df['Start Station'] + '\n\t ' + 'End Station: ' + df['End Station']
    #Uses the mode method on the Start & End Station column to extract the most occurring value
    popular_start_end_station= df['Combo Station'].mode()[0]
    print('Most popular combo of start and end stations:\n\t {}'.format(popular_start_end_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*80)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('Calculating Trip Duration...\n')
    time.sleep(2)
    start_time = time.time()

    #Stores the sum of the values in Trip Duration column in a variable called total_time
    total_time = df['Trip Duration'].sum()
    
    print('Total duration: {}s'.format(total_time))

    #Stores the mean of the value in Trip Duration column in a variable called avg_time
    avg_time= df['Trip Duration'].mean()
    print('Average duration: {}s'.format(avg_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*80)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('Calculating User Stats...\n')
    time.sleep(2)
    start_time = time.time()

    user_types= df['User Type'].value_counts()
    print('User type:\n{}'.format(user_types))

    #Checks if the Gender column exists in the dataframe.  If it does, then it counts the values in the column and then groups together by those values
    if 'Gender' in df.columns:
        gender= df['Gender'].value_counts()
        print('\nGender:\n{}'.format(gender))
    else:
        print('\nI\'m sorry but there are no Gender stats for the city of {}.'.format(city.title()))

    #Converts the Birth Year from a string to number
    #Checks if the Birth Year column exists in the dataframe.  If it does, then it counts the values in the column and then groups together by those values
    if 'Birth Year' in df.columns:
        df['Birth Year']=  pd.to_numeric(df['Birth Year'])
        #Uses the min method to find the lowest occurring value
        dob_earliest= df['Birth Year'].min()
        #Uses the max method to find the highest occurring value
        dob_latest= df['Birth Year'].max()
        #Uses the mode method to find the most occurring value
        dob_common= df['Birth Year'].mode()[0]
        print('\nBirth Year:')
        print('Earliest: {}'.format(int(dob_earliest)))
        print('Most recent: {}'.format(int(dob_latest)))
        print('Most common: {}'.format(int(dob_common)))
    else:
        print('\nI\'m sorry but there are no Birth Year stats for the city of {}.'.format(city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*80)

def raw_data(df):

    answer= input('Would you like to see individual data? Enter yes or no. ').lower()

    #Enter conditional flow if first answer is yes
    if answer == 'yes':
        #Drop some of the columns that were appended to the dataframe in order to do calculations.  Also dropped the first column with id values as they are not useful
        df.drop([df.columns[0],'month','day_of_week','hour','Combo Station'],axis='columns',inplace=True)
        i=0
        #Use the tabulat function of the tabulate model to display the dataframe as a fancy grid.  It looks nicer!
        print('\n',tabulate(df.iloc[i:i+5],headers=df.columns,tablefmt='fancy_grid'))
        #Enter while loop and only remain if answer is yes
        while answer == 'yes':
            i+= 5
            answer= input('\nWould you like to see more data? Enter yes or no. ').lower()
            #If the answer is not yes, then break from the loop immediately
            if answer!= 'yes': break
            print('\n',tabulate(df.iloc[i:i+5],headers=df.columns,tablefmt='fancy_grid'))

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no. ').lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
	main()
