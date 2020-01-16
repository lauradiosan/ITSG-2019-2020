create table role
(
    id   bigint auto_increment
        primary key,
    role varchar(255) null
);

create table person
(
    id         bigint auto_increment
        primary key,
    active     bit          not null,
    address    varchar(255) null,
    bio        varchar(255) null,
    birth_date datetime     null,
    email      varchar(255) null,
    first_name varchar(255) null,
    gender     int          null,
    last_name  varchar(255) null,
    skills     varchar(255) null,
    role_id    bigint       null,
    constraint FKfqfeq5nokuewxxtb44t9lw012
        foreign key (role_id) references role (id)
);

create table account
(
    id                bigint auto_increment
        primary key,
    active            bit          not null,
    password          varchar(255) null,
    registration_date datetime     null,
    username          varchar(255) null,
    person_id         bigint       null,
    constraint FKd9dhia7smrg88vcbiykhofxee
        foreign key (person_id) references person (id)
);

