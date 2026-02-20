# AI Assignment 01 - Kids in the Yard

See assignment details on Canvas.

Answer the following questions:
● Which tool(s) did you use?
    I used cursor's agent tool and chatgpt's generative function
    I also used VSCode's autocomplete function to help me with var names and finishing code blocks
● If you used an LLM, what was your prompt to the LLM?
    I used chatgpt's chat function to process the instructions in the implementation section into a cursor prompt to feed into cursor 
    here is the prompt: 
    Cursor Prompt:
You are generating a complete object-oriented Python implementation of a Family Tree simulation.

Follow ALL requirements exactly.

✅ Overview
Build a multi-generational family tree beginning with two people born in 1950.
Generate descendants (children, grandchildren, etc.) until:
No more children can be generated OR
Year Born would exceed 2120
After generation, provide a command-line interface that allows user interaction.
📁 File Assumptions
All CSV files are in the current directory.
The implementation may use:

Basic Python file reading loops
OR
pandas.read_csv
If you use external-style logic (e.g., weighted random selection patterns), include comments explaining the approach.
🧱 Required Object-Oriented Design
Use clean PEP 8 style.
Implement the following classes:

1️⃣ Person Class
Represents one person in the family tree.
Required Attributes
first_name
last_name
year_born
year_died
gender
partner (Person or None)
children (list of Person)
parent(s) reference (optional but recommended)
Include:
Proper accessor and mutator methods (getters/setters)
__str__ method
full_name() helper
2️⃣ PersonFactory Class
Responsible for:
Reading CSV files
Generating new Person instances
Required Methods
read_files()
get_person(year_born, parent_last_names=None, directly_descended=False)
Any helper methods for:
weighted random selection
life expectancy calculation
last name probability normalization
📊 Attribute Rules
Year Born
First two people: 1950
Children:
Born evenly distributed between:
elder_parent_year + 25
elder_parent_year + 45
Stop generation if > 2120
Year Died
File: life_expectancy.csv
Determine decade of birth
Get life expectancy
Randomly assign:
expectancy ± 10 years
First Name
Files:
first_names.csv
gender_name_probability.csv (Graduate requirement)
Rules:
Based on decade of birth
Based on gender
Based on name frequency
Graduate requirement:
Apply gendered name probability adjustment
Last Name
Files:
last_names.csv
rank_to_probability.csv
Rules:
Direct descendants of original 1950 couple:
Must inherit last name of either original person
Non-direct descendants:
Select last name based on:
Rank (1–30)
Convert rank to probability via rank_to_probability.csv
Normalize probabilities (they do NOT sum to 1.0)
Partner / Spouse
File:
birth_and_marriage_rates.csv
Rules:
Use marriage_rate probability
If partner is created:
Year born within ±10 years of person
No name change
Max 1 partner
Children
File:
birth_and_marriage_rates.csv
Rules:
Based on birth_rate of birth decade
Number of children:
birth_rate ± 1.5
Round up to nearest integer
Graduate requirement:
If no partner → 1 fewer child
🌳 FamilyTree Class
Responsible for:
Storing all Person objects
Generating full tree
Handling user interaction
Attributes:
two original Person instances
master list of all persons
Required Methods:
generate_tree()
count_total_people()
count_by_decade()
find_duplicate_names()
run_cli()
💬 CLI Interface
After generating tree:
Print:

Are you interested in:
(T)otal number of people in the tree
Total number of people in the tree by (D)ecade
(N)ames duplicated

Handle input loop until user exits.

Required Outputs
Total
The tree contains X people total
By Decade
1950: 2
1960: 5
...
Duplicate Names
There are X duplicate names in the tree:

Name 1
Name 2
🎯 Technical Requirements
Use OOP
Use PEP 8 style
Use snake_case
Self-documenting variable names
Include docstrings
Avoid global variables
Use type hints
Use random module properly
Ensure reproducibility option (optional seed parameter)
🚫 Do NOT
Hardcode probabilities
Hardcode names
Ignore CSV files
Use procedural-only design
Exceed 2120 birth year
📦 Final Output
Generate:
A single clean Python script
OR
Multiple Python files (person.py, factory.py, family_tree.py, main.py)
Include clear comments explaining logic.
The code must be complete and runnable.

Now generate the full implementation.



● What differences are there between your implementation and the LLM?
    The LLM read the files at initilization time rather than in each function. It also added alot of checks to set some vars as None if they were out of range from the provided CSV data ex: a name for someone born in 2030
● What changes would you make to your implementation in general based on suggestions from the
LLM?
    I used part of the refactored version to read in all the CSV data when the PersonFactory object is initilized. My original logic can be found at this commit : 22db0c8bf59cb2856a95d763f027b65f61d30d84
● What changes would you refuse to make?
    Cursor's implementation had checks to set First/Lastnames to None if the decade couldn't be found. This allowed for a successful tree to be generated, but when you try to read a  person object with "None" as a name, python will throw a TypeError: unsupported operand type(s) for +: 'str' and 'NoneType'