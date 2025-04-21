DO $$
DECLARE
    first_names TEXT[] := ARRAY['James', 'Mary', 'John', 'Patricia', 'Robert'];
    last_names TEXT[] := ARRAY['Smith', 'Johnson', 'Williams', 'Brown', 'Jones'];
    departments TEXT[] := ARRAY['backend', 'frontend', 'ios', 'android'];
    i INT;
    random_name TEXT;
    random_department TEXT;
    lat FLOAT;
    lon FLOAT;
    ip TEXT;
BEGIN
    FOR i IN 1..1000 LOOP
        random_name := first_names[1 + floor(random() * array_length(first_names, 1))::int] || ' ' ||
                       last_names[1 + floor(random() * array_length(last_names, 1))::int];

        random_department := departments[1 + floor(random() * array_length(departments, 1))::int];

        lat := round((random() * 180 - 90)::numeric, 6);
        lon := round((random() * 360 - 180)::numeric, 6);

        ip := (
            (trunc(random() * 256)::int)::text || '.' ||
            (trunc(random() * 256)::int)::text || '.' ||
            (trunc(random() * 256)::int)::text || '.' ||
            (trunc(random() * 256)::int)::text
        );

        INSERT INTO developers (name, department, geolocation, last_known_ip, is_available)
        VALUES (
            random_name,
            random_department,
            ST_GeogFromText('SRID=4326;POINT(' || lon || ' ' || lat || ')'),
            ip::INET,
            (random() > 0.5)
        );
    END LOOP;
END $$;

