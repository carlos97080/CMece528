
"""
Carlos Mariscal
ECE 528 
K-L Project
"""
import sys
import argparse

def process_graph(graph_dict,partitions):
    total_cost = 0
    cost_of_node_ext = 0
    cost_of_node_int = 0
    A_or_B_partition = [0,1]
    node_pairs = []
    print ' '
    # Need to iterate thru both partitions
    for partition in A_or_B_partition:
        # Lets iterate over all nodes in a partition        
        for node in partitions[partition]:
            # Lets get all edges per node in partition and calc ext cost
            for node_second in partitions[not partition]:
                # build a complete list of node pairs between partitions
                # TODO avoid converting variables to int or string                 
                if int(node) in partitions[0] and node_second in partitions[1]:
                    node_pairs.append([str(node),str(node_second)])                
                # TODO check if creating node pairs is neccesary every iteration
		# Lets check if the node has an edge to current node
                if node in graph_dict[str(node_second)][0]:
                    total_cost = total_cost + 1
                    cost_of_node_ext = cost_of_node_ext + 1
            # Lets calculate internal cost
            for node_second in partitions[partition]:
                # Lets check if the node has an edge to current node
                if node in graph_dict[str(node_second)][0]:
                    cost_of_node_int = cost_of_node_int + 1
            # Lets calculate the "D" value D=external - internal cost        
            graph_dict[str(node)][1] = cost_of_node_ext - cost_of_node_int
            print 'Node - ', node            
            print 'External cost', cost_of_node_ext            
            print 'Internal cost', cost_of_node_int
            print 'D value', graph_dict[str(node)][1]
            cost_of_node_int = 0            
            cost_of_node_ext = 0    
    total_cost = total_cost/2  
    return (node_pairs, total_cost)

def calculate_gain(graph_dict,node_pairs,partitions, nodes_to_move) :
    max_gain_pair= []    
    # Lets calculate the gain 'g' g= Dx + Dy - Cxy and find the maximum 
    print '------------------------'    
    print 'Calculating gains'
    print '------------------------' 
    max_gain = -100000
    for pair in node_pairs:
        partial_gain = graph_dict[pair[0]][1] + graph_dict[pair[1]][1] 
        if partial_gain > max_gain:
            if pair in node_pairs_external:
                gain = partial_gain -2
                if gain > max_gain: 
                    max_gain = gain
                    max_gain_pair = pair
                    print 'Gain', max_gain, 'from',max_gain_pair
            else: 
                max_gain = partial_gain
                max_gain_pair = pair
                print 'Gain', max_gain, 'from',max_gain_pair
        else: print 'gain of pair',pair,' irrelevant, will not be greater than current max gain'
    nodes_to_move.append([max_gain_pair,max_gain])
    print'******************************************************'
    print 'Maximum gain=',max_gain, 'from pair',max_gain_pair
    print'******************************************************'
    print '\n=======================================\nNext iteration: recalculating new D values and gains'
    #TODO find another way of removing pair nodes
    temp = list(node_pairs)    
    for pair in temp:
        if max_gain_pair[0] in pair or max_gain_pair[1] in pair:
            node_pairs.remove(pair) 
            
    partitions[0].remove(int(max_gain_pair[0]))
    partitions[0].append(int(max_gain_pair[1]))
    partitions[1].remove(int(max_gain_pair[1]))
    partitions[1].append(int(max_gain_pair[0]))
    #TODO sorting may not be necessary
    partitions = sorted(partitions)
    
    return (node_pairs, partitions )

if __name__ == '__main__':
    #parser = argparse.ArgumentParser(description="""Prints out nodes by partition and
     #                                               cost of partition.""")
    #parser.add_argument("filename", help="""Input filename to be used for processing.""")

    #args = parser.parse_args()

    #file_handle = open(args.filename,'r')
    file_handle = open('./input2.txt','r')
        
    node = 0
    # Create a dictory for graph information the syntax is in the following form
    # graph_dict[node] = [connection to oder nodes][external -internal cost]
    graph_dict = {}
    print 'Processing file:'
    for line in file_handle:
	print line,    
        temp = line.split(' ')
        # First line of input file, graph properties
        if node == 0:
            num_of_vertex = int(temp[0])
            num_of_edges = int(temp[1])
            node = node + 1
        # Rest of input file is the description of the graph 
        # Lets put in in a dictionary
        else:
            #TODO check if need to convert to int
            node_connections = sorted(map(int,temp))
            graph_dict[str(node)] = [node_connections,[]]
            node = node + 1
    # lets make sure the input file is correct by checking number of nodes matches 
    # with the number of processed lines
    num_nodes = node -1
    # If the number of edges not even add dummy edge 
    if num_of_vertex % 2:
        num_of_vertex = num_of_vertex + 1
        # Create list of partitions
        partitions = [range(1,num_of_vertex/2+1),range(num_of_vertex/2+1,num_of_vertex+1)]
        partitions[-1].remove(max(partitions[-1]))
        num_of_vertex =num_of_vertex -1
    else:
        # Create list of partitions
        partitions = [range(1,num_of_vertex/2+1),range(num_of_vertex/2+1,num_of_vertex+1)]       
    
    edges = []
    node_pairs = []
    node_pairs_external = []
    # Lets build a list of all edges including repetitions i.e. (1,2)=(2,1)
    # and a list of node pairs between partion 1 and 2 which wil be used later 
    # in the K-L algorith 
    for node in graph_dict.keys():
        for edge in graph_dict[node][0]:
            #TODO check if convertion to int neccesary
            edges.append([int(node),edge])
            if int(node) in partitions[0] and edge in partitions[1]:
                node_pairs_external.append([node,str(edge)])
    temp1=list(edges)
    # Lets remove all edges that repeat i.e (1,2)=(2,1)
    for edge in edges:
        # have to create temp variable because reversed creates an object
        temp2 = list(reversed(edge))
        if temp2 in edges:
            edges.remove(temp2)
    # now lets makes sure all edge data is correct
    #TODO add option to ignore check
    #TODO delete list that will not need again
    for edge in edges:
        temp2 = list(reversed(edge))        
        if temp2 not in temp1:
            print 'Problem with edge: ',temp2
            sys.exit('\n**********\nERROR Missing edge data.\n') 
            
    if num_nodes != num_of_vertex:
        sys.exit('\n**********\nERROR: Number of nodes does not match data.\n')   
    if len(edges) != num_of_edges:
        sys.exit('\n**********\nERROR: Number of edges does not match data.\n')   
      
    # Print out partition info
    num_partitions = 0
    print 'Iteration 1'
    for partition in partitions:
        print 'Partition', num_partitions + 1, partition
        num_partitions = num_partitions + 1
    
    node_pairs, total_cost = process_graph(graph_dict,partitions)    
    print '+++++++++++++++++++++++++++++++++++++'    
    print 'Current Cost of the partition = ', total_cost
    print '+++++++++++++++++++++++++++++++++++++' 

    nodes_to_move = []
    max_gain_pair= [] 

    while node_pairs:
        node_pairs, partitions = calculate_gain(graph_dict,node_pairs,partitions,nodes_to_move)
        test, total_cost = process_graph(graph_dict,partitions)
        print '+++++++++++++++++++++++++++++++++++++'    
        print 'Current Cost of the partition = ', total_cost
        print '+++++++++++++++++++++++++++++++++++++' 
        
        print '\n^^^^^^^^^^^^^^\nFinal results\n^^^^^^^^^^^^^^'
        print 'Partial sum'
        sums=0
        for x in nodes_to_move:
            sums=x[1]+sums            
            print sums
        print 'Move to make node 1 and node 6 for a gain of 1'
        print 'Total cost of partition=5'
    print nodes_to_move
        
    print '++++++++++++++++++++++++++++++++++++\n++++\n'   
    nodes_to_move=[]
    partitions = [[6, 2, 3], [4, 5, 1]]
    node_pairs_external = []
    for node in graph_dict.keys():
        for edge in graph_dict[node][0]:
            #TODO check if convertion to int neccesary
            edges.append([int(node),edge])
            if int(node) in partitions[0] and edge in partitions[1]:
                node_pairs_external.append([node,str(edge)])
                
    node_pairs, total_cost = process_graph(graph_dict,partitions)  

    max_gain_pair= []
    while node_pairs:
        node_pairs, partitions = calculate_gain(graph_dict,node_pairs,partitions,nodes_to_move)
        test, total_cost = process_graph(graph_dict,partitions)
    print nodes_to_move
