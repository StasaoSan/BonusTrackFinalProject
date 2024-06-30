CREATE TABLE if not exists Airport(
    ID          integer primary key,
    Name        varchar(255),
    City        varchar(255),
    Country     varchar(255),
    Coordinates varchar(255) not null
);

CREATE TABLE if not exists Airplane(
    ID               integer primary key,
    TypeAirplane     varchar(255),
    BortNumber       integer,
    PersonalsOnBoard integer,
    NumberOfSeats    integer
);

CREATE TABLE if not exists UserSite(
    ID             integer primary key,
    Username       varchar(255),
    Password       varchar(255),
    E_Mail         varchar(255),
    Role           varchar(255),
    DateOfRegister DATE
);

CREATE TABLE if not exists Seat(
    ID         integer primary key,
    AirplaneID integer,
    SeatType   varchar(30),
    SeatNumber integer,
    FOREIGN KEY (AirplaneID) REFERENCES Airplane (ID)
);

CREATE TABLE if not exists Passanger(
    ID                   integer primary key,
    UserSiteID               integer,
    Name                 varchar(255),
    Surname              varchar(255),
    Pathronymic          varchar(255),
    Age                  integer,
    DateOfBithdate       DATE,
    Gender               char(1),
    SerialNumberDocument integer,
    TypeOfDocument       varchar(30),
    FOREIGN KEY (UserSiteID) REFERENCES UserSite (ID)
);

CREATE TABLE if not exists Flight(
    ID                 integer primary key,
    AirportDepartureID integer,
    AirportArrivalID   integer,
    AirplaneID         integer,
    TimeDeparture      time(7),
    TimeArrival        time(7),
    TimeOnBoard        integer,
    RangeOfFlight      integer,
    FOREIGN KEY (AirportDepartureID) REFERENCES Airport (ID),
    FOREIGN KEY (AirportArrivalID) REFERENCES Airport (ID),
    FOREIGN KEY (AirplaneID) REFERENCES Airplane (ID)
);

CREATE TABLE if not exists Reservation(
ID              integer primary key,
Insuranse       varchar(10),
SeatID          integer,
PassangerID     integer,
TypeOfBill      varchar(255),
PaymentCurrency varchar(255),
FOREIGN KEY (SeatID) REFERENCES Seat (ID),
FOREIGN KEY (PassangerID) REFERENCES Passanger (ID)
);
