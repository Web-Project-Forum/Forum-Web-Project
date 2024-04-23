select id, name, is_private 
from categories 
where 
is_private = 0
OR
id in (3,4)
AND
name like "%e%"

select * from permissions

select * from categories

select * from users