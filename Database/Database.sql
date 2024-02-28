create database if not exists ecommerce2;
create table if not exists ecommerce2.products(
    id int not null auto_increment primary key,
    nome varchar(100),
    marca varchar(100),
    prezzo float
);