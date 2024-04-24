
select * from permissions

select * from categories

select * from users

select * from messages


select id, name, is_private 
from categories 
where 
is_private = 0
OR
id in (3,4)
AND
name like "%e%"


select username, role
from users
where id in (select DISTINCT receiver_id
            from messages
            where sender_id = 3)
UNION
select username, role
from users
where id in(select DISTINCT sender_id
            from messages
            where receiver_id=3)


select id, text, date, sender_id, receiver_id
from messages
where sender_id = 4 and receiver_id=1
UNION
select id, text, date, sender_id, receiver_id
from messages
where sender_id = 1 and receiver_id=4
