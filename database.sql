use distributed_system;

create table account (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email varchar(50),
    password varchar(20),
    created_date date,
    role_id int
);

create table roleuser (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    rolename varchar(20)
);

alter table account
add constraint fk_account_roleuser foreign key (role_id) references roleuser (id)

create table profileuser (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fullname varchar(100),
    cccd varchar(20),
    tax varchar(20),
    phone varchar(20),
    address varchar(100),
    bankcode varchar(20),
    bankname varchar(20),
    idaccount int
);

alter table profileuser
add constraint fk_profile_account foreign key (idaccount) references account (id)

create table user_avatar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idprofile int,
    pic_name varchar(100)
);

alter table user_avatar
add constraint fk_avatar_prfile foreign key (idprofile) references profileuser (id)

DELIMITER / /

CREATE PROCEDURE `login_user`(
     IN p_Email VARCHAR(50),
     IN p_Password VARCHAR(50),
     OUT idtemp INT
 )
 BEGIN
 	DECLARE user_count INT;
     DECLARE user_id INT;
     SELECT COUNT(*) INTO user_count FROM account WHERE email = p_Email AND password = p_Password;
     IF user_count = 0 THEN
         SET idtemp = 0;
     ELSE
         -- Retrieve the user id
         SELECT id INTO user_id FROM account WHERE email = p_Email AND password = p_Password ;
         SET idtemp = user_id;
     END IF;
 END/ /

DELIMITER;

insert into roleuser (rolename) values ('employee'), ('manager');

insert into
    account (
        email,
        password,
        created_date,
        role_id
    )
values (
        'pnhtuanhcmus@gmail.com',
        '123456',
        CURDATE(),
        1
    );

insert into
    account (
        email,
        password,
        created_date,
        role_id
    )
values (
        'pnhtuanjob@gmail.com',
        '123456',
        CURDATE(),
        2
    );

insert into
    profileuser (
        fullname,
        cccd,
        tax,
        phone,
        address,
        bankcode,
        bankname,
        idaccount
    )
values (
        'tuan',
        '1',
        '1',
        '1',
        '1',
        '1',
        '1',
        1
    )
insert into
    profileuser (
        fullname,
        cccd,
        tax,
        phone,
        address,
        bankcode,
        bankname,
        idaccount
    )
values (
        'tuanjob',
        '1',
        '1',
        '1',
        '1',
        '1',
        '1',
        4
    )

create table project (
    id INT AUTO_INCREMENT PRIMARY KEY,
    projecttype varchar(100)
)

insert into
    project (projecttype)
values ('leave'),
    ('work from home')

create TABLE leave_off (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task VARCHAR(50),
    projectid int
);

alter table leave_off
add constraint fk_lv_p foreign key (projectid) references project (id)

insert into
    leave_off (task, projectid)
values ('Marriage', 1),
    ("Child's marriage", 1),
    ('Death of parent', 1),
    ('Dayoff', 1),
    (null, 2);

create table user_request (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idtask int,
    idprofile int,
    startdate date,
    enddate date,
    reason nvarchar (255),
    status varchar(50)
)

alter table user_request
add constraint fk_er_task foreign key (idtask) references leave_off (id)

alter table user_request
add constraint fk_er_profile foreign key (idprofile) references profileuser (id)

create table timesheet (
    id INT AUTO_INCREMENT PRIMARY KEY,
    updatedate date,
    hours int,
    idprofile int,
    status varchar(100)
)

alter table timesheet
add constraint fk_t_profile foreign key (idprofile) references profileuser (id)

CREATE TABLE calendar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    checkin DATEtime,
    checkout datetime,
    idaccount int
);

SET SQL_SAFE_UPDATES = 0;

select *
from calendar
where
    checkout is not null
    and idaccount = % s