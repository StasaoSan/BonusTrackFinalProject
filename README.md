# BonusTrackFinalProject

## Содержание
- [Описание предметной области](#описание-и-цель-проекта)
- [ER-диаграмма](#er-диаграмма)
- [Скрипты](#скрипты)
  - [Скрипт создания таблиц](#скрипт-создания-таблиц)
  - [Скрипт заполнения таблиц данными](#скрипт-заполнения-таблиц-данными)
  - [Скрипт заполнения таблиц из CSV файлов](#скрипт-заполнения-таблиц-из-csv-файлов)
  - [Примеры запросов](#примеры-запросов)
- [Описание таблиц и их полей](#описание-таблиц-и-их-полей)
  - [Таблица 1: Airport](#таблица-1-airport)
  - [Таблица 2: Airplane](#таблица-2-airplane)
  - [Таблица 3: Flight](#таблица-3-flight)
  - [Таблица 4: Passenger](#таблица-4-passenger)
  - [Таблица 5: Seat](#таблица-5-seat)
  - [Таблица 6: Reservation](#таблица-6-reservation)
  - [Таблица 7: User](#таблица-7-user)
- [Скрипт для генерации SQL запросов заполнения таблиц](#скрипт-для-генерации-sql-запросов-заполнения-таблиц)



Описание и цель проекта: <br>
Цель проекта - проектирование архитектуры БД для сайта авиакомпании, где будет производиться выбор и покупка авиабилетов. 
В качестве референса был выбран сайт https://www.aeroflot.ru/. Данный ресурс используется для выбора и бронирования авиабилетов в любом из возможных направлений на любую из возможных дат. Моделирование охватывает область бронирования билетов, а именно: этам от выбора возможных рейсов между двумя аэропортами, выбор даты этих рейсов, и выбор времени вылета. Выбор авиакомпании я не рассматриваю, так как это не является целью поставленной мной задачи.
Считается, что на одни и те же направления могут летать различные самолеты, различные рейсы.

# ER-диаграмма:

<img width="468" alt="image" src="https://github.com/StasaoSan/BonusTrackFinalProject/assets/113228941/563e4635-a61d-43e6-9f93-19ba6f1409cd">

Так же данная диаграмма доступна для открытия в программе Visual Paradigm (файл diagramm.vpp)

## Скрипты

### Скрипт создания таблиц

Данный скрипт можно найти в файле `create.sql`.

### Скрипт заполнения таблиц данными

Скрипт заполнения таблиц данными, сгенерированными программой, написанной мной (ее описание можно посмотреть [ниже](#скрипт-для-генерации-sql-запросов-заполнения-таблиц)), можно найти в файле `insert.sql`.

### Скрипт заполнения таблиц из CSV файлов

Также есть второй вариант заполнения таблиц, если у вас есть уже созданные и заполненные необходимыми данными CSV файлы. В таком случае можно использовать скрипт `insertCSV.sql`. Примеры CSV файлов можно найти в папке `srcCSVs`.

### Примеры запросов
- Найти все рейсы, которые выполнялись между двумя конкретными городами в заданный период времени.
```sql
SELECT Flight.* FROM Flight
JOIN Airport AS Departure ON Flight.AirportDepartureID = Departure.ID
JOIN Airport AS Arrival ON Flight.AirportArrivalID = Arrival.ID
WHERE Departure.City = 'Moscow'
AND Arrival.City = 'Saint-Petersburg'
AND Flight.TimeDeparture BETWEEN '2023-01-01' AND '2023-12-31';
```
- Получить информацию о пользователях, которые бронировали места только в бизнес-классе.
```sql
SELECT DISTINCT User.* FROM User
JOIN Passenger ON User.ID = Passenger.UserID
JOIN Reservation ON Passenger.ID = Reservation.PassengerID
JOIN Seat ON Reservation.SeatID = Seat.ID
WHERE Seat.SeatType = 'Business';
```
- Получить все рейсы определенного пользователя за определенный день из определенного аэропорта.
```sql
SELECT Flight.* FROM Flight
JOIN Airplane ON Flight.AirplaneID = Airplane.ID
JOIN Seat ON Airplane.ID = Seat.AirplaneID
JOIN Reservation ON Seat.ID = Reservation.SeatID
JOIN Passenger ON Reservation.PassengerID = Passenger.ID
JOIN User ON Passenger.UserID = User.ID
WHERE User.Username = 'username'
AND Flight.TimeDeparture::date = '2023-06-30'
AND Flight.AirportDepartureID = (SELECT ID FROM Airport WHERE Name = 'AER');
```
- Найти все рейсы, выполняемые самолетами с количеством мест более 150, вылетающие из определенного аэропорта.
```sql
SELECT Flight.* FROM Flight
JOIN Airplane ON Flight.AirplaneID = Airplane.ID
WHERE Airplane.NumberOfSeats > 150
AND Flight.AirportDepartureID = (SELECT ID FROM Airport WHERE Name = 'LED');
```
- Получить все бронирования пассажиров, у которых есть страховка и которые вылетают из определенного города.
```sql
SELECT Reservation.* FROM Reservation
JOIN Passenger ON Reservation.PassengerID = Passenger.ID
JOIN Seat ON Reservation.SeatID = Seat.ID
JOIN Airplane ON Seat.AirplaneID = Airplane.ID
JOIN Flight ON Airplane.ID = Flight.AirplaneID
JOIN Airport ON Flight.AirportDepartureID = Airport.ID
WHERE Reservation.Insurance = 'Yes'
AND Airport.City = 'Sochi';
```

# Описание таблиц и их полей:
## Таблица 1: Airport
Эта таблица хранит информацию об аэропортах. Она необходима для указания точек отправления и прибытия рейсов.

| Поле                  | Тип данных       | Описание                                |
|-----------------------|------------------|-----------------------------------------|
| ID (первичный ключ)   | Integer(10)      | Уникальный идентификатор аэропорта      |
| Name                  | varchar(255)     | Название аэропорта                      |
| City                  | varchar(255)     | Город, где находится аэропорт           |
| Country               | varchar(255)     | Страна, где находится аэропорт          |
| Coordinates           | varchar(255)     | Координаты аэропорта                    |

## Таблица 2: Airplane
Эта таблица содержит информацию о самолетах, которые используются для выполнения рейсов.

| Поле                  | Тип данных       | Описание                                |
|-----------------------|------------------|-----------------------------------------|
| ID (первичный ключ)   | Integer(10)      | Уникальный идентификатор самолета       |
| Type                  | varchar(255)     | Тип самолета                            |
| Bort number           | varchar(255)     | Бортовой номер                          |
| Personal on board     | Integer(10)      | Количество персонала на борту           |
| Number of seats       | Integer(10)      | Количество мест                         |

## Таблица 3: Flight
Эта таблица содержит информацию о рейсах, включая время отправления и прибытия, а также самолеты и аэропорты, участвующие в рейсе.

| Поле                                | Тип данных       | Описание                                |
|-------------------------------------|------------------|-----------------------------------------|
| ID (первичный ключ)                 | Integer(10)      | Уникальный идентификатор рейса          |
| Airport departureID (внешний ключ)  | Integer(10)      | Идентификатор аэропорта отправления     |
| Airport arrivalID (внешний ключ)    | Integer(10)      | Идентификатор аэропорта прибытия        |
| AirplaneID (внешний ключ)           | Integer(10)      | Идентификатор самолета                  |
| Time departure                      | time(7)          | Время отправления                       |
| Time arrival                        | time(7)          | Время прибытия                          |
| Time on board                       | time(7)          | Время в пути                            |
| Range of flight                     | Integer(10)      | Дальность полета                        |

## Таблица 4: Passenger
Эта таблица содержит информацию о пассажирах, включая их личные данные и удостоверяющие документы.

| Поле                    | Тип данных       | Описание                                |
|-------------------------|------------------|-----------------------------------------|
| ID (первичный ключ)     | Integer(10)      | Уникальный идентификатор пассажира      |
| UserID (внешний ключ)   | Integer(10)      | Идентификатор пользователя              |
| Name                    | varchar(255)     | Имя                                     |
| Surname                 | varchar(255)     | Фамилия                                 |
| Patronymic              | varchar(255)     | Отчество                                |
| Age                     | Integer(10)      | Возраст                                 |
| Date of birthdate       | time(7)          | Дата рождения                           |
| Gender                  | char(1)          | Пол                                     |
| Serial number document  | Integer(10)      | Серия и номер удостоверяющего документа |
| Type of document        | varchar(30)      | Тип удостоверяющего документа           |

## Таблица 5: Seat
Эта таблица содержит информацию о местах в самолете, включая тип и номер места.

| Поле                    | Тип данных       | Описание                                |
|-------------------------|------------------|-----------------------------------------|
| ID (первичный ключ)     | Integer(10)      | Уникальный идентификатор места          |
| AirplaneID (внешний ключ) | Integer(10)    | Идентификатор самолета                  |
| Seat type               | varchar(30)      | Тип места                               |
| Seat number             | Integer(10)      | Номер места                             |

## Таблица 6: Reservation
Эта таблица содержит информацию о бронированиях, включая детали места, пассажира и оплаты.

| Поле                    | Тип данных       | Описание                                |
|-------------------------|------------------|-----------------------------------------|
| ID (первичный ключ)     | Integer(10)      | Уникальный идентификатор бронирования   |
| SeatID (внешний ключ)   | Integer(10)      | Идентификатор места                     |
| PassengerID (внешний ключ) | Integer(10)   | Идентификатор пассажира                 |
| Insurance               | varchar(10)      | Наличие страховки                       |
| Type of bill            | varchar(255)     | Тип билета                              |
| Payment currency        | varchar(255)     | Валюта оплаты                           |


## Таблица 7: User
Эта таблица содержит информацию о пользователях системы, включая их учетные данные и роль.

| Поле                    | Тип данных       | Описание                                |
|-------------------------|------------------|-----------------------------------------|
| ID (первичный ключ)     | Integer(10)      | Уникальный идентификатор пользователя   |
| Username                | varchar(255)     | Имя пользователя                        |
| Password                | varchar(255)     | Пароль                                  |
| E-Mail                  | varchar(255)     | Электронная почта                       |
| Role                    | varchar(30)      | Роль                                    |
| Date of register        | time(7)          | Дата регистрации                        |



# Скрипт для генерации sql запросов заполнения таблиц:
Данный скрипт вы можете найти в файле createImport.py. Данный скрипт создает файл insert.sql, который содержит в себе строки для вставки значений в таблицы. Число записей регулируетcя благодаря параметру n_records. Имя генерируемого файла можно менять изменяя параметр filename

- generate_airports(n): генерирует список SQL-запросов для вставки данных в таблицу Airport.
```python
def generate_airports(n):
    airports = []
    for i in range(1, n + 1):
        airports.append(f"({i}, '{random_string(3)}', 'City{i}', 'Country{i}', '{random.uniform(-90, 90):.6f}, {random.uniform(-180, 180):.6f}')")
    return airports
```

- generate_airplanes(n): генерирует список SQL-запросов для вставки данных в таблицу Airplane.
```python
def generate_airplanes(n):
    airplanes = []
    for i in range(1, n + 1):
        airplanes.append(f"({i}, 'Type{i}', '{random_string(5)}', {random.randint(1, 50)}, {random.randint(50, 300)})")
    return airplanes
```

- generate_seats(n): генерирует список SQL-запросов для вставки данных в таблицу Seat.
```python
def generate_seats(n):
    seats = []
    for i in range(1, n + 1):
        seats.append(f"({i}, {random.randint(1, n)}, 'Economy', {i})")
    return seats
```
- generate_passengers(n): генерирует список SQL-запросов для вставки данных в таблицу Passenger.
```python
def generate_passengers(n):
    passengers = []
    for i in range(1, n + 1):
        gender = random.choice(['M', 'F'])
        date_of_birth = random_date(datetime(1950, 1, 1), datetime(2003, 12, 31)).strftime('%Y-%m-%d')
        passengers.append(f"({i}, {random.randint(1, n)}, 'Name{i}', 'Surname{i}', 'Patronymic{i}', {random.randint(18, 70)}, '{date_of_birth}', '{gender}', {random.randint(100000, 999999)}, 'Passport')")
    return passengers
```
- generate_reservations(n): генерирует список SQL-запросов для вставки данных в таблицу Reservation.
```python
def generate_reservations(n):
    reservations = []
    for i in range(1, n + 1):
        reservations.append(f"({i}, {random.randint(1, n)}, {random.randint(1, n)}, 'Yes', 'Electronic', 'RUB')")
    return reservations
```
- generate_flights(n): генерирует список SQL-запросов для вставки данных в таблицу Flight.
```python
def generate_flights(n):
    flights = []
    for i in range(1, n + 1):
        time_departure = random_time()
        time_arrival = (datetime.combine(datetime.today(), time_departure) + timedelta(hours=random.randint(1, 5))).time()
        flights.append(f"({i}, {random.randint(1, n)}, {random.randint(1, n)}, {random.randint(1, n)}, '{time_departure}', '{time_arrival}', {random.randint(60, 300)}, {random.randint(500, 1500)})")
    return flights
```
- generate_users(n): генерирует список SQL-запросов для вставки данных в таблицу User.
```python
def generate_users(n):
    users = []
    for i in range(1, n + 1):
        users.append(f"({i}, 'Username{i}', 'Password{i}', 'user{i}@example.com', 'User', '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}')")
    return users
```

- Функция для записи SQL-запросов в файл
Описание функции:
write_to_file(filename, data): записывает все SQL-запросы в один файл.
```python
def write_to_file(filename, data):
    with open(filename, 'w') as file:
        for table, values in data.items():
            file.write(f"INSERT INTO {table} VALUES\n")
            file.write(",\n".join(values) + ";\n\n")
```

Главная часть программы

Описание:
Устанавливает количество записей для генерации (число указано в переменной n_records).
Генерирует данные для всех таблиц.
Записывает все SQL-запросы в файл с именем записанным в переменной filename.
```python
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
```
