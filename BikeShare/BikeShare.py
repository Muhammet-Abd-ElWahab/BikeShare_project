import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_raw_data(df):
    """
    keep ask user if he want to see more five lines from raw data.
    INPUT:
    df: DataFrame after filteration
    OUTPUT:
    print 5 rows from raw data till user type 'No' or End of dataframe
    """
    show_data=True
    next_five=5
    df_shape=df.shape[0]

    while True:
        try:
            raw_data = input("Would you like to see the raw data? ").lower()
            if raw_data=="yes":
                print(df.iloc[0:5])
                if next_five>=df_shape:
                    print('-'*10,"End of Data",'-'*10)
                    show_data=False
                break
            elif raw_data=="no":
                show_data=False
                break
            else:
                raise ("invalid input")
        except:
            print("please type 'yes' or 'no'!")

    while show_data:

        try:
            next= input("Would you like to see 5 more rows? type 'Yes' or 'No' ").lower()
            if next=='yes':
                print(df.iloc[next_five:next_five+5])
                next_five+=5
                if next_five>=df_shape:
                    print('-'*10,"End of Data",'-'*10)
                    break
            elif next=='no':
                break
            else:
                raise ("invalid input")
        except:
            print("Please type 'Yes' or 'No' ")



def month_day_filter():
    """
    ask user to chose month & day to filter dataframe with.
    this function made to be called on get_filters function
    OUTPUT:
    it return the selected month and day.
    """
    while True:
        try:
            month = input("Which month - January, February, March, April, May,June or 'all'? ").lower()
            months={'january':0, 'february':1, 'march':2, 'april':3, 'may':4, 'june':5,'all':6}
            x=months[month]
            break

        except ValueError:
            print("ValueError!")
        except:
            print("Please enter a vaild Month!")

    while True:
        try:
            day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or 'all'? ").lower()
            days={'monday':0, 'tuesday':1, 'wednesday':2, 'thursday':3, 'friday':4, 'saturday':5, 'sunday':6,'all':7}
            x=days[day]
            break
        except ValueError:
            print("ValueError!")
        except:
            print("Please enter a vaild Day!")

    return month, day



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze
    for month and day i will call month_day_filter function.
    OUTPUT:
    city: str. selected city by user.
    month: str. selected month by user.
    day: str. selected day by user.
    return selected City, Month, and day.
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        try:
            city = input("Would you like to see data for Chicago, New York city or Washington? ").lower()
            cites={'chicago':0, 'new york city':1, 'washington':2}
            x=cites [city]
            break
        except ValueError:
            print("ValueError!")
        except:
            print("Please enter a vaild City name!")
    while True:
        try:
            filt_quest = input("Would you like to filter data by month & day? Type 'Yes' for apply filter and 'No' for no time filter ").lower()
            if filt_quest == "no":
                month="all"
                day="all"
                break
            elif filt_quest == "yes":
                month, day=month_day_filter()
                break
            else:
                raise ("invalid input")
        except:
            print("please type 'Yes' or 'No' ")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    INPUT:
    city: str. the city which user wanna see it's statistics.
    month: str. the month which user chose to filter data with.
    day: str. the day which user chose to filter data with.
    OUTPUT:
    df: DtaFrame for chosen city after filteration with selected month and day.

    """
    month=month.title()
    day=day.title()
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] =pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.day_name()
    if month != 'All':
        dic_of_month={'January':1,'February':2,'March':3, 'April':4, 'May':5, 'June':6}
        month = dic_of_month[month]
        df =df[df['Month']==month]
    if day != 'All':
        df =df[df['Day']==day]


    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    INPUT:
    df: DataFrame after filteration.
    OUTPUT:
    print the most common month, day and hour.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    com_month=df["Month"].mode()[0]
    month_dic={1:'January',2:'February',3:'March', 4:'April',5:'May',6:'June'}
    com_month=month_dic[com_month]
    print("the most common Month is: ", com_month.title())

    com_Day=df["Day"].mode()[0]
    print("the most common day of week is: ",com_Day.title())

    df["Hour"]=df["Start Time"].dt.hour
    com_hour=df["Hour"].mode()[0]
    print("the most common start hour is: ", com_hour)
    df=df.pop("Hour")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    INPUT:
    df: DataFrame after filteration.
    OUTPUT:
    print common start station, end station and most frequent
    combination from start to end station.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start_station=df["Start Station"].mode()[0]

    common_end_station=df["End Station"].mode()[0]

    df["St to End Station"]=df["Start Station"] + " to " + df["End Station"]
    common_comb_station = df["St to End Station"].mode()[0]

    print('most commonly used start station is: ',common_start_station)
    print('most commonly used end station is: ',common_end_station)
    print('most frequent combination of start & end station is: ',common_comb_station)
    df.pop("St to End Station")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    INPUT:
    df: DataFrame after filteration
    OUTPUT:
    print total travel time and average travel time in Seconds
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print("total travel time is: ", df["Trip Duration"].sum(), "Seconds.")
    print("mean travel time is: ", df["Trip Duration"].mean(), "Seconds.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.
    INPUT:
    df: DataFrame after filteration
    OUTPUT:
    print every user type count, gender count and
    earliest, most recent and most common birth year
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print(df["User Type"].value_counts())

    x= "Gender" in df
    if x== True:
        print(df["Gender"].value_counts())

    y="Birth Year" in df
    if y == True:
        print("Earliest year of birth is: ", int(df["Birth Year"].min()))
        print("Most recent year of birth is: ",int( df["Birth Year"].max()))
        print("Most common year of birth is: ",int(df["Birth Year"].mode()[0]))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)






def main():
    to_restart=True
    while to_restart:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        get_raw_data(df)

        while True:
            try:
                restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
                if restart == 'yes':
                    break
                elif restart == 'no':
                    to_restart=False
                    break
                else:
                    raise ("invalid input")

            except:
                print("please type 'Yes' or 'No' ")


if __name__ == "__main__":
	main()
