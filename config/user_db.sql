create database USER_DB
USE USER_DB

create table users (
	Id int primary key,
	Ten varchar(100) not null,
	DiaChi varchar(100) not null,
	Email varchar(100) unique not null
) 

insert into users(Id, Ten, DiaChi, Email) VALUES 
	(1,'Thuy Linh', 'Hoa Binh', 'lyn@gmail.com'),
	(2,'Ngan', 'Nam Dinh', 'Ngan@gmail.com'),
	(3,'Ha', 'Ha Noi', 'ha123@gmail.com'),
	(4,'Quynh', 'Ha Noi', 'Quynhne@gmail.com'),
	(5,'Minh', 'HCM', 'minh@gmail.com'),
	(6,'Vinh', 'Hue', 'Vin@gmail.com')
 
SELECT * FROM users