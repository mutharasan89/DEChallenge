# Senior Data Enginer Tech Challenge

## Section 3: System Design 1

---



When a table is created, it is assigned an owner. The initial state is that only the owner (or a superuser) can do anything with the object. Based on the requirement provided to us, each team must be granted with specific privileges using DCL commands. Usually DCL commands are executed by admins.

- Logistics team should be provided with select and update commands privileges using below DCL command 
<br>`GRANT SELECT, UPDATE ON orders TO <logistics_user>;`


- Analytics team should be provided with select only (perform analysis but cannot perform update)  privilege using below DCL command
<br>`GRANT SELECT ON orders TO <analytics_user>;`
<br>`GRANT SELECT ON products TO <analytics_user>;`

- Sales team should be provided with select, update , delete, truncate commands privileges using below DCL command
<br>`GRANT SELECT, UPDATE, DELETE, TRUNCATE ON orders TO <sales_user>;`
<br>`GRANT SELECT, UPDATE, DELETE, TRUNCATE ON products TO <sales_user>;`

