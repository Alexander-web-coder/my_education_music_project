-- Очищаем таблицы (если они уже существуют)
TRUNCATE TABLE ratings, track, "user" RESTART IDENTITY CASCADE;

-- 1. Создаем 16 случайных пользователей
INSERT INTO "user" (login, first_name, last_name, email, hashed_password)
VALUES
    ('user1', 'Иван', 'Иванов', 'ivan@example.com', 'hashed_pass_1'),
    ('user2', 'Петр', 'Петров', 'petr@example.com', 'hashed_pass_2'),
    ('user3', 'Анна', 'Сидорова', 'anna@example.com', 'hashed_pass_3'),
    ('user4', 'Мария', 'Кузнецова', 'maria@example.com', 'hashed_pass_4'),
    ('user5', 'Алексей', 'Смирнов', 'alex@example.com', 'hashed_pass_5'),
    ('user6', 'Елена', 'Попова', 'elena@example.com', 'hashed_pass_6'),
    ('user7', 'Дмитрий', 'Васильев', 'dmitry@example.com', 'hashed_pass_7'),
    ('user8', 'Ольга', 'Новикова', 'olga@example.com', 'hashed_pass_8'),
    ('user9', 'Сергей', 'Федоров', 'sergey@example.com', 'hashed_pass_9'),
    ('user10', 'Татьяна', 'Морозова', 'tanya@example.com', 'hashed_pass_10'),
    ('user11', 'Андрей', 'Волков', 'andrey@example.com', 'hashed_pass_11'),
    ('user12', 'Наталья', 'Алексеева', 'natalia@example.com', 'hashed_pass_12'),
    ('user13', 'Артем', 'Лебедев', 'artem@example.com', 'hashed_pass_13'),
    ('user14', 'Виктория', 'Семенова', 'vika@example.com', 'hashed_pass_14'),
    ('user15', 'Михаил', 'Павлов', 'misha@example.com', 'hashed_pass_15'),
   	('root', 'Админ', 'Админ', 'root@example.com', 'hashed_pass_14');

-- 2. Создаем 50 случайных треков с разными жанрами
INSERT INTO track (title, author, genre)
VALUES
    ('Bohemian Rhapsody', 'Queen', 'Rock'),
    ('Shape of You', 'Ed Sheeran', 'Pop'),
    ('Smells Like Teen Spirit', 'Nirvana', 'Rock'),
    ('Blinding Lights', 'The Weeknd', 'Pop'),
    ('Billie Jean', 'Michael Jackson', 'Pop'),
    ('Sweet Child O''Mine', 'Guns N'' Roses', 'Rock'),
    ('Uptown Funk', 'Mark Ronson ft. Bruno Mars', 'Funk'),
    ('Hotel California', 'Eagles', 'Rock'),
    ('Despacito', 'Luis Fonsi', 'Latin'),
    ('Rolling in the Deep', 'Adele', 'Pop'),
    ('Thriller', 'Michael Jackson', 'Pop'),
    ('Stairway to Heaven', 'Led Zeppelin', 'Rock'),
    ('Take On Me', 'a-ha', 'Pop'),
    ('Wonderwall', 'Oasis', 'Rock'),
    ('Bad Guy', 'Billie Eilish', 'Electropop'),
    ('Yesterday', 'The Beatles', 'Rock'),
    ('Don''t Stop Believin''', 'Journey', 'Rock'),
    ('Clocks', 'Coldplay', 'Alternative'),
    ('Radioactive', 'Imagine Dragons', 'Alternative'),
    ('Happy', 'Pharrell Williams', 'Pop'),
    ('Hey Jude', 'The Beatles', 'Rock'),
    ('Shape of My Heart', 'Sting', 'Pop'),
    ('Sweet Home Alabama', 'Lynyrd Skynyrd', 'Rock'),
    ('Viva la Vida', 'Coldplay', 'Alternative'),
    ('Smoke on the Water', 'Deep Purple', 'Rock'),
    ('Another Brick in the Wall', 'Pink Floyd', 'Rock'),
    ('Purple Haze', 'Jimi Hendrix', 'Rock'),
    ('Like a Rolling Stone', 'Bob Dylan', 'Rock'),
    ('Imagine', 'John Lennon', 'Rock'),
    ('Hallelujah', 'Jeff Buckley', 'Folk'),
    ('All Star', 'Smash Mouth', 'Rock'),
    ('Smooth', 'Santana', 'Latin'),
    ('Lose Yourself', 'Eminem', 'Hip-Hop'),
    ('Poker Face', 'Lady Gaga', 'Pop'),
    ('Sweet Dreams', 'Eurythmics', 'Pop'),
    ('Take Five', 'Dave Brubeck', 'Jazz'),
    ('Fly Me to the Moon', 'Frank Sinatra', 'Jazz'),
    ('Moon River', 'Andy Williams', 'Jazz'),
    ('My Way', 'Frank Sinatra', 'Jazz'),
    ('What a Wonderful World', 'Louis Armstrong', 'Jazz'),
    ('Autumn Leaves', 'Nat King Cole', 'Jazz'),
    ('Take the "A" Train', 'Duke Ellington', 'Jazz'),
    ('So What', 'Miles Davis', 'Jazz'),
    ('Blue in Green', 'Bill Evans', 'Jazz'),
    ('Giant Steps', 'John Coltrane', 'Jazz'),
    ('A Love Supreme', 'John Coltrane', 'Jazz'),
    ('Kind of Blue', 'Miles Davis', 'Jazz'),
    ('Time After Time', 'Cyndi Lauper', 'Pop'),
    ('Every Breath You Take', 'The Police', 'Rock'),
   	('Paint It Black', 'Rolling Stones', 'Rock');

-- 3. Создаем 150 уникальных оценок с учетом ограничений
DO $$
DECLARE
    i INTEGER := 0;
    selected_user_id INTEGER;
    selected_track_id INTEGER;
    estimate INTEGER;
    track_genre TEXT;
BEGIN
    WHILE i < 150 LOOP
        -- Выбираем случайного пользователя и трек
        selected_user_id := 1 + floor(random() * 15);
        selected_track_id := 1 + floor(random() * 50);
        
        -- Проверяем, нет ли уже такой оценки (используем явные имена таблиц)
        PERFORM 1 FROM public.ratings 
        WHERE user_id = selected_user_id AND track_id = selected_track_id;
        IF NOT FOUND THEN
            -- Базовый рейтинг (70% высоких оценок)
            IF random() < 0.7 THEN
                estimate := 4 + floor(random() * 2); -- 4 или 5
            ELSE
                estimate := 1 + floor(random() * 3); -- 1, 2 или 3
            END IF;
            
            -- Получаем жанр трека
            SELECT genre INTO track_genre FROM public.track WHERE id = selected_track_id;
            
            -- Учитываем жанровые предпочтения
            IF selected_user_id <= 5 AND track_genre = 'Rock' THEN
                estimate := LEAST(5, estimate + 1);
            ELSIF selected_user_id BETWEEN 6 AND 10 AND track_genre = 'Pop' THEN
                estimate := LEAST(5, estimate + 1);
            ELSIF selected_user_id >= 11 AND track_genre = 'Jazz' THEN
                estimate := LEAST(5, estimate + 1);
            END IF;
            
            -- Вставляем оценку
            INSERT INTO public.ratings (user_id, track_id, estimate)
            VALUES (selected_user_id, selected_track_id, estimate);
            
            i := i + 1;
        END IF;
    END LOOP;
END $$;

-- Проверяем количество созданных оценок (должно быть 150)
SELECT COUNT(*) FROM ratings;

-- Проверяем отсутствие дубликатов
SELECT user_id, track_id, COUNT(*) 
FROM ratings 
GROUP BY user_id, track_id 
HAVING COUNT(*) > 1;