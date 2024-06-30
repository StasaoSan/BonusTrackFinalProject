import random
import string
from datetime import datetime, timedelta
# Параметризуемая часть
n_records = 10000 # Параметр отвечающий за число генерируемыз запросов импорта
filename = 'insert.sql' # параметр отвечаюший за имя генерируемого файла

# Основная часть кода
def random_string(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

def random_time():
    return (datetime.min + timedelta(minutes=random.randint(0, 1440))).time()

def generate_airports(n):
    airports = []
    for i in range(1, n + 1):
        airports.append(f"({i}, '{random_string(3)}', 'City{i}', 'Country{i}', '{random.uniform(-90, 90):.6f}, {random.uniform(-180, 180):.6f}')")
    return airports

def generate_airplanes(n):
    airplanes = []
    for i in range(1, n + 1):
        airplanes.append(f"({i}, 'Type{i}', '{random_string(5)}', {random.randint(1, 50)}, {random.randint(50, 300)})")
    return airplanes

def generate_seats(n):
    seats = []
    for i in range(1, n + 1):
        seats.append(f"({i}, {random.randint(1, n)}, 'Economy', {i})")
    return seats

def generate_passengers(n):
    passengers = []
    for i in range(1, n + 1):
        gender = random.choice(['M', 'F'])
        date_of_birth = random_date(datetime(1950, 1, 1), datetime(2003, 12, 31)).strftime('%Y-%m-%d')
        passengers.append(f"({i}, {random.randint(1, n)}, 'Name{i}', 'Surname{i}', 'Patronymic{i}', {random.randint(18, 70)}, '{date_of_birth}', '{gender}', {random.randint(100000, 999999)}, 'Passport')")
    return passengers

def generate_reservations(n):
    reservations = []
    for i in range(1, n + 1):
        reservations.append(f"({i}, {random.randint(1, n)}, {random.randint(1, n)}, 'Yes', 'Electronic', 'RUB')")
    return reservations

def generate_flights(n):
    flights = []
    for i in range(1, n + 1):
        time_departure = random_time()
        time_arrival = (datetime.combine(datetime.today(), time_departure) + timedelta(hours=random.randint(1, 5))).time()
        flights.append(f"({i}, {random.randint(1, n)}, {random.randint(1, n)}, {random.randint(1, n)}, '{time_departure}', '{time_arrival}', {random.randint(60, 300)}, {random.randint(500, 1500)})")
    return flights

def generate_users(n):
    users = []
    for i in range(1, n + 1):
        users.append(f"({i}, 'Username{i}', 'Password{i}', 'user{i}@example.com', 'User', '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}')")
    return users

def write_to_file(filename, data):
    with open(filename, 'w') as file:
        for table, values in data.items():
            file.write(f"INSERT INTO {table} VALUES\n")
            file.write(",\n".join(values) + ";\n\n")

if __name__ == "__main__":
    data = {
        'Airport(ID, Name, City, Country, Coordinates)': generate_airports(n_records),
        'Airplane(ID, Type, BortNumber, PersonalOnBoard, NumberOfSeats)': generate_airplanes(n_records),
        'Seat(ID, AirplaneID, SeatType, SeatNumber)': generate_seats(n_records),
        'Passenger(ID, UserID, Name, Surname, Patronymic, Age, DateOfBirthdate, Gender, SerialNumberDocument, TypeOfDocument)': generate_passengers(n_records),
        'Reservation(ID, SeatID, PassengerID, Insurance, TypeOfBill, PaymentCurrency)': generate_reservations(n_records),
        'Flight(ID, AirportDepartureID, AirportArrivalID, AirplaneID, TimeDeparture, TimeArrival, TimeOnBoard, RangeOfFlight)': generate_flights(n_records),
        'User(ID, Username, Password, E-Mail, Role, DateOfRegister)': generate_users(n_records)
    }
    write_to_file(filename, data)
