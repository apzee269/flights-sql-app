import streamlit as st
from dbhelper import DB
import plotly.graph_objects as go
import plotly.express as px

db = DB()

st.sidebar.title('Flights Analytics')
user_option = st.sidebar.selectbox('Menu', ['Select One','Check Flights','Analytics'])

if user_option == 'Check Flights':
    st.title('Check Flights')
    col1, col2 = st.columns(2)
    city = db.fetch_city_names()

    with col1:
        source = st.selectbox('Source', sorted(city))
    with col2:
        destination = st.selectbox('Destination', sorted(city))
    if st.button('Search'):
        results = db.fetch_all_flights(source,destination)
        st.dataframe(results)

elif user_option == 'Analytics':
    airline,freq = db.fetch_airline_frequency()
    fig = go.Figure(
        go.Pie(
            labels = airline,
            values = freq,
            hoverinfo = "label+percent",
            textinfo= "value"
        ))
    st.header('Pie Chart')
    st.plotly_chart(fig)

    st.header('Bar Chart')
    city, freq1 = db.busy_airport()
    fig = px.bar(
        x = city,
        y = freq1
    )
    st.plotly_chart(fig,theme = "streamlit", use_container_width=True)

    st.header('Line Chart')
    date, freq2 = db.daily_freq()
    fig2 = px.line(
        x=date,
        y=freq2
    )
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

else:
    st.title('Tell about the project')

