import numpy as np
import streamlit as st
from datetime import datetime, time
import pytz

"""
#  :globe_with_meridians: :calendar: Worldwide Event Manager

### Schedule and count down the worldwide events!
"""

#The preferred way of dealing with times is to always work in UTC, converting to localtime only when generating output to be read by humans.

st.sidebar.write("Put your event info")

your_tz = st.sidebar.selectbox(
    'Your time zone',
    ('US/Pacific', 'US/Arizona', 'US/Mountain', 'US/Central', 'US/Eastern', 'GMT', 'Europe/Berlin', 'Asia/Tokyo'),
    )

d = st.sidebar.date_input(f"Your event date in {your_tz}")
t = st.sidebar.time_input(f"Your event time in {your_tz}", time(10, 00))
event_dt = datetime.combine(d, t).astimezone(pytz.timezone(your_tz))
st.sidebar.write(f"Your event date and time: {event_dt.strftime('%Y:%m:%d %H:%M:%S')}")

def convert_tz(dt, tz):
    return dt.astimezone(pytz.timezone(tz))

selected_tz = st.multiselect(
    'Add time zones to convert',
    ['US/Pacific', 'US/Arizona', 'US/Mountain', 'US/Central', 'US/Eastern', 'GMT', 'Europe/Berlin', 'Asia/Tokyo'],
    ['US/Eastern', 'Asia/Tokyo'])

# Get the daylight saving time (DST offset) adjustment
# print(dt_us_central.dst())

st.subheader('Event time in other time zones')

output_tz = ""
for i in selected_tz:
    dt_tmp = convert_tz(event_dt, i)
    output_tz += i + ": " + str(dt_tmp.strftime('%m/%d %H:%M'))
    if i != selected_tz[-1]:
        output_tz += ", \n"
st.code(output_tz)

st.subheader('Countdown to your event')

dt_now = datetime.now(pytz.timezone(your_tz))
difference = event_dt - dt_now

days = difference.days
hours = difference.seconds // 3600
minutes = (difference.seconds%3600) // 60
seconds = difference.seconds%60

col1, col2, col3, col4 = st.columns(4)
col1.metric("DAYS", f"{days}")
col2.metric("HOURS", f"{hours}")
col3.metric("MINUTES", f"{minutes}")
col4.metric("SECONDS", f"{seconds}")