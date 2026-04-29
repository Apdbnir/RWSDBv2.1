-- Fix work table with unique combinations
TRUNCATE TABLE work RESTART IDENTITY CASCADE;

INSERT INTO work (train_number, employee_number) VALUES
(1, 1), (1, 2), (1, 3),
(2, 4), (2, 5), (2, 6),
(3, 7), (3, 8), (3, 9),
(4, 10), (4, 11), (4, 12),
(5, 13), (5, 14), (5, 15),
(6, 16), (6, 17), (6, 18),
(7, 19), (7, 20), (7, 21),
(8, 22), (8, 23), (8, 24),
(9, 25), (9, 26), (9, 27),
(10, 28), (10, 29), (10, 30),
(11, 1), (11, 2), (11, 3),
(12, 4), (12, 5), (12, 6),
(13, 7), (13, 8), (13, 9),
(14, 10), (14, 11), (14, 12),
(15, 13), (15, 14), (15, 15),
(16, 16), (16, 17), (16, 18),
(17, 19), (17, 20), (17, 21),
(18, 22), (18, 23), (18, 24),
(19, 25), (19, 26), (19, 27),
(20, 28), (20, 29), (20, 30),
(1, 4), (2, 7), (3, 10),
(4, 13), (5, 16), (6, 19),
(7, 22), (8, 25), (9, 28),
(10, 1), (11, 4), (12, 7),
(13, 10), (14, 13), (15, 16),
(16, 19), (17, 22), (18, 25),
(19, 28), (20, 1), (1, 5),
(2, 8), (3, 11), (4, 14),
(5, 17), (6, 20), (7, 23);

SELECT 'passenger' as table_name, COUNT(*) as count FROM passenger
UNION ALL SELECT 'train', COUNT(*) FROM train
UNION ALL SELECT 'platform', COUNT(*) FROM platform
UNION ALL SELECT 'ticket', COUNT(*) FROM ticket
UNION ALL SELECT 'schedule', COUNT(*) FROM schedule
UNION ALL SELECT 'employee', COUNT(*) FROM employee
UNION ALL SELECT 'service', COUNT(*) FROM service
UNION ALL SELECT 'appointment', COUNT(*) FROM appointment
UNION ALL SELECT 'work', COUNT(*) FROM work;