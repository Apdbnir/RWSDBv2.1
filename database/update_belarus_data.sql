-- ============================================================================
-- Update Database with Belarusian Data
-- RWSDBv2.1 - Railway Station Database System v2.1
-- This script updates existing data with Belarusian regional data
-- ============================================================================

-- Update train data with Belarusian names
UPDATE public.train SET 
    type = CASE 
        WHEN train_number LIKE '001%' OR train_number LIKE '002%' OR train_number LIKE '005%' OR train_number LIKE '008%' OR train_number LIKE '011%' OR train_number LIKE '015%' OR train_number LIKE '016%' OR train_number LIKE '020%' OR train_number LIKE '024%' THEN 'Пасажырскі'
        WHEN train_number LIKE '003%' OR train_number LIKE '006%' OR train_number LIKE '009%' OR train_number LIKE '013%' OR train_number LIKE '018%' OR train_number LIKE '022%' THEN 'Хуткі'
        WHEN train_number LIKE '004%' OR train_number LIKE '007%' OR train_number LIKE '012%' OR train_number LIKE '017%' OR train_number LIKE '021%' OR train_number LIKE '025%' THEN 'Грузавы'
        WHEN train_number LIKE '010%' OR train_number LIKE '014%' OR train_number LIKE '019%' OR train_number LIKE '023%' THEN 'Прыгарадны'
        ELSE type
    END,
    train_number = CASE
        WHEN train_number = '001A' THEN '001БЧ'
        WHEN train_number = '002A' THEN '002БЧ'
        WHEN train_number = '003A' THEN '003БЧ'
        WHEN train_number = '004A' THEN '004БЧ'
        WHEN train_number = '005A' THEN '005БЧ'
        WHEN train_number = '006A' THEN '006БЧ'
        WHEN train_number = '007A' THEN '007БЧ'
        WHEN train_number = '008A' THEN '008БЧ'
        WHEN train_number = '009A' THEN '009БЧ'
        WHEN train_number = '010A' THEN '010БЧ'
        WHEN train_number = '011A' THEN '011БЧ'
        WHEN train_number = '012A' THEN '012БЧ'
        WHEN train_number = '013A' THEN '013БЧ'
        WHEN train_number = '014A' THEN '014БЧ'
        WHEN train_number = '015A' THEN '015БЧ'
        WHEN train_number = '016A' THEN '016БЧ'
        WHEN train_number = '017A' THEN '017БЧ'
        WHEN train_number = '018A' THEN '018БЧ'
        WHEN train_number = '019A' THEN '019БЧ'
        WHEN train_number = '020A' THEN '020БЧ'
        WHEN train_number = '021A' THEN '021БЧ'
        WHEN train_number = '022A' THEN '022БЧ'
        WHEN train_number = '023A' THEN '023БЧ'
        WHEN train_number = '024A' THEN '024БЧ'
        WHEN train_number = '025A' THEN '025БЧ'
        ELSE train_number
    END
WHERE train_number LIKE '0%A' OR type IN ('Passazhirskiy', 'Skorostnoy', 'Gruzovoy', 'Prigorodnyy');

-- Update employee data with Belarusian names
UPDATE public.employee SET 
    full_name = CASE 
        WHEN employee_number = 'EMP001' THEN 'Іваноў Іван Іванавіч'
        WHEN employee_number = 'EMP002' THEN 'Пятроў Пётр Пятровіч'
        WHEN employee_number = 'EMP003' THEN 'Сідараў Сідар Сідаравіч'
        WHEN employee_number = 'EMP004' THEN 'Кузняцоў Кузьма Кузьміч'
        WHEN employee_number = 'EMP005' THEN 'Попов Поп Попавіч'
        WHEN employee_number = 'EMP006' THEN 'Смірноў Смірн Смірновіч'
        WHEN employee_number = 'EMP007' THEN 'Васільеў Васіль Васільевіч'
        WHEN employee_number = 'EMP008' THEN 'Міхайлаў Міхаіл Міхайлавіч'
        WHEN employee_number = 'EMP009' THEN 'Фёдараў Фёдар Фёдаравіч'
        WHEN employee_number = 'EMP010' THEN 'Аляксееў Аляксей Аляксеевіч'
        ELSE full_name
    END,
    position = CASE 
        WHEN employee_number = 'EMP001' THEN 'Начальнік вакзала'
        WHEN employee_number = 'EMP002' THEN 'Намеснік начальніка вакзала'
        WHEN employee_number = 'EMP003' THEN 'Дыспетчар'
        WHEN employee_number = 'EMP004' THEN 'Касір'
        WHEN employee_number = 'EMP005' THEN 'Проваднік'
        WHEN employee_number = 'EMP006' THEN 'Машыніст'
        WHEN employee_number = 'EMP007' THEN 'Памочнік машыніста'
        WHEN employee_number = 'EMP008' THEN 'Дзяжурны па станцыі'
        WHEN employee_number = 'EMP009' THEN 'Прыбіральшчык'
        WHEN employee_number = 'EMP010' THEN 'Ахоўнік'
        ELSE position
    END
WHERE employee_number LIKE 'EMP%';

-- Update passenger data with Belarusian names
UPDATE public.passenger SET 
    full_name = CASE 
        WHEN passenger_number LIKE 'PASS%' THEN CONCAT('Пасажыр ', passenger_number)
        ELSE full_name
    END,
    passport_number = CASE
        WHEN passport_number NOT LIKE 'MP %' THEN CONCAT('MP ', SUBSTRING(passport_number FROM 2))
        ELSE passport_number
    END,
    mobile_phone = CASE
        WHEN mobile_phone NOT LIKE '+375%' THEN CONCAT('+375(29)', SUBSTRING(mobile_phone FROM 4))
        ELSE mobile_phone
    END
WHERE passenger_number LIKE 'PASS%';

-- Update platform data with Belarusian locations
UPDATE public.platform SET 
    location = CASE 
        WHEN platform_number LIKE '1%' OR platform_number LIKE '2%' OR platform_number LIKE '3%' OR platform_number LIKE '4%' OR platform_number LIKE '5%' THEN 'Мінск-Пасажырскі'
        WHEN platform_number LIKE '6%' OR platform_number LIKE '7%' THEN 'Прыгарадны тэрмінал'
        WHEN platform_number LIKE '8%' OR platform_number LIKE '9%' THEN 'Грузавы тэрмінал'
        WHEN platform_number LIKE '10%' THEN 'Хуткія цягнікі'
        WHEN platform_number LIKE '11%' THEN 'Брэст-Цэнтральны'
        WHEN platform_number LIKE '12%' THEN 'Гомель-Пасажырскі'
        WHEN platform_number LIKE '13%' THEN 'Віцебск-Пасажырскі'
        WHEN platform_number LIKE '14%' THEN 'Магілёў-Пасажырскі'
        WHEN platform_number LIKE '15%' THEN 'Гродна-Пасажырскі'
        ELSE location
    END
WHERE platform_number IS NOT NULL;

-- Update service data with Belarusian names
UPDATE public.service SET 
    service_name = CASE 
        WHEN service_number = 'SRV001' THEN 'Камера захоўвання багажу'
        WHEN service_number = 'SRV002' THEN 'Пакой адпачынку'
        WHEN service_number = 'SRV003' THEN 'Wi-Fi доступ'
        WHEN service_number = 'SRV004' THEN 'Таксі заказ'
        WHEN service_number = 'SRV005' THEN 'Грузчык'
        WHEN service_number = 'SRV006' THEN 'Проваднік для інвалідаў'
        WHEN service_number = 'SRV007' THEN 'Дзіцячы пакой'
        WHEN service_number = 'SRV008' THEN 'Бізнес-зала'
        WHEN service_number = 'SRV009' THEN 'Душ'
        WHEN service_number = 'SRV010' THEN 'Зарадка прылад'
        ELSE service_name
    END,
    type = CASE 
        WHEN service_number IN ('SRV001', 'SRV002', 'SRV007', 'SRV008') THEN 'Сэрвіс'
        WHEN service_number IN ('SRV003', 'SRV010') THEN 'Сувязь'
        WHEN service_number IN ('SRV004', 'SRV015') THEN 'Транспарт'
        WHEN service_number IN ('SRV005', 'SRV006') THEN 'Дапамога'
        ELSE type
    END
WHERE service_number LIKE 'SRV%';
