-- ============================================================================
-- SQL Script for Creating Railway Station Database Schema
-- RWSDBv2.1 - Railway Station Database System v2.1
-- Laboratory Work №1 - Variant 18
-- Belarusian Region Data
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- LOOKUP TABLES (Справочники)
-- ============================================================================

-- Table: train (Поезда) - LOOKUP TABLE
CREATE TABLE IF NOT EXISTS public.train (
    train_number VARCHAR(20) PRIMARY KEY,
    speed INTEGER CHECK (speed > 0 AND speed <= 400),
    year_of_manufacture INTEGER CHECK (year_of_manufacture >= 1900 AND year_of_manufacture <= 2100),
    type VARCHAR(255),
    number_of_cars INTEGER CHECK (number_of_cars > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: platform (Платформы) - LOOKUP TABLE
CREATE TABLE IF NOT EXISTS public.platform (
    platform_number VARCHAR(10) PRIMARY KEY,
    capacity INTEGER CHECK (capacity > 0),
    location VARCHAR(255),
    number_of_tracks INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: service (Услуги) - LOOKUP TABLE
CREATE TABLE IF NOT EXISTS public.service (
    service_number VARCHAR(20) PRIMARY KEY,
    service_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) CHECK (price >= 0),
    type VARCHAR(100),
    date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: employee (Сотрудники) - LOOKUP TABLE
CREATE TABLE IF NOT EXISTS public.employee (
    employee_number VARCHAR(20) PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    position VARCHAR(255),
    work_experience INTEGER DEFAULT 0,
    passport_information VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- OPERATIONAL TABLES (Операционные таблицы)
-- ============================================================================

-- Table: schedule (Расписание) - MAIN OPERATIONAL TABLE
CREATE TABLE IF NOT EXISTS public.schedule (
    schedule_number VARCHAR(20) PRIMARY KEY,
    arrival_time TIME,
    departure_time TIME,
    date DATE DEFAULT CURRENT_DATE,
    carriage_numbering VARCHAR(100),
    train_number VARCHAR(20),
    platform_number VARCHAR(10),
    ticket_number VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_schedule_train FOREIGN KEY (train_number)
        REFERENCES public.train(train_number) MATCH SIMPLE
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_schedule_platform FOREIGN KEY (platform_number)
        REFERENCES public.platform(platform_number) MATCH SIMPLE
        ON UPDATE CASCADE ON DELETE SET NULL
);

-- Table: passenger (Пассажиры)
CREATE TABLE IF NOT EXISTS public.passenger (
    passenger_number VARCHAR(20) PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    passport_number VARCHAR(20) UNIQUE NOT NULL,
    mobile_phone VARCHAR(20),
    feature TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: ticket (Билеты)
CREATE TABLE IF NOT EXISTS public.ticket (
    ticket_number VARCHAR(20) PRIMARY KEY,
    carriage_number VARCHAR(10),
    ticket_price DECIMAL(10, 2) CHECK (ticket_price >= 0),
    seat_number VARCHAR(10),
    passenger_number VARCHAR(20),
    train_number VARCHAR(20),
    purchase_date DATE DEFAULT CURRENT_DATE,
    travel_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_ticket_passenger FOREIGN KEY (passenger_number)
        REFERENCES public.passenger(passenger_number) MATCH SIMPLE
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_ticket_train FOREIGN KEY (train_number)
        REFERENCES public.train(train_number) MATCH SIMPLE
        ON UPDATE CASCADE ON DELETE SET NULL
);

-- ============================================================================
-- INDEXES
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_schedule_date ON public.schedule(date);
CREATE INDEX IF NOT EXISTS idx_schedule_train ON public.schedule(train_number);
CREATE INDEX IF NOT EXISTS idx_schedule_platform ON public.schedule(platform_number);
CREATE INDEX IF NOT EXISTS idx_schedule_arrival ON public.schedule(arrival_time);

CREATE INDEX IF NOT EXISTS idx_ticket_passenger ON public.ticket(passenger_number);
CREATE INDEX IF NOT EXISTS idx_ticket_train ON public.ticket(train_number);
CREATE INDEX IF NOT EXISTS idx_ticket_purchase_date ON public.ticket(purchase_date);

CREATE INDEX IF NOT EXISTS idx_passenger_name ON public.passenger(full_name);
CREATE INDEX IF NOT EXISTS idx_passenger_passport ON public.passenger(passport_number);

CREATE INDEX IF NOT EXISTS idx_train_type ON public.train(type);
CREATE INDEX IF NOT EXISTS idx_platform_location ON public.platform(location);
CREATE INDEX IF NOT EXISTS idx_service_type ON public.service(type);
CREATE INDEX IF NOT EXISTS idx_employee_position ON public.employee(position);

-- ============================================================================
-- VIEWS
-- ============================================================================

-- View: schedule_details
CREATE OR REPLACE VIEW schedule_details AS
SELECT
    s.schedule_number,
    s.arrival_time,
    s.departure_time,
    s.date,
    s.carriage_numbering,
    t.train_number,
    t.type AS train_type,
    t.speed,
    t.number_of_cars,
    p.platform_number,
    p.location AS platform_location,
    p.capacity
FROM public.schedule s
JOIN public.train t ON s.train_number = t.train_number
LEFT JOIN public.platform p ON s.platform_number = p.platform_number
ORDER BY s.date, s.arrival_time;

-- View: ticket_details
CREATE OR REPLACE VIEW ticket_details AS
SELECT
    t.ticket_number,
    t.carriage_number,
    t.seat_number,
    t.ticket_price,
    t.purchase_date,
    t.travel_date,
    p.passenger_number,
    p.full_name AS passenger_name,
    p.passport_number,
    p.mobile_phone,
    tr.train_number AS train_number,
    tr.type AS train_type,
    tr.speed
FROM public.ticket t
JOIN public.passenger p ON t.passenger_number = p.passenger_number
JOIN public.train tr ON t.train_number = tr.train_number
ORDER BY t.purchase_date DESC;

-- View: train_schedule_summary
CREATE OR REPLACE VIEW train_schedule_summary AS
SELECT
    s.schedule_number,
    t.train_number,
    t.type AS train_type,
    s.arrival_time,
    s.departure_time,
    s.date AS schedule_date,
    p.platform_number,
    p.location AS platform_location
FROM public.schedule s
JOIN public.train t ON s.train_number = t.train_number
LEFT JOIN public.platform p ON s.platform_number = p.platform_number
ORDER BY s.date, s.arrival_time;

-- View: ticket_sales_summary
CREATE OR REPLACE VIEW ticket_sales_summary AS
SELECT
    t.ticket_number,
    t.seat_number,
    t.ticket_price,
    t.purchase_date,
    t.travel_date,
    p.full_name AS passenger_name,
    p.passport_number,
    tr.train_number,
    tr.type AS train_type
FROM public.ticket t
JOIN public.passenger p ON t.passenger_number = p.passenger_number
JOIN public.train tr ON t.train_number = tr.train_number
ORDER BY t.purchase_date DESC;

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON TABLE public.train IS 'Справочник поездов';
COMMENT ON TABLE public.platform IS 'Справочник платформ';
COMMENT ON TABLE public.service IS 'Справочник услуг';
COMMENT ON TABLE public.employee IS 'Справочник сотрудников';
COMMENT ON TABLE public.schedule IS 'Расписание - основная операционная таблица';
COMMENT ON TABLE public.passenger IS 'Пассажиры';
COMMENT ON TABLE public.ticket IS 'Билеты';

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================
