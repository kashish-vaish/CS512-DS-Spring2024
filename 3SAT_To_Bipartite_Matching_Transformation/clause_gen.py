import random
import csv

def generate_variables(num_clauses):
    # Generate a list of variables
    variables = list(range(1, num_clauses + 1))
    
    # Initialize an empty list to store all variables and their copies
    all_variables = []
    
    # Create 3 copies of each variable with random signs and add to all_variables list
    for var in variables:
        var_copies = [var * random.choice([-1, 1]) for _ in range(3)]
        all_variables.extend(var_copies)
    
    random.shuffle(all_variables)
    return all_variables



def write_to_csv(variables):
    # Open a CSV file for writing
    with open('input.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        row = ""
        for index, var in enumerate(variables, start=1):
            row += str(var)
            if index % 3 == 0 and index != len(variables):
                row += ', '
            else:
                row += ' '
        csvfile.write(row.strip())

# def main():
#     # Take user input for the number of clauses needed
#     num_clauses = int(input("Enter the number of clauses needed: "))
    
#     # Generate variables
#     all_variables = generate_variables(num_clauses)
    
#     # Print the generated variables
#     print("Generated Variables:")
#     print(all_variables)
#     write_to_csv(all_variables)
# if __name__ == "__main__":
#     main()
