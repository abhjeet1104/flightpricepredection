import streamlit as st
import pandas as pd
import numpy as np
import pickle
import datetime

rf = pickle.load(open('rf.pkl','rb'))

st.title(':blue[Flight Fare Prediction] ✈️')

airline_name = ['IndiGo', 'Air India', 'Jet Airways', 'SpiceJet',
           'Multiple carriers', 'GoAir', 'Vistara', 'Air Asia',
           'Vistara Premium economy', 'Jet Airways Business',
           'Multiple carriers Premium economy']

source = ['Banglore', 'Kolkata', 'Delhi', 'Chennai', 'Mumbai']
destinaton = ['Delhi', 'Banglore', 'Cochin', 'Kolkata', 'Hyderabad']
stopage = ['non-stop', '1 stop','2 stops', '3 stops', '4 stops']

airline = st.selectbox('Airline',sorted(airline_name))

col1,col2,col3 = st.columns(3)
with col1 :
    departure_date = st.date_input('Departure Date',min_value=datetime.date(2023,1,1))
with col2 :
    hour=[i for i in range(0,25)]
    departure_hour = st.selectbox('Departure Hour',hour)
with col3 :
    minute = [i for i in range(0, 61)]
    departure_min = st.selectbox('Departure minute', minute)

col4,col5,col6 = st.columns(3)
with col4 :
    arrival_date = st.date_input('Arrival Date',min_value=datetime.date(2023,1,1))
with col5 :
    hour=[i for i in range(0,25)]
    arrival_hour = st.selectbox('Arrival Hour',hour)
with col6 :
    minute = [i for i in range(0,61)]
    arrival_min = st.selectbox('Arrival minute',minute)

col7,col8 = st.columns(2)
with col7 :
    source = st.selectbox("Source", sorted(source))
with col8 :
    destination = st.selectbox('Destination',sorted(destinaton))

stopage = st.selectbox("Stopage",stopage)

if arrival_date >= departure_date:
    time = datetime.datetime(arrival_date.year,arrival_date.month,arrival_date.day,arrival_hour,arrival_min)-datetime.datetime(departure_date.year,departure_date.month,departure_date.day,departure_hour,departure_min)
    total_duration_mins = time.days*24*60 + time.seconds/60
else :
    st.warning("Arrival Date should be Higher! ")

airline_dict={'SpiceJet': 0,
        'Air Asia': 1,
         'IndiGo': 2,
         'GoAir': 3,
         'Vistara': 4,
         'Vistara Premium economy': 5,
         'Air India': 6,
         'Multiple carriers': 7,
         'Multiple carriers Premium economy': 8,
         'Jet Airways': 9,
         'Jet Airways Business': 10}

source_dict = {'Chennai': 0, 'Mumbai': 1, 'Banglore': 2, 'Kolkata': 3, 'Delhi': 4}

destination_dict = {'Kolkata': 0, 'Hyderabad': 1, 'Delhi': 2, 'Banglore': 3, 'Cochin': 4}

stop_dict = {
            'non-stop' : 0,
            '1 stop' : 1,
            '2 stops' : 2,
            '3 stops' : 3,
            '4 stops' : 4
                      }
try :
    if st.button(':red[Predict Price]'):
        input = pd.DataFrame(
                    {'Airline':[int(airline.replace(airline,str(airline_dict[airline])))],
                     'Source':[int(source.replace(source,str(source_dict[source])))],
                     'Destination':[int(destination.replace(destination,str(destination_dict[destination])))] ,
                     'Total_Stops': [int(stopage.replace(stopage,str(stop_dict[stopage])))],
                     'Date_of_Journey_day' : [departure_date.day],
                     'Date_of_Journey_month' : [departure_date.month],
                     'Dep_hour':[departure_hour],
                     'Dep_min':[departure_min],
                     'Arrival_Time_hour' :[arrival_hour],
                     'Arrival_Time_min' :[arrival_min],
                     'total_duration_mins' :[total_duration_mins]
                     }
                )


        result = rf.predict(input)

        st.header(f'Flight Price is Rs. {round(result[0],2)}')
except Exception as e:
    print(e)



