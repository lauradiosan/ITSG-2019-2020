DELETE FROM account;

DELETE FROM person;

DELETE FROM role;

-- ROLE
INSERT INTO role (id, role) VALUES (1, 'PRESCHOOLAR');

-- PERSON
INSERT INTO person (id, address, birth_date, email, first_name, gender, last_name, active, role_id)
VALUES (1, 'Cluj', '2009-04-20 00:00:00', 'preschoolar@yahoo.com', 'Diana', 1, 'Truta', TRUE, 1);

-- ACCOUNT
INSERT INTO account (id, password, registration_date, username, person_id, active)
-- plaintext password: preschoolar
-- to generate bcrypt password goto link: https://www.devglan.com/online-tools/bcrypt-hash-generator
-- and select number of rounds: 6
VALUES (1, '$2a$06$ERzP5LUg1tOOVtthHhEQKOVR4AZRLD6JKtTO0JIySjlXWXnspDy0K', '2017-09-19 17:25:19', 'preschoolar', 1, TRUE);

