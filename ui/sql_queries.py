"""
Module containing SQL queries for train station database according to lab work requirements.
This includes SELECT queries, JOIN queries, and queries with subqueries, aggregate functions, etc.
"""

class TrainQueries:
    """SQL queries for Train table"""
    
    # SELECT FROM
    SELECT_ALL_SPEED_AND_TYPE = "SELECT speed, type FROM train"
    
    # SELECT FROM WHERE
    SELECT_SPEED_MORE_THAN_100 = "SELECT * FROM train WHERE speed > 100"
    
    # SELECT FROM ORDER BY
    SELECT_ORDER_BY_SPEED = "SELECT type FROM train ORDER BY speed"
    
    # Combined query - trains with type containing 'Пассажирский' or speed > 140, ordered by year
    SELECT_COMBINED_TRAIN = """
    SELECT * FROM train 
    WHERE type LIKE '%Пассажирский%' OR speed > 140 
    ORDER BY year_manufactured DESC
    """


class TicketQueries:
    """SQL queries for Ticket table"""
    
    # SELECT FROM
    SELECT_CAR_NUMBER_AND_PRICE = "SELECT carriage_number, price FROM ticket"
    
    # SELECT FROM WHERE
    SELECT_PRICE_LESS_THAN_6 = "SELECT * FROM ticket WHERE price < 6"
    
    # SELECT FROM ORDER BY
    SELECT_ORDER_BY_PRICE_DESC = "SELECT * FROM ticket ORDER BY price DESC"
    
    # Combined query - tickets with price > 3 and <= 7
    SELECT_COMBINED_TICKET = "SELECT * FROM ticket WHERE price > 3 AND price <= 7"


class ServiceQueries:
    """SQL queries for Service table"""
    
    # SELECT FROM
    SELECT_SERVICE_NAME_AND_TOTAL_PRICE = "SELECT service_name, price FROM service"
    
    # SELECT FROM WHERE
    SELECT_PRICE_MORE_THAN_1000_AND_DATE_BEFORE = "SELECT * FROM service WHERE price > 1000 AND service_date < '2025-01-20'"
    
    # SELECT FROM ORDER BY
    SELECT_ORDER_BY_SERVICE_DATE = "SELECT * FROM service ORDER BY service_date ASC"
    
    # Combined query - services with price > 1000 and type 'Техническая'
    SELECT_COMBINED_SERVICE = "SELECT * FROM service WHERE price > 1000 AND type = 'Техническая'"


class ScheduleQueries:
    """SQL queries for Schedule table"""
    
    # SELECT FROM
    SELECT_CARRIAGE_AND_DEPARTURE = "SELECT carriage_enumeration, departure_time FROM schedule"
    
    # SELECT FROM WHERE
    SELECT_DEPARTURE_AFTER_12 = "SELECT * FROM schedule WHERE departure_time > '12:00:00'"
    
    # SELECT FROM ORDER BY
    SELECT_ORDER_BY_DEPARTURE_DESC = "SELECT * FROM schedule ORDER BY departure_time DESC"
    
    # Combined query - schedules where difference between arrival and departure time is more than 20 minutes
    SELECT_COMBINED_SCHEDULE = """
    SELECT * FROM schedule 
    WHERE time((julianday(arrival_time) - julianday(departure_time)) * 24 * 60) > 20
    """
    

class PlatformQueries:
    """SQL queries for Platform table"""
    
    # SELECT FROM - first 5 records
    SELECT_FIRST_5_PLATFORMS = "SELECT * FROM platform LIMIT 5"
    
    # SELECT FROM WHERE - capacity between 300 and 500
    SELECT_CAPACITY_300_TO_500 = "SELECT * FROM platform WHERE capacity BETWEEN 300 AND 500"
    
    # SELECT FROM ORDER BY - ordered by location, then capacity
    SELECT_ORDER_BY_LOCATION_AND_CAPACITY = "SELECT * FROM platform ORDER BY location, capacity"
    
    # Combined query - capacity > 400 or track_count > 3, ordered by capacity and track_count descending
    SELECT_COMBINED_PLATFORM = """
    SELECT * FROM platform 
    WHERE capacity > 400 OR track_count > 3 
    ORDER BY capacity DESC, track_count DESC
    """


class PassengerQueries:
    """SQL queries for Passenger table"""
    
    # SELECT FROM - first 10 passengers with passport, name, and phone
    SELECT_FIRST_10_PASSPORT_NAME_PHONE = "SELECT passport_number, full_name, mobile_phone FROM passenger LIMIT 10"
    
    # SELECT FROM WHERE - ID between certain values
    SELECT_ID_BETWEEN_5_AND_10 = "SELECT * FROM passenger WHERE passenger_id > 5 AND passenger_id < 10"
    
    # SELECT FROM ORDER BY - ordered by full_name in reverse order
    SELECT_ORDER_BY_NAME_REVERSE = "SELECT * FROM passenger ORDER BY full_name DESC"
    
    # Combined query - sorted by name, first letter 'A' or phone starts with '+37544'
    SELECT_COMBINED_PASSENGER = """
    SELECT * FROM passenger 
    WHERE full_name LIKE 'A%' OR mobile_phone LIKE '+37544%'
    ORDER BY full_name
    """


class EmployeeQueries:
    """SQL queries for Employee table"""
    
    # SELECT FROM - first 5 employees with experience > 10
    SELECT_FIRST_5_WITH_EXPERIENCE_10 = "SELECT * FROM employee WHERE experience > 10 LIMIT 5"
    
    # SELECT FROM WHERE - only engineers
    SELECT_ONLY_ENGINEERS = "SELECT * FROM employee WHERE position = 'инженер'"
    
    # SELECT FROM ORDER BY - ordered by passport number in reverse
    SELECT_ORDER_BY_PASSPORT_REVERSE = "SELECT * FROM employee ORDER BY passport_data DESC"
    
    # Combined query - employees with all positions except 'Проводник', ordered by full_name
    SELECT_COMBINED_EMPLOYEE = "SELECT * FROM employee WHERE position != 'Проводник' ORDER BY full_name"


class TrainTicketJoinQueries:
    """SQL queries for JOIN operations between Train and Ticket"""
    
    # INNER JOIN - tickets with carriage number equal to train carriage count
    INNER_JOIN_TRAIN_TICKET = """
    SELECT t.*, tr.* 
    FROM ticket t 
    INNER JOIN train tr ON t.carriage_number = tr.carriage_count
    """
    
    # LEFT OUTER JOIN - all trains with tickets for the last carriage
    LEFT_JOIN_TRAIN_TICKET = """
    SELECT tr.*, t.* 
    FROM train tr 
    LEFT JOIN ticket t ON tr.carriage_count = t.carriage_number
    """
    
    # RIGHT OUTER JOIN - tickets > 5 with last carriages of trains
    RIGHT_JOIN_TRAIN_TICKET = """
    SELECT t.*, tr.* 
    FROM ticket t 
    RIGHT JOIN train tr ON t.carriage_number = tr.carriage_count 
    WHERE t.price > 5
    """
    
    # FULL OUTER JOIN - using PostgreSQL native support
    FULL_JOIN_TRAIN_TICKET = """
    SELECT t.*, tr.* 
    FROM ticket t 
    LEFT JOIN train tr ON t.carriage_number = tr.carriage_count AND tr.type != 'Грузовой' 
    WHERE t.price > 5 AND t.carriage_number > 12
    
    UNION
    
    SELECT t.*, tr.* 
    FROM ticket t 
    RIGHT JOIN train tr ON t.carriage_number = tr.carriage_count AND tr.type != 'Грузовой' 
    WHERE t.price > 5 AND t.carriage_number > 12
    """
    
    # CROSS JOIN - tickets > 5 for non-freight trains for one carriage
    CROSS_JOIN_TRAIN_TICKET = """
    SELECT t.*, tr.* 
    FROM ticket t 
    CROSS JOIN train tr 
    WHERE t.price > 5 AND tr.type != 'Грузовой' AND t.carriage_number = 1
    """


class ServiceEmployeeJoinQueries:
    """SQL queries for JOIN operations between Service and Employee"""
    
    # INNER JOIN - services with employees providing them
    INNER_JOIN_SERVICE_EMPLOYEE = """
    SELECT s.*, e.* 
    FROM service s 
    INNER JOIN service_assignment sa ON s.service_id = sa.service_id 
    INNER JOIN employee e ON sa.employee_id = e.employee_id
    """
    
    # LEFT OUTER JOIN - employees with positions and services they provide
    LEFT_JOIN_SERVICE_EMPLOYEE = """
    SELECT e.full_name, e.position, s.service_name 
    FROM employee e 
    LEFT JOIN service_assignment sa ON e.employee_id = sa.employee_id 
    LEFT JOIN service s ON sa.service_id = s.service_id
    """
    
    # RIGHT OUTER JOIN - all services and employees providing them
    RIGHT_JOIN_SERVICE_EMPLOYEE = """
    SELECT s.*, e.* 
    FROM service s 
    RIGHT JOIN service_assignment sa ON s.service_id = sa.service_id 
    RIGHT JOIN employee e ON sa.employee_id = e.employee_id
    """
    
    # FULL OUTER JOIN - using PostgreSQL native support
    FULL_JOIN_SERVICE_EMPLOYEE = """
    SELECT s.*, e.* 
    FROM service s 
    LEFT JOIN service_assignment sa ON s.service_id = sa.service_id 
    LEFT JOIN employee e ON sa.employee_id = e.employee_id
    
    UNION
    
    SELECT s.*, e.* 
    FROM service s 
    RIGHT JOIN service_assignment sa ON s.service_id = sa.service_id 
    RIGHT JOIN employee e ON sa.employee_id = e.employee_id
    """
    
    # CROSS JOIN - all services and employees
    CROSS_JOIN_SERVICE_EMPLOYEE = """
    SELECT s.*, e.* 
    FROM service s 
    CROSS JOIN employee e
    """


class PlatformScheduleJoinQueries:
    """SQL queries for JOIN operations between Platform and Schedule"""
    
    # INNER JOIN - platform location with arrival/departure times and track count > 2
    INNER_JOIN_PLATFORM_SCHEDULE = """
    SELECT p.location, s.arrival_time, s.departure_time, p.track_count 
    FROM platform p 
    INNER JOIN schedule s ON p.platform_id = s.platform_id 
    WHERE p.track_count > 2
    """
    
    # LEFT OUTER JOIN - platforms with capacity > 400 and their schedules
    LEFT_JOIN_PLATFORM_SCHEDULE = """
    SELECT p.*, s.* 
    FROM platform p 
    LEFT JOIN schedule s ON p.platform_id = s.platform_id 
    WHERE p.capacity > 400
    """
    
    # RIGHT OUTER JOIN - arrival/departure times for train 2 with platform location
    RIGHT_JOIN_PLATFORM_SCHEDULE = """
    SELECT s.*, p.location 
    FROM schedule s 
    RIGHT JOIN platform p ON s.platform_id = p.platform_id 
    WHERE s.train_id = 2
    """
    
    # FULL OUTER JOIN - all data for platform 4
    FULL_JOIN_PLATFORM_SCHEDULE = """
    SELECT p.*, s.* 
    FROM platform p 
    LEFT JOIN schedule s ON p.platform_id = s.platform_id 
    WHERE p.platform_id = 4
    
    UNION
    
    SELECT p.*, s.* 
    FROM platform p 
    RIGHT JOIN schedule s ON p.platform_id = s.platform_id 
    WHERE p.platform_id = 4
    """
    
    # CROSS JOIN - first 5 records: "Platform 1 Minsk-Passenger" with all schedules
    CROSS_JOIN_PLATFORM_SCHEDULE = """
    SELECT p.location, s.* 
    FROM platform p 
    CROSS JOIN schedule s 
    WHERE p.location LIKE '%1%Минск%' AND p.location LIKE '%Пассажирский%' 
    LIMIT 5
    """


class EmployeeTrainJoinQueries:
    """SQL queries for JOIN operations between Employee and Train via assignment table"""
    
    # INNER JOIN - services provided by engine drivers and their names
    INNER_JOIN_EMPLOYEE_SERVICE = """
    SELECT s.service_name, e.full_name, e.position 
    FROM service s 
    INNER JOIN service_assignment sa ON s.service_id = sa.service_id 
    INNER JOIN employee e ON sa.employee_id = e.employee_id
    """
    
    # LEFT OUTER JOIN - all drivers and services they provide
    LEFT_JOIN_EMPLOYEE_SERVICE = """
    SELECT e.*, s.service_name 
    FROM employee e 
    LEFT JOIN service_assignment sa ON e.employee_id = sa.employee_id 
    LEFT JOIN service s ON sa.service_id = s.service_id 
    WHERE e.position LIKE '%машинист%'
    """
    
    # RIGHT OUTER JOIN - all technical services and employees providing them
    RIGHT_JOIN_EMPLOYEE_SERVICE = """
    SELECT s.*, e.* 
    FROM service s 
    RIGHT JOIN service_assignment sa ON s.service_id = sa.service_id 
    RIGHT JOIN employee e ON sa.employee_id = e.employee_id 
    WHERE s.type = 'Техническая'
    """
    
    # FULL OUTER JOIN - engineers providing technical services
    FULL_JOIN_EMPLOYEE_SERVICE = """
    SELECT e.*, s.* 
    FROM employee e 
    LEFT JOIN service_assignment sa ON e.employee_id = sa.employee_id 
    LEFT JOIN service s ON sa.service_id = s.service_id 
    WHERE e.position = 'инженер' AND s.type = 'Техническая'
    
    UNION
    
    SELECT e.*, s.* 
    FROM employee e 
    RIGHT JOIN service_assignment sa ON e.employee_id = sa.employee_id 
    RIGHT JOIN service s ON sa.service_id = s.service_id 
    WHERE e.position = 'инженер' AND s.type = 'Техническая'
    """
    
    # CROSS JOIN - specific service with specific employee first 5
    CROSS_JOIN_EMPLOYEE_SERVICE = """
    SELECT s.*, e.* 
    FROM service s 
    CROSS JOIN employee e 
    WHERE e.employee_id = 1 
    LIMIT 5
    """


class ScheduleTrainJoinQueries:
    """SQL queries for JOIN operations between Schedule and Train"""
    
    # INNER JOIN - trains with speed > 100 with their arrival/departure times
    INNER_JOIN_SCHEDULE_TRAIN = """
    SELECT tr.*, s.arrival_time, s.departure_time 
    FROM train tr 
    INNER JOIN schedule s ON tr.train_id = s.train_id 
    WHERE tr.speed > 100
    """
    
    # LEFT OUTER JOIN - arrival/departure times for trains with speed > 100
    LEFT_JOIN_SCHEDULE_TRAIN = """
    SELECT s.arrival_time, s.departure_time, tr.* 
    FROM train tr 
    LEFT JOIN schedule s ON tr.train_id = s.train_id 
    WHERE tr.speed > 100
    """
    
    # RIGHT OUTER JOIN - arrival/departure times for trains with speed > 100 even without schedule
    RIGHT_JOIN_SCHEDULE_TRAIN = """
    SELECT s.arrival_time, s.departure_time, tr.* 
    FROM train tr 
    RIGHT JOIN schedule s ON tr.train_id = s.train_id 
    WHERE tr.speed > 100
    """
    
    # FULL OUTER JOIN - express trains with departure time < 12:00:00
    FULL_JOIN_SCHEDULE_TRAIN = """
    SELECT tr.*, s.* 
    FROM train tr 
    LEFT JOIN schedule s ON tr.train_id = s.train_id 
    WHERE tr.type = 'Скорый' AND s.departure_time < '12:00:00'
    
    UNION
    
    SELECT tr.*, s.* 
    FROM train tr 
    RIGHT JOIN schedule s ON tr.train_id = s.train_id 
    WHERE tr.type = 'Скорый' AND s.departure_time < '12:00:00'
    """
    
    # CROSS JOIN - express trains with all schedules first 5
    CROSS_JOIN_SCHEDULE_TRAIN = """
    SELECT tr.*, s.* 
    FROM train tr 
    CROSS JOIN schedule s 
    WHERE tr.type = 'Скорый' 
    LIMIT 5
    """


class TicketPassengerJoinQueries:
    """SQL queries for JOIN operations between Ticket and Passenger"""
    
    # INNER JOIN - ticket seats and passenger names with ticket price > 7
    INNER_JOIN_TICKET_PASSENGER = """
    SELECT t.seat_number, p.full_name 
    FROM ticket t 
    INNER JOIN passenger p ON t.passenger_id = p.passenger_id 
    WHERE t.price > 7
    """
    
    # LEFT OUTER JOIN - ticket prices > 7 and corresponding passengers
    LEFT_JOIN_TICKET_PASSENGER = """
    SELECT t.price, t.seat_number, p.full_name 
    FROM ticket t 
    LEFT JOIN passenger p ON t.passenger_id = p.passenger_id 
    WHERE t.price > 7
    """
    
    # RIGHT OUTER JOIN - seats and names of passengers with ticket price > 7
    RIGHT_JOIN_TICKET_PASSENGER = """
    SELECT t.seat_number, p.full_name, t.price 
    FROM ticket t 
    RIGHT JOIN passenger p ON t.passenger_id = p.passenger_id 
    WHERE t.price > 7
    """
    
    # FULL OUTER JOIN - tickets and passengers with discounted tickets and price > 7
    FULL_JOIN_TICKET_PASSENGER = """
    SELECT t.*, p.* 
    FROM ticket t 
    LEFT JOIN passenger p ON t.passenger_id = p.passenger_id 
    WHERE (p.remark LIKE '%льготный%' OR t.price > 7)
    
    UNION
    
    SELECT t.*, p.* 
    FROM ticket t 
    RIGHT JOIN passenger p ON t.passenger_id = p.passenger_id 
    WHERE (p.remark LIKE '%льготный%' OR t.price > 7)
    """
    
    # CROSS JOIN - all tickets and passengers with price > 7
    CROSS_JOIN_TICKET_PASSENGER = """
    SELECT t.*, p.* 
    FROM ticket t 
    CROSS JOIN passenger p 
    WHERE t.price > 7
    """


class TicketScheduleJoinQueries:
    """SQL queries for JOIN operations between Ticket and Schedule"""
    
    # INNER JOIN - ticket data and departure time for tickets > 7
    INNER_JOIN_TICKET_SCHEDULE = """
    SELECT t.*, s.departure_time 
    FROM ticket t 
    INNER JOIN schedule s ON t.ticket_id = s.ticket_id 
    WHERE t.price > 7
    """
    
    # LEFT OUTER JOIN - all schedule data and ticket data > 7
    LEFT_JOIN_TICKET_SCHEDULE = """
    SELECT s.*, t.* 
    FROM schedule s 
    LEFT JOIN ticket t ON s.ticket_id = t.ticket_id 
    WHERE t.price > 7
    """
    
    # RIGHT OUTER JOIN - all tickets with seats and arrival/departure times before 12:00:00
    RIGHT_JOIN_TICKET_SCHEDULE = """
    SELECT t.*, s.arrival_time, s.departure_time 
    FROM ticket t 
    RIGHT JOIN schedule s ON t.ticket_id = s.ticket_id 
    WHERE s.departure_time < '12:00:00'
    """
    
    # FULL OUTER JOIN - tickets < 7 and arrival/departure times after 12:00:00
    FULL_JOIN_TICKET_SCHEDULE = """
    SELECT t.*, s.* 
    FROM ticket t 
    LEFT JOIN schedule s ON t.ticket_id = s.ticket_id 
    WHERE t.price < 7 AND s.arrival_time > '12:00:00'
    
    UNION
    
    SELECT t.*, s.* 
    FROM ticket t 
    RIGHT JOIN schedule s ON t.ticket_id = s.ticket_id 
    WHERE t.price < 7 AND s.arrival_time > '12:00:00'
    """
    
    # CROSS JOIN - tickets > 7 and departure/arrival times before 12:00:00 first 5
    CROSS_JOIN_TICKET_SCHEDULE = """
    SELECT t.*, s.* 
    FROM ticket t 
    CROSS JOIN schedule s 
    WHERE t.price > 7 AND s.departure_time < '12:00:00' 
    LIMIT 5
    """


class AggregateQueries:
    """SQL queries with aggregate functions, subqueries, grouping and set operations"""
    
    # Train table - AVG speed, COUNT years
    AGGREGATE_TRAIN = """
    SELECT AVG(speed) AS avg_speed, COUNT(year_manufactured) AS count_years 
    FROM train
    """
    
    # Ticket table - SUM price, MIN seat number, MAX carriage number
    AGGREGATE_TICKET = """
    SELECT SUM(price) AS total_price, MIN(seat_number) AS min_seat, MAX(carriage_number) AS max_carriage 
    FROM ticket
    """
    
    # Service table - scalar and aggregate functions with GROUP BY
    AGGREGATE_SERVICE = """
    SELECT service_name, CAST(AVG(price) AS INTEGER) AS avg_price, EXTRACT(DAY FROM service_date) AS day 
    FROM service 
    GROUP BY service_name, EXTRACT(DAY FROM service_date) 
    HAVING AVG(price) > 1000
    """
    
    # Schedule table - subqueries in WHERE clause
    SUBQUERY_SCHEDULE = """
    SELECT carriage_enumeration, arrival_time, date, departure_time 
    FROM schedule 
    WHERE carriage_enumeration IN ('с головы поезда', 'с хвоста поезда', 'середины состава')
      AND arrival_time > ANY (SELECT arrival_time FROM schedule WHERE departure_time LIKE '10:%')
      AND EXISTS (SELECT 1 FROM schedule s2 WHERE departure_time > ALL (SELECT departure_time FROM schedule WHERE date LIKE '%-15'))
    ORDER BY arrival_time
    """
    
    # Platform and Train - UNION operation
    UNION_PLATFORM_TRAIN = """
    SELECT capacity AS value, track_count AS attribute 
    FROM platform 
    WHERE capacity > 0
    UNION
    SELECT carriage_count AS value, speed AS attribute 
    FROM train 
    WHERE type NOT LIKE '%Грузовой%' AND speed > ALL (SELECT speed FROM train WHERE year_manufactured < 2010)
    ORDER BY value
    LIMIT 10
    """
    
    # Passenger and Ticket - INTERSECT operation using PostgreSQL native support
    INTERSECT_PASSENGER_TICKET = """
    SELECT DISTINCT p.full_name AS name
    FROM passenger p
    WHERE p.remark NOT LIKE '%льготный%'
       OR p.remark LIKE '%Постоянный клиент%'
    AND p.full_name IN (
        SELECT p2.full_name 
        FROM passenger p2 
        JOIN ticket t ON p2.passenger_id = t.passenger_id 
        WHERE t.price > ALL (SELECT price FROM ticket WHERE price < 6.00)
    )
    ORDER BY name DESC
    """
    
    # Employee and Service - EXCEPT operation using PostgreSQL native support
    EXCEPT_EMPLOYEE_SERVICE = """
    SELECT DISTINCT e.position
    FROM employee e
    WHERE e.position NOT IN (
        SELECT s.service_name 
        FROM service s
    )
    """