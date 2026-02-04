"""
Module containing SQL queries for laboratory work 5 and 6 according to the requirements.
This includes all the special queries mentioned in the lab work.
"""

class LabQueries:
    """SQL queries for laboratory work 5 and 6"""

    # Lab Work 5 - SELECT queries
    
    # 1. Select trains with speed more than 100
    LAB5_QUERY1 = "SELECT * FROM train WHERE speed > 100"
    
    # 2. List of train types sorted by train speed
    LAB5_QUERY2 = "SELECT type FROM train ORDER BY speed"
    
    # 3. Trains with type containing 'Пассажирский' or speed more than 140, sorted by year of manufacture from new to old
    LAB5_QUERY3 = """
    SELECT * FROM train
    WHERE type LIKE '%Пассажирский%' OR speed > 140
    ORDER BY year_manufactured DESC
    """
    
    # 4. Output carriage number and price of all tickets
    LAB5_QUERY4 = "SELECT carriage_number, price FROM ticket"
    
    # 5. Select all tickets with price less than 6
    LAB5_QUERY5 = "SELECT * FROM ticket WHERE price < 6"
    
    # 6. Tickets sorted by descending price
    LAB5_QUERY6 = "SELECT * FROM ticket ORDER BY price DESC"
    
    # 7. Tickets with price greater than 3 and less than or equal to 7
    LAB5_QUERY7 = "SELECT * FROM ticket WHERE price > 3 AND price <= 7"
    
    # 8. Output service name and total price
    LAB5_QUERY8 = "SELECT service_name, price FROM service"
    
    # 9. Materials with price more than 1000 and date before 2025-01-20
    LAB5_QUERY9 = "SELECT * FROM service WHERE price > 1000 AND service_date < '2025-01-20'"
    
    # 10. Services sorted in ascending order by service date
    LAB5_QUERY10 = "SELECT * FROM service ORDER BY service_date ASC"
    
    # 11. Services with price more than 1000 and with service type 'Техническая'
    LAB5_QUERY11 = "SELECT * FROM service WHERE price > 1000 AND type = 'Техническая'"
    
    # 12. Output carriage enumeration and departure time
    LAB5_QUERY12 = "SELECT carriage_enumeration, departure_time FROM schedule"
    
    # 13. Carriage enumerations where departure is after 12:00:00
    LAB5_QUERY13 = "SELECT * FROM schedule WHERE departure_time > '12:00:00'"
    
    # 14. List of carriage enumerations sorted by departure time from greater to lesser
    LAB5_QUERY14 = "SELECT * FROM schedule ORDER BY departure_time DESC"
    
    # 15. Output carriage enumerations where the difference between arrival and departure time is more than 20 minutes
    LAB5_QUERY15 = """
    SELECT * FROM schedule
    WHERE CAST(strftime('%H', arrival_time) AS INTEGER) * 60 + CAST(strftime('%M', arrival_time) AS INTEGER) -
          (CAST(strftime('%H', departure_time) AS INTEGER) * 60 + CAST(strftime('%M', departure_time) AS INTEGER)) > 20
    """
    
    # 16. Output first 5 records about platforms
    LAB5_QUERY16 = "SELECT * FROM platform LIMIT 5"
    
    # 17. Platforms with capacity from 300 to 500
    LAB5_QUERY17 = "SELECT * FROM platform WHERE capacity BETWEEN 300 AND 500"
    
    # 18. List of checks (probably meant tickets) sorted by location, then by capacity
    LAB5_QUERY18 = "SELECT * FROM platform ORDER BY location, capacity"
    
    # 19. Output platforms with capacity more than 400 or with track count more than 3, sorted first by decreasing capacity, then by decreasing track count
    LAB5_QUERY19 = """
    SELECT * FROM platform
    WHERE capacity > 400 OR track_count > 3
    ORDER BY capacity DESC, track_count DESC
    """
    
    # 20. Output passport number, full name and mobile phone of first 10 passengers
    LAB5_QUERY20 = "SELECT passport_number, full_name, mobile_phone FROM passenger LIMIT 10"
    
    # 21. Passengers with ID greater than 5 and less than 10
    LAB5_QUERY21 = "SELECT * FROM passenger WHERE passenger_id > 5 AND passenger_id < 10"
    
    # 22. Passengers sorted in reverse order by full name
    LAB5_QUERY22 = "SELECT * FROM passenger ORDER BY full_name DESC"
    
    # 23. Output passengers sorted by full name where the first letter of full name is 'A' or phone number starts with +37544
    LAB5_QUERY23 = """
    SELECT * FROM passenger
    WHERE full_name LIKE 'A%' OR mobile_phone LIKE '+37544%'
    ORDER BY full_name
    """
    
    # 24. Output first 5 employees with work experience more than 10
    LAB5_QUERY24 = "SELECT * FROM employee WHERE experience > 10 LIMIT 5"
    
    # 25. Select only engineers
    LAB5_QUERY25 = "SELECT * FROM employee WHERE position = 'инженер'"
    
    # 26. Sort employees by passport number in reverse order
    LAB5_QUERY26 = "SELECT * FROM employee ORDER BY passport_data DESC"
    
    # 27. Output employees with all positions except 'Проводник', sorted by full name
    LAB5_QUERY27 = "SELECT * FROM employee WHERE position != 'Проводник' ORDER BY full_name"
    
    # 28. Tickets where carriage number equals the carriage count of the train
    LAB5_QUERY28 = """
    SELECT t.*
    FROM ticket t
    INNER JOIN schedule s ON t.ticket_id = s.ticket_id
    INNER JOIN train tr ON s.train_id = tr.train_id
    WHERE t.carriage_number = tr.carriage_count
    """
    
    # 29. All trains with corresponding tickets for the last carriage in each train
    LAB5_QUERY29 = """
    SELECT tr.*, t.*
    FROM train tr
    LEFT JOIN ticket t ON tr.carriage_count = t.carriage_number
    LEFT JOIN schedule s ON t.ticket_id = s.ticket_id AND s.train_id = tr.train_id
    """
    
    # 30. All tickets with cost more than 5 and corresponding last carriages of trains
    LAB5_QUERY30 = """
    SELECT t.*, tr.*
    FROM ticket t
    INNER JOIN schedule s ON t.ticket_id = s.ticket_id
    INNER JOIN train tr ON s.train_id = tr.train_id
    WHERE t.price > 5 AND t.carriage_number = tr.carriage_count
    """
    
    # 31. Output trains with corresponding tickets for the last carriage, not for freight trains, with price more than 5 and carriage numbers greater than 12
    LAB5_QUERY31 = """
    SELECT tr.*, t.*
    FROM train tr
    LEFT JOIN ticket t ON tr.carriage_count = t.carriage_number
    LEFT JOIN schedule s ON t.ticket_id = s.ticket_id AND s.train_id = tr.train_id
    WHERE tr.type != 'Грузовой' AND t.price > 5 AND tr.carriage_count > 12
    """
    
    # 32. Tickets with price more than 5, not freight, for one carriage of the train
    LAB5_QUERY32 = """
    SELECT t.*, tr.*
    FROM ticket t
    INNER JOIN schedule s ON t.ticket_id = s.ticket_id
    INNER JOIN train tr ON s.train_id = tr.train_id
    WHERE t.price > 5 AND tr.type != 'Грузовой' AND t.carriage_number = 1
    """
    
    # 33. Services with employees who will provide them
    LAB5_QUERY33 = """
    SELECT s.*, e.full_name
    FROM service s
    INNER JOIN service_assignment sa ON s.service_id = sa.service_id
    INNER JOIN employee e ON sa.employee_id = e.employee_id
    """
    
    # 34. Employees with their positions and services they provide
    LAB5_QUERY34 = """
    SELECT e.full_name, e.position, s.service_name
    FROM employee e
    LEFT JOIN service_assignment sa ON e.employee_id = sa.employee_id
    LEFT JOIN service s ON sa.service_id = s.service_id
    """
    
    # 35. All services and employees who will provide them
    LAB5_QUERY35 = """
    SELECT s.*, e.*
    FROM service s
    RIGHT JOIN service_assignment sa ON s.service_id = sa.service_id
    RIGHT JOIN employee e ON sa.employee_id = e.employee_id
    """
    
    # 36. Full join of services and employees
    LAB5_QUERY36 = """
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
    
    # 37. Cartesian product of all services and employees
    LAB5_QUERY37 = """
    SELECT s.*, e.*
    FROM service s
    CROSS JOIN employee e
    """
    
    # 38. Platform location with departure and arrival time and with track count more than 2
    LAB5_QUERY38 = """
    SELECT p.location, s.arrival_time, s.departure_time, p.track_count
    FROM platform p
    INNER JOIN schedule s ON p.platform_id = s.platform_id
    WHERE p.track_count > 2
    """
    
    # 39. Schedules with track locations with capacity more than 400
    LAB5_QUERY39 = """
    SELECT s.*, p.location
    FROM schedule s
    LEFT JOIN platform p ON s.platform_id = p.platform_id
    WHERE p.capacity > 400
    """
    
    # 40. Departure time of train 2 with platform location
    LAB5_QUERY40 = """
    SELECT s.departure_time, p.location
    FROM schedule s
    INNER JOIN platform p ON s.platform_id = p.platform_id
    WHERE s.train_id = 2
    """
    
    # 41. All data about platform 4
    LAB5_QUERY41 = "SELECT * FROM platform WHERE platform_id = 4"
    
    # 42. Cartesian product 'Platform 1 Minsk-Passenger' with all schedules (first 5)
    LAB5_QUERY42 = """
    SELECT p.*, s.*
    FROM platform p
    CROSS JOIN schedule s
    WHERE p.location LIKE '%1%Минск%' AND p.location LIKE '%Пассажирский%'
    LIMIT 5
    """
    
    # 43. Services provided by drivers and their full names
    LAB5_QUERY43 = """
    SELECT s.service_name, e.full_name
    FROM service s
    INNER JOIN service_assignment sa ON s.service_id = sa.service_id
    INNER JOIN employee e ON sa.employee_id = e.employee_id
    WHERE e.position LIKE '%машинист%'
    """
    
    # 44. All drivers and services they provide
    LAB5_QUERY44 = """
    SELECT e.*, s.service_name
    FROM employee e
    LEFT JOIN service_assignment sa ON e.employee_id = sa.employee_id
    LEFT JOIN service s ON sa.service_id = s.service_id
    WHERE e.position LIKE '%машинист%'
    """
    
    # 45. All technical services and employees providing them
    LAB5_QUERY45 = """
    SELECT s.*, e.*
    FROM service s
    RIGHT JOIN service_assignment sa ON s.service_id = sa.service_id
    RIGHT JOIN employee e ON sa.employee_id = e.employee_id
    WHERE s.type = 'Техническая'
    """
    
    # 46. Full join showing all engineers providing technical services
    LAB5_QUERY46 = """
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
    
    # 47. Cartesian product of services and specific employee (first 5)
    LAB5_QUERY47 = """
    SELECT s.*, e.*
    FROM service s
    CROSS JOIN employee e
    WHERE e.employee_id = 1
    LIMIT 5
    """
    
    # 48. Trains with speed more than 100 and their arrival and departure times
    LAB5_QUERY48 = """
    SELECT tr.*, s.arrival_time, s.departure_time
    FROM train tr
    INNER JOIN schedule s ON tr.train_id = s.train_id
    WHERE tr.speed > 100
    """
    
    # 49. Arrival and departure times for trains with speed more than 100
    LAB5_QUERY49 = """
    SELECT s.arrival_time, s.departure_time, tr.type, tr.speed
    FROM schedule s
    INNER JOIN train tr ON s.train_id = tr.train_id
    WHERE tr.speed > 100
    """
    
    # 50. Arrival and departure times of trains with speed more than 100, even if they don't have a schedule
    LAB5_QUERY50 = """
    SELECT tr.*, s.arrival_time, s.departure_time
    FROM train tr
    LEFT JOIN schedule s ON tr.train_id = s.train_id
    WHERE tr.speed > 100
    """
    
    # 51. Full join of trains with type 'Express' and trains with departure time less than 12:00:00
    LAB5_QUERY51 = """
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
    
    # 52. Cartesian product of trains with type 'Express' with all schedules (first 5)
    LAB5_QUERY52 = """
    SELECT tr.*, s.*
    FROM train tr
    CROSS JOIN schedule s
    WHERE tr.type = 'Скорый'
    LIMIT 5
    """
    
    # 53. Seat numbers and full names of passengers with ticket price more than 7
    LAB5_QUERY53 = """
    SELECT t.seat_number, p.full_name
    FROM ticket t
    INNER JOIN passenger p ON t.passenger_id = p.passenger_id
    WHERE t.price > 7
    """
    
    # 54. Ticket cost with price more than 7 and passengers on corresponding seats
    LAB5_QUERY54 = """
    SELECT t.price, t.seat_number, p.full_name
    FROM ticket t
    INNER JOIN passenger p ON t.passenger_id = p.passenger_id
    WHERE t.price > 7
    """
    
    # 55. Seat and full names of passengers whose tickets cost more than 7
    LAB5_QUERY55 = """
    SELECT t.seat_number, p.full_name
    FROM ticket t
    LEFT JOIN passenger p ON t.passenger_id = p.passenger_id
    WHERE t.price > 7
    """
    
    # 56. Full join showing tickets and passengers with discounted tickets and price above 7
    LAB5_QUERY56 = """
    SELECT t.*, p.*
    FROM ticket t
    LEFT JOIN passenger p ON t.passenger_id = p.passenger_id
    WHERE p.remark LIKE '%льготный%' AND t.price > 7

    UNION

    SELECT t.*, p.*
    FROM ticket t
    RIGHT JOIN passenger p ON t.passenger_id = p.passenger_id
    WHERE p.remark LIKE '%льготный%' AND t.price > 7
    """
    
    # 57. Cartesian product of all tickets and passengers with price more than 7
    LAB5_QUERY57 = """
    SELECT t.*, p.*
    FROM ticket t
    CROSS JOIN passenger p
    WHERE t.price > 7
    """
    
    # 58. Ticket data and departure time that cost more than 7
    LAB5_QUERY58 = """
    SELECT t.*, s.departure_time
    FROM ticket t
    INNER JOIN schedule s ON t.ticket_id = s.ticket_id
    WHERE t.price > 7
    """
    
    # 59. All data from schedules and data from tickets that cost more than 7
    LAB5_QUERY59 = """
    SELECT s.*, t.*
    FROM schedule s
    LEFT JOIN ticket t ON s.ticket_id = t.ticket_id
    WHERE t.price > 7
    """
    
    # 60. All tickets with seats and their departure and arrival times before 12:00:00
    LAB5_QUERY60 = """
    SELECT t.seat_number, s.arrival_time, s.departure_time
    FROM ticket t
    INNER JOIN schedule s ON t.ticket_id = s.ticket_id
    WHERE s.departure_time < '12:00:00' AND s.arrival_time < '12:00:00'
    """
    
    # 61. Full join of tickets less than 7 and departure and arrival times after 12:00:00
    LAB5_QUERY61 = """
    SELECT t.*, s.*
    FROM ticket t
    LEFT JOIN schedule s ON t.ticket_id = s.ticket_id
    WHERE t.price < 7 AND s.departure_time > '12:00:00' AND s.arrival_time > '12:00:00'

    UNION

    SELECT t.*, s.*
    FROM ticket t
    RIGHT JOIN schedule s ON t.ticket_id = s.ticket_id
    WHERE t.price < 7 AND s.departure_time > '12:00:00' AND s.arrival_time > '12:00:00'
    """
    
    # 62. Cartesian product of tickets more than 7 and departure and arrival times before 12:00:00 (first 5)
    LAB5_QUERY62 = """
    SELECT t.*, s.*
    FROM ticket t
    CROSS JOIN schedule s
    WHERE t.price > 7 AND s.departure_time < '12:00:00' AND s.arrival_time < '12:00:00'
    LIMIT 5
    """

    # Lab Work 6 - Aggregate, Subquery, and Set Operation Queries
    
    # 1. Output average speed value and count of rows in 'year of manufacture' column
    LAB6_QUERY1 = "SELECT AVG(speed) AS avg_speed, COUNT(year_manufactured) AS count_year FROM train"
    
    # 2. Output total sum of ticket costs, minimum seat number, maximum carriage number
    LAB6_QUERY2 = "SELECT SUM(price) AS total_price, MIN(seat_number) AS min_seat, MAX(carriage_number) AS max_carriage FROM ticket"
    
    # 3. Output unique service names, average cost of given service type more than 1000, earliest execution day for each service type
    LAB6_QUERY3 = """
    SELECT DISTINCT service_name, 
           AVG(price) AS avg_price,
           MIN(service_date) AS earliest_date
    FROM service
    GROUP BY service_name
    HAVING AVG(price) > 1000
    """
    
    # 4. Output values that match one of three patterns: 'from the head of the train', 'from the tail of the train' or 'middle of the train', 
    # departure time matches the 10th hour, departure time that is greater than all departure times among records with date equal to 15th
    LAB6_QUERY4 = """
    SELECT carriage_enumeration, departure_time
    FROM schedule
    WHERE carriage_enumeration IN ('с головы поезда', 'с хвоста поезда', 'середины состава')
      AND departure_time LIKE '10:%'
      AND departure_time > (SELECT MAX(departure_time) FROM schedule WHERE date LIKE '%-15-%')
    """
    
    # 5. Output two merged parts of tables Platform and Train into one common selection without duplicates
    LAB6_QUERY5 = """
    SELECT capacity FROM platform
    UNION
    SELECT carriage_count FROM train
    """
    
    # 6. Output two merged selections from Passenger table, leaving only common rows without duplicates
    LAB6_QUERY6 = """
    SELECT full_name FROM passenger
    WHERE remark LIKE '%льготный%'
    INTERSECT
    SELECT full_name FROM passenger
    WHERE mobile_phone LIKE '+375%'
    """
    
    # 7. Output unique rows from first table, excluding matching values from second
    LAB6_QUERY7 = """
    SELECT position FROM employee
    EXCEPT
    SELECT service_name FROM service
    """