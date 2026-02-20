from familytree import PersonFactory
from familytree import Person
p = Person(1980,1990, 'chang', 'wang', 'male', None, [])
print(p.get_year_born())
print(p.get_year_died())
print(p.get_first_name())
print(p.get_last_name())
print(p.get_gender())
print(PersonFactory().getname('female', 2020, 'Wang'))
print(PersonFactory().deathyear(2067 ))
p.set_partner(p)
PersonFactory().partner(p)
print(p.get_partner().get_first_name()+" "+p.get_partner().get_last_name())