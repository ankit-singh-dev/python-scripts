import networkx as nx
import matplotlib.pyplot as plt
import csv


def read_from_csv_file():
    print('started reading csv file')
    study_treatment_dict = dict()
    with open('Dummy Data for Network.csv', mode='r') as file:
        # reading the CSV file
        csv_file = csv.reader(file)
        # logic to skip header line
        header_index = 0
        # displaying the contents of the CSV file
        for line in csv_file:
            if 0 < header_index:
                if header_index == 201:
                    break
                header_index = header_index + 1
                if line[0] is not None:
                    existing_treatments = study_treatment_dict.get(line[0].strip(), list())
                    existing_treatments.append(line[1].strip())
                    study_treatment_dict[line[0].strip()] = existing_treatments
            else:
                header_index = 1
    return study_treatment_dict


def add_edge_into_graph(graph, u, v):
    if graph.has_edge(u, v):
        graph[u][v]['weight'] += 0.1
    else:
        graph.add_edge(u, v, weight=0.1)


def create_network(studies_treatment_input):
    print('started to create network')
    graph_obj = nx.Graph()
    for key, value in studies_treatment_input.items():
        treatment_list_size = len(value)
        if treatment_list_size > 1:
            for i in range(treatment_list_size):
                for j in range(i+1, treatment_list_size):
                    add_edge_into_graph(graph_obj, value[i], value[j])
    network_diagram(graph_obj)
    print('Finished')


def network_diagram(graph_obj_input):
    # define width of edges
    weights = [graph_obj_input[u][v]['weight'] for u, v in graph_obj_input.edges()]
    # define layout of the graph
    layout = nx.shell_layout(graph_obj_input, scale=2)
    # layout = nx.spring_layout(graph_obj, scale=2)
    # define edge label
    edge_weights = nx.get_edge_attributes(graph_obj_input, "weight")
    for key in edge_weights:
        edge_weights[key] = int(edge_weights[key] * 10)
    # node degree to define node size
    node_degree = dict(nx.degree(graph_obj_input))
    # draw the graph
    nx.draw(graph_obj_input, with_labels=True, pos=layout, font_size=8, width=weights,
            node_size=[v * 50 for v in node_degree.values()])
    # draw the graph edges
    nx.draw_networkx_edge_labels(graph_obj_input, pos=layout, edge_labels=edge_weights, font_size=6)
    # nx.draw_shell(graph_obj, with_labels=True, width=weights)
    plt.savefig('plot_graph1.png', dpi=300, bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    studies_treatment_dict = read_from_csv_file()
    create_network(studies_treatment_dict)
