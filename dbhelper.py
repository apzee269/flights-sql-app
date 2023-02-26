import mysql.connector

class DB:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='',
                database = 'indigo'
            )
            self.mycursor = self.conn.cursor()
            print("Connection Established")
        except:
            print('Connection Error')

    def fetch_city_names(self):
        city = []
        self.mycursor.execute("""
            SELECT DISTINCT Source FROM indigo.flights
            UNION
            SELECT DISTINCT destination FROM indigo.flights;
        """)
        data = self.mycursor.fetchall()
        for i in data:
            city.append(i[0])
        return city

    def fetch_all_flights(self,source,destination):
        self.mycursor.execute("""
            SELECT Airline,Route,Dep_time,Duration,Price FROM flights
            WHERE Source = '{}' AND Destination = '{}'
        """.format(source,destination))
        data = self.mycursor.fetchall()
        return data

    def fetch_airline_frequency(self):
        airline = []
        frequency = []
        self.mycursor.execute('''
            SELECT Airline, COUNT(*) FROM flights
            GROUP BY Airline
        ''')
        data = self.mycursor.fetchall()
        for item in data:
            airline.append(item[0])
            frequency.append(item[1])
        return airline,frequency

    def busy_airport(self):
        city = []
        frequency = []
        self.mycursor.execute("""
            SELECT Source,COUNT(*) FROM (SELECT Source FROM flights
                                         UNION ALL
                                         SELECT Destination FROM flights) t
            GROUP BY t.Source
            ORDER BY COUNT(*) DESC   
        """)
        data = self.mycursor.fetchall()
        for item in data:
            city.append(item[0])
            frequency.append(item[1])
        return city, frequency

    def daily_freq(self):
        date = []
        freq = []

        self.mycursor.execute("""
            SELECT Date_of_Journey, COUNT(*) FROM flights
            GROUP BY Date_of_Journey
        """)
        data = self.mycursor.fetchall()
        for item in data:
            date.append(item[0])
            freq.append(item[1])

        return date,freq