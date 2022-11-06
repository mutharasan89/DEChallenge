--
-- DDL Statements
--

BEGIN;

SET client_encoding = 'LATIN1';

CREATE TABLE customer (
	membership_id text NOT NULL,
	firstname text NOT NULL,
	lastname text NOT NULL,
	email text NOT NULL,
	dob DATE NOT NULL
	mobilenumber integer NOT ,
	lastlogin TIMESTAMP NOT NULL
);

CREATE TABLE orders (
	order_id integer NOT NULL,
	membership_id text NOT NULL,
	total_units integer NOT NULL,
	total_items_price real NOT NULL, 
	total_items_weight real NOT NULL,  
	product_id integer NOT NULL
);

CREATE TABLE products (
	product_name text NOT NULL,
	manufacturer_name text NOT NULL,
	cost real NOT NULL, 
	weight real NOT NULL, 
	product_id integer NOT NULL
);


ALTER TABLE ONLY customer
    ADD CONSTRAINT membership_id_pkey PRIMARY KEY (membership_id);

ALTER TABLE ONLY orders
    ADD CONSTRAINT order_id_pkey PRIMARY KEY (order_id);

ALTER TABLE ONLY products
    ADD CONSTRAINT product_id_pkey PRIMARY KEY (product_id);


COMMIT;

ANALYZE customer;
ANALYZE orders;
ANALYZE products;

