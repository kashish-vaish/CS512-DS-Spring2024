import csv
import json
from collections import Counter
from config import *


def read_3sat_instances_from_csv(file_path):
    instances = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            instance = [tuple(map(int, clause.split())) for clause in row]
            instances.append(instance)
    return instances

def clause_count_chk(instance_list):
    valid_instances = []
    for instance in instance_list:
        #Calculating number of clauses entered
        no_of_clauses = len(instance)
        # print(f"{instance} - it has {no_of_clauses} clauses")
        no_of_literals = 0
        for clause in instance:
        #Calculating number of literals in an instance
            no_of_literals += len(clause)
        # print(f"In {instance} there are {no_of_literals} literals")
        if(no_of_literals == 3*no_of_clauses):
            valid_instances.append(instance)
    return valid_instances

def literal_occurence_chk(valid_instances):
    clean_instances = []
    for instance in valid_instances:
        var_list = []
        instance_val_flg ="Y"
        for clause in instance:
            for literal in clause:
                var_list.append(abs(literal))
        var_count = Counter(var_list)
        for element, count in var_count.items():
            if count > 3:
                instance_val_flg = "N"
                print(f"Variable {element} appears more than 3 times")
        if instance_val_flg != "N":
            clean_instances.append(instance)
    return clean_instances


def powerset(s):
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1 << x):
        yield [ss for mask, ss in zip(masks, s) if i & mask]


def check_file_format(filename):
    try:
        with open(filename, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                parts = line.strip().split(', ')
                for part_number, part in enumerate(parts, start=1):
                    numbers = part.split()
                    if len(numbers) != 3:
                        raise ValueError(f"Error in line {line_number}, Clause {part_number}: '{part}'")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return False
    except ValueError as e:
        print(e)
        return False
    return True


def write_csv(data, filename):
    if filename == OUTPUT_ASSIGNMENT:
        formatted_output = [', '.join(str(value) for value in clause).replace(',', ' ').replace('[', ',').replace(']', '')for clause in data]

        # Write the formatted output to a CSV file
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(formatted_output)

def write_matching(data, filename):
    with open(filename, 'w') as jsonfile:
        json.dump(data, jsonfile)