# Senior Data Enginer Tech Challenge

## Section2: Databases

---

Mandatory to complete section 1.

Pre-requisities : Install Docker and pull postgres DB from Dockerhub

- Execute below command in windows terminal (or) powershell terminal to download postgres DB from Docker hub
<br> `docker pull postgres`
- Below command to setup postgres DB with name, password and port allocation
<br> `docker run --name postgres-db -e POSTGRES_PASSWORD=docker -p 5432:5432 -d postgres`
- Use <b>Dockerfile</b> provided (which consumes ecommerce.sql) and place under the location where postgres DB is setup. Then, execute below command in terminal for DDL execution as per the given requirements
<br> `docker build -t my-postgres-db ./`

Note: ecommerce.sql script provided this repo has necessary DDL scripts to create tables

---

ERD: Refer to ERD_Model.png for the ERD model design.
There are three tables as per the design requirements.
- Customer to Orders Cardinality : 1 to N
- Orders to Products Cardinality : N to N

Tables:
- Orders
- Customer
- Products

---

Write a SQL statement for each of the following task:

- Which are the top 10 members by spending ?
<br> `select membership_id, sum(total_items_price) from  orders groupby membership_id orderby sum(total_items_price) desc limit 10;`

- Which are the top 3 items that are frequently brought by members ?
<br> `select product_id, sum(total_units) from  orders groupby product_id orderby sum(total_units) desc limit 3;
`

