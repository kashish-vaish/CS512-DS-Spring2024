import time
import matplotlib.pyplot as plt
from collections import defaultdict
import networkx as nx
from networkx import bipartite as bp
from utils import * 
from clause_gen import *
from config import *

#Constructing Bipartite graph
def construct_bipartite_graph(clauses):
    graph = defaultdict(list)
    left_vertices = set()
    right_vertices = set()

    for idx, clause in enumerate(clauses):
        # Clause vertex
        left_vertex = 'C' + str(idx + 1)  
        left_vertices.add(left_vertex)
        for literal in clause:
            right_vertex = str(abs(literal))
            right_vertices.add(right_vertex)
            # Connect clause vertex to variable vertex
            graph[left_vertex].append(right_vertex)

    return graph, left_vertices, right_vertices

#Visualizing the bipartite graph
def visualize_bipartite_graph(graph, left_vertices, right_vertices,pltflg):
    G = nx.Graph()
    G.add_nodes_from(left_vertices, bipartite=0)
    G.add_nodes_from(right_vertices, bipartite=1)

    for left_vertex, right_vertices in graph.items():
        for right_vertex in right_vertices:
            G.add_edge(left_vertex, right_vertex)

    pos = nx.bipartite_layout(G, left_vertices)
    if pltflg =='Y':
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=500, font_size=10)
        plt.title("Bipartite Graph")
        plt.show()
    return G

def plot_matching(matching):
    graph = defaultdict(list)
    left_vertices = set()
    right_vertices = set()

    for idx, clause in enumerate(matching):

        left_vertices.add(idx)
        right_vertices.add(clause)
        graph[idx].append(clause)

    visualize_bipartite_graph(graph, left_vertices, right_vertices,'Y')


def find_truth_assignments(maximal_matching, clauses):
    truth_assignments = {}
    
    # Extract clauses and variables from the matching
    # matched_clauses = {clause_vertex: variable_vertex for clause_vertex, variable_vertex in maximal_matching.items() if clause_vertex.startswith('C')}
    assignment = []
    for index, clause in enumerate(clauses):
        clause_value = maximal_matching['C' + str(index + 1)]
        clause_values = [True if value == clause_value else False for value in clause]

        assignment.append(clause_values)    

    return assignment

def main():
    # Take user input for the number of clauses needed
    num_clauses = int(input("Enter the number of clauses needed: "))
    
    # Generate variables
    all_variables = generate_variables(num_clauses)
    
    print("Generating input file...")
    write_to_csv(all_variables)
    print("File generated")


    file_path = INPUT_FILE_NAME

    if check_file_format(file_path):
        print("Processing the file...")
        start = time.time()
        list_of_instances = read_3sat_instances_from_csv(file_path)

        valid_instances = clause_count_chk(list_of_instances)

        clean_instances = literal_occurence_chk(valid_instances)

        if clean_instances:
            print("Processing completed.")
            print("Initiating Bipartite Matching...")
            for instance in clean_instances:
                graph, left_vertices, right_vertices = construct_bipartite_graph(instance)

                G = visualize_bipartite_graph(graph, left_vertices, right_vertices,'N')
                matching = bp.hopcroft_karp_matching(G)

                matching_assignment = {key: value for key, value in matching.items() if key[0].isalpha()}

                print("Matching completed!")
                instance_assignment = list(graph.values())
                assignment = find_truth_assignments(matching_assignment, instance_assignment)
                print("Assignment completed")
                end = time.time()
                print("Time elapsed (in seconds) : "+ str(end-start)) 
                # print("PLotting the matching")
                # plot_matching(matching_assignment)
                write_csv(assignment, OUTPUT_ASSIGNMENT)
                write_matching(matching_assignment, OUTPUT_MATCHING)
            
    else:
        print("Incorrect file format")


if __name__ == "__main__":
    main()