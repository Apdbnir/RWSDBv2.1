-- RWSDBv2.1 - Railway Station Database System v2.1
-- Belarusian Edition - New Schema based on relational specification
-- Created: 2026

-- Drop existing tables in correct order (respecting foreign keys)
DROP TABLE IF EXISTS appointment CASCADE;
DROP TABLE IF EXISTS work CASCADE;
DROP TABLE IF EXISTS service CASCADE;
DROP TABLE IF EXISTS schedule CASCADE;
DROP TABLE IF EXISTS ticket CASCADE;
DROP TABLE IF EXISTS employee CASCADE;
DROP TABLE IF EXISTS platform CASCADE;
DROP TABLE IF EXISTS train CASCADE;
DROP TABLE IF EXISTS passenger CASCADE;

-- ============================================
-- 1. passenger (Пасажыр) - Passenger table
-- ============================================
CREATE TABLE passenger (
    passenger_number SERIAL PRIMARY KEY,
    passport_number VARCHAR(20) NOT NULL UNIQUE,
    full_name VARCHAR(200) NOT NULL,
    mobile_phone VARCHAR(20),
    feature VARCHAR(100)
);

-- ============================================
-- 2. train (Цягнік) - Train table
-- ============================================
CREATE TABLE train (
    train_number SERIAL PRIMARY KEY,
    speed INTEGER NOT NULL,
    year_of_manufacture INTEGER NOT NULL,
    type VARCHAR(50) NOT NULL,
    number_of_cars INTEGER NOT NULL
);

-- ============================================
-- 3. platform (Платформа) - Platform table
-- ============================================
CREATE TABLE platform (
    platform_number SERIAL PRIMARY KEY,
    capacity INTEGER NOT NULL,
    location VARCHAR(200) NOT NULL,
    number_of_tracks INTEGER NOT NULL
);

-- ============================================
-- 4. ticket (Квіток) - Ticket table
-- ============================================
CREATE TABLE ticket (
    ticket_number SERIAL PRIMARY KEY,
    carriage_number INTEGER NOT NULL,
    ticket_price DECIMAL(10, 2) NOT NULL,
    seat_number INTEGER NOT NULL,
    passenger_number INTEGER NOT NULL,
    FOREIGN KEY (passenger_number) REFERENCES passenger(passenger_number)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================
-- 5. schedule (Расклад) - Schedule table
-- ============================================
CREATE TABLE schedule (
    schedule_number SERIAL PRIMARY KEY,
    arrival_time TIME NOT NULL,
    departure_time TIME NOT NULL,
    carriage_numbering VARCHAR(50),
    date DATE NOT NULL,
    train_number INTEGER NOT NULL,
    platform_number INTEGER NOT NULL,
    ticket_number INTEGER,
    FOREIGN KEY (train_number) REFERENCES train(train_number)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (platform_number) REFERENCES platform(platform_number)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (ticket_number) REFERENCES ticket(ticket_number)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- ============================================
-- 6. employee (Супрацоўнік) - Employee table
-- ============================================
CREATE TABLE employee (
    employee_number SERIAL PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL,
    position VARCHAR(100) NOT NULL,
    work_experience INTEGER,
    passport_information VARCHAR(50) NOT NULL
);

-- ============================================
-- 7. work (Праца) - Work assignment table (train <-> employee M:N)
-- ============================================
CREATE TABLE work (
    train_number INTEGER NOT NULL,
    employee_number INTEGER NOT NULL,
    PRIMARY KEY (train_number, employee_number),
    FOREIGN KEY (train_number) REFERENCES train(train_number)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (employee_number) REFERENCES employee(employee_number)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================
-- 8. service (Паслуга) - Service table
-- ============================================
CREATE TABLE service (
    service_number SERIAL PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    type VARCHAR(50) NOT NULL,
    date DATE NOT NULL
);

-- ============================================
-- 9. appointment (Прызначэнне) - Service assignment (employee <-> service M:N)
-- ============================================
CREATE TABLE appointment (
    employee_number INTEGER NOT NULL,
    service_number INTEGER NOT NULL,
    PRIMARY KEY (employee_number, service_number),
    FOREIGN KEY (employee_number) REFERENCES employee(employee_number)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (service_number) REFERENCES service(service_number)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================
-- Create indexes for better query performance
-- ============================================
CREATE INDEX idx_ticket_passenger ON ticket(passenger_number);
CREATE INDEX idx_schedule_train ON schedule(train_number);
CREATE INDEX idx_schedule_platform ON schedule(platform_number);
CREATE INDEX idx_schedule_ticket ON schedule(ticket_number);
CREATE INDEX idx_schedule_date ON schedule(date);
CREATE INDEX idx_work_train ON work(train_number);
CREATE INDEX idx_work_employee ON work(employee_number);
CREATE INDEX idx_appointment_employee ON appointment(employee_number);
CREATE INDEX idx_appointment_service ON appointment(service_number);

-- ============================================
-- Comments for documentation (in Belarusian)
-- ============================================
COMMENT ON TABLE passenger IS 'Інфармацыя пра пасажыраў чыгункі';
COMMENT ON TABLE train IS 'Інфармацыя пра цягнікі';
COMMENT ON TABLE platform IS 'Інфармацыя пра чыгуначныя платформы';
COMMENT ON TABLE ticket IS 'Інфармацыя пра квіткі';
COMMENT ON TABLE schedule IS 'Расклад руху цягнікоў';
COMMENT ON TABLE employee IS 'Інфармацыя пра супрацоўнікаў';
COMMENT ON TABLE work IS 'Прызначэнне супрацоўнікаў на цягнікі';
COMMENT ON TABLE service IS 'Паслугі для пасажыраў і цягнікоў';
COMMENT ON TABLE appointment IS 'Прызначэнне супрацоўнікаў на паслугі';
