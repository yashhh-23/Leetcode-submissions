# Write your MySQL query statement below
Select p.firstName, p.lastName, a.city, a.state
from Person p
LEFT join Address a on p.personId=a.personId;
