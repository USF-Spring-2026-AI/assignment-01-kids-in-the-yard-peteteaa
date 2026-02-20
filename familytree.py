import csv
import random


class Person:
    def __init__(self, year_born, year_died, first_name, last_name, gender, partner, children):
        self.year_born = year_born
        self.year_died = year_died
        self.first_name = first_name
        self.last_name = last_name
        self.partner = partner
        self.gender = gender
        self.children = children
    #getters and setters for the person
    def get_year_born(self):
        return self.year_born

    def set_year_born(self, year_born):
        self.year_born = year_born

    def get_year_died(self):
        return self.year_died

    def set_year_died(self, year_died):
        self.year_died = year_died

    def get_first_name(self):
        return self.first_name

    def set_first_name(self, first_name):
        self.first_name = first_name

    def get_last_name(self):
        return self.last_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def get_partner(self):
        return self.partner

    def set_partner(self, partner):
        self.partner = partner

    def get_gender(self):
        return self.gender

    def set_gender(self, gender):
        self.gender = gender

    def get_children(self):
        return self.children

    def set_children(self, children):
        self.children = children


    
    def add_child(self, child):
        self.children.append(child)

    def remove_child(self, child):
        self.children.remove(child)

  
    def get_full_name(self):
        return self.first_name + " " + self.last_name
class PersonFactory:
    def __init__(self):

        self.read_files()

    def read_files(self): #read all the csvs
        print("reading files...")
        # rank_to_probability
        with open('rank_to_probability.csv', 'r') as f:
            row = next(csv.reader(f))
            self.rank_weights = [float(x) for x in row]

        # first_names - get weights and first names
        self.first_names = {}
        with open('first_names.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            for row in reader:
                decade = int(row[0][:-1])  # "1950s" - 1950
                gender = row[1]
                key = (decade, gender)
                if key not in self.first_names:
                    self.first_names[key] = ([], [])
                self.first_names[key][0].append(row[2])
                self.first_names[key][1].append(float(row[3]))
                


        # last_names - get weights and last names
        self.last_names = {}
        with open('last_names.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                year = int(row[0][:-1])
                decade = year - year % 10
                if decade not in self.last_names:
                    self.last_names[decade] = ([], [])
                rank = int(row[1])
                self.last_names[decade][0].append(row[2])
                self.last_names[decade][1].append(self.rank_weights[rank - 1])

        # lstore life expectancy in dict
        self.life_expectancy = {}
        with open('life_expectancy.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                self.life_expectancy[int(row[0])] = float(row[1])

        # sotre the birth + marriage rates
        self.birth_marriage_rates = {}
        with open('birth_and_marriage_rates.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                decade = int(row[0][:-1])
                self.birth_marriage_rates[decade] = (float(row[1]), float(row[2]))

    def create_person(self, year_born):
        
        gender = random.choice(['male', 'female'])
        firstname, lastname = self.getname(gender, year_born, None)
        deathyear = self.deathyear(year_born)
        
        person = Person(year_born, deathyear, firstname, lastname, gender, None, [])


        return person
    

    
   
    #get the birthyear of the child (min 25-45 years after the eldest parent)
    def birthyear(self, p, number_of_children):
        eldest = 0
        year_born = p.get_year_born()
        partner = p.get_partner()
        
        if partner is None:
            eldest = p.get_year_born()
        else:
            eldest = min(year_born, partner.get_year_born())
        #get the eldest parent's birthyear

 
        #calculate the start and end years for the child's birthyear
        startyear = eldest + 25
        endyear = eldest + 45
        #return an empty list if the eldest parent is out of range 
        if startyear > 2120 :
            return[] 
        if number_of_children == 1:
            #return the average of the start and end years only one child
            return[round((startyear+endyear)/2)]
            
        years = []
        step = (endyear - startyear) / (number_of_children - 1)
        #equally spaced years between the start and end years for the number of children
        for i in range(number_of_children ):
            year = round(startyear + i * step)
            years.append(year)

        return years
    def getname(self, gender, birthyear, parentname):  # birthyear needs to be a decade 1950
        birthyear = int(birthyear)
        birth_decade = min(birthyear - birthyear % 10, 2120)  # cap to max decade in CSV
        key = (birth_decade, gender)
        names, weights = self.first_names[key]
        firstname = random.choices(names, weights=weights, k=1)[0]  # use the weighted random choice to get a random name, i used documentation from https://docs.python.org/3/library/random.html#random.choices
        if parentname:  # if parent name is provided, use the parent's last name
            lastname = parentname
        else:
            lastnames, rank_list = self.last_names[birth_decade]
            lastname = random.choices(lastnames, weights=rank_list, k=1)[0]  # use the weighted random choice to get a random last name, i used documentation from https://docs.python.org/3/library/random.html#random.choices
        return firstname, lastname
    
    def deathyear(self, year_born):  # return the death year of the person based on year_born exact year born
        life_expectancy = self.life_expectancy.get(year_born)
        
       
        random_variation = random.randint(-10, 10)  # add a random variation to the life expectancy
        return round(year_born + life_expectancy + random_variation)
    def partner(self, person):  # takes decade and returns the birth and marriage rates for the decade
        partner = person.get_partner()
        year_born = person.get_year_born()
        decade = year_born - year_born % 10
        rates = self.birth_marriage_rates.get(decade)
        birth_rate, marriage_rate = rates

        if partner is None and random.random() < marriage_rate :  # if married generate a partner
            partnerbirthyear = max(1950, min(year_born + random.randint(-10, 10), 2120))  # clamp to 1950-2120
            partnergender = random.choice(['male', 'female'])#gender of the partner
            partnerfirstname, partnerlastname = self.getname(partnergender, partnerbirthyear, None)
            deathyear = self.deathyear(partnerbirthyear)
            partner = Person(partnerbirthyear, deathyear, partnerfirstname, partnerlastname, partnergender, None, [])
            person.set_partner(partner)  # set the partner of the person
            partner.set_partner(person)
        
        number_of_children = round(birth_rate + random.uniform(-1.5, 1.5))  # add a random variation to the birth rate
        if number_of_children > 0:  # if there are children, generate a child
            childbirthyears = self.birthyear(person, number_of_children)  # get array of birth years for the children
            for childbirthyear in childbirthyears: # for each child, generate a child
                if childbirthyear > 2120:  # no one born after 2120
                    continue
                childgender = random.choice(['male', 'female'])
                childfirstname, childlastname = self.getname(childgender, childbirthyear, person.get_last_name())
                deathyear = self.deathyear(childbirthyear)
                child = Person(childbirthyear, deathyear, childfirstname, childlastname, childgender, None, [])
                person.add_child(child)

            return person
        else:
            person.children = []

            return person  # if no children, return the person (no children)