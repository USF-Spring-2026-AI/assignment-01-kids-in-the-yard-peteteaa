from familytree import PersonFactory
from familytree import Person
import csv
class FamilyTree:
    def __init__(self):
        self.personfactory = PersonFactory()
                

        self.personfactory.read_files()
        self.all_people = []
    def generate_tree(self):
        print("Generating family tree...")
        
        person1deathyear = self.personfactory.deathyear(1950)
        person2deathyear = self.personfactory.deathyear(1950)
        
        self.root_person1 = Person(1950, person1deathyear, "Desmond", "Jones", "male", None, [])
        self.root_person2 = Person(1950, person2deathyear, "Molly", "Jones", "female", None, [])
        
        # link root people
        self.root_person1.set_partner(self.root_person2)
        self.root_person2.set_partner(self.root_person1)
        
        # add root people to all people
        self.all_people.extend([self.root_person1, self.root_person2])
        #add first to que
        queue = [self.root_person1]
        
        while queue:
            person = queue.pop(0)
            
            if person.get_year_born() >= 2120:#dont add people born after 2120
                break
                
            # make partner  and children
            self.personfactory.partner(person)
            
            partner = person.get_partner() 
            if partner is not None and partner not in self.all_people:
                self.all_people.append(partner)
                
            for child in person.get_children():
                if child not in self.all_people and child.get_year_born() <= 2120:
                    self.all_people.append(child)
                    queue.append(child)
    def interactive_menu(self):
        while True:
            print("\nAre you interested in:")

            print("(T)otal number of people in the tree")
            print("Total number of people in the tree by (D)ecade")
            print("(N)ames duplicated")
            print("(Q)uit")
            
            choice = input("> ").strip().upper()
            
            if choice == 'T':
                print(f"\nThe tree contains {len(self.all_people)} people total")
            
            elif choice == 'D':
                self.printdecades()
            
            elif choice == 'N':
                self.printduplicates()
            
            elif choice == 'Q':
                break
            
            else:
                print("Invalid option. Please try again.")
            
    def printdecades(self):
        print("> D")
        decade_counts = {}
        for person in self.all_people:
            decade = person.get_year_born() - person.get_year_born() % 10
            decade_counts[decade] = decade_counts.get(decade, 0) + 1
        for decade in sorted(decade_counts):
            print(str(decade) + ": " + str(decade_counts[decade]))
    def printduplicates(self):
        print("> N")
        name_counts = {}
        for person in self.all_people:
            name = person.get_first_name() + " " + person.get_last_name()
            name_counts[name] = name_counts.get(name, 0) + 1
        duplicates = [name for name in sorted(name_counts) if name_counts[name] > 1]
        print(f"There are {len(duplicates)} duplicate names in the tree:")
        for name in duplicates:
            print("* " + name)
if __name__ == "__main__":
    tree = FamilyTree()
    tree.generate_tree()
    tree.interactive_menu()