
"""
Carlos Mariscal
ECE 528 
K-L Project
"""
import sys
import copy

def process_graph(graph_dict,partitions):
    total_cost = 0
    cost_of_node_ext = 0
    cost_of_node_int = 0
    A_or_B_partition = [0,1]
    node_pairs_internal = []
    # Need to iterate thru both partitions
    for partition in A_or_B_partition:
        # Lets iterate over all nodes in a partition        
        for node in partitions[partition]:
            # Lets get all edges per node in partition and calc ext cost
            if node in node_to_ignore:
                continue
            for node_other_partition in partitions[not partition]:
                # build a complete list of node pairs between partitions
                if reset and graph_dict[node][1] == False and graph_dict[node_other_partition][1] == True:
                    node_pairs_internal.append([node, node_other_partition])                
		      # Lets check if the node in the other partition has an edge to current node
                if node in graph_dict[node_other_partition][0]:
                    total_cost = total_cost + 1
                    cost_of_node_ext = cost_of_node_ext + 1
            # Lets calculate internal cost
            for node_in_partition in partitions[partition]:
                # Lets check if the node has an edge to current node
                if node in graph_dict[node_in_partition][0]:
                    cost_of_node_int = cost_of_node_int + 1
            # Lets calculate the "D" value D=external - internal cost        
            graph_dict[node][2] = cost_of_node_ext - cost_of_node_int
            d_values.append(cost_of_node_ext - cost_of_node_int)            
            cost_of_node_int = 0            
            cost_of_node_ext = 0    
    total_cost = total_cost/2  
    return (node_pairs_internal, total_cost)

def calculate_gain(graph_dict,node_pairs,partitions, nodes_to_move) :
    max_gain_pair= []    
    # Lets calculate the gain 'g' g= Dx + Dy - Cxy and find the maximum    
    max_gain = -100000
    for pair in node_pairs:
        partial_gain = graph_dict[pair[0]][2] + graph_dict[pair[1]][2] 
        if partial_gain > max_gain:
            if pair[0] in graph_dict[pair[1]][0] and graph_dict[pair[0]][1] != graph_dict[pair[1]][1]:
                gain = partial_gain -2
                if gain > max_gain: 
                    max_gain = gain
                    max_gain_pair = pair
            else: 
                max_gain = partial_gain
                max_gain_pair = pair
    nodes_to_move.append([max_gain_pair,max_gain])
    node_to_ignore.append(max_gain_pair[0])
    node_to_ignore.append(max_gain_pair[1])
    
    # Lets remove the pair that gives most gain
    keep_checking = True
    counter = 0
    node1 = max_gain_pair[0]
    node2 = max_gain_pair[1]
    while keep_checking:
        try:
            pair = node_pairs[counter]            
            if node1 in pair or node2 in pair:
                node_pairs.pop(counter) 
            else:
                counter = counter + 1 
        except IndexError:
            keep_checking = False
        except:
            keep_checking = False
            print 'Unexpected error in calculating gains'
         
    partitions[0].remove((max_gain_pair[0]))
    partitions[0].append((max_gain_pair[1]))
    partitions[1].remove((max_gain_pair[1]))
    partitions[1].append((max_gain_pair[0]))
    
    return (node_pairs, partitions )

if __name__ == '__main__':
       
    options = sys.argv[1:]  
    print options    
    try:
       file_handle = open(options[0],'r')
    except:
        sys.exit('Input file error')
    file_handle = open(options[0],'r')
    # Handle fast algorithm option
    fast_process = False
    if len(options) > 1:
        if options[1] == '-f':
            print """******\nWarning: Running algorithm in this mode does not
             guarantee best possible solution\n******"""
            fast_process = True
            speed_coeff = 0.5

    # First line of input file, graph properties    
    first_line = file_handle.readline()
    first_line = first_line.rsplit()
    num_of_vertex = int(first_line[0])
    num_of_edges = int(first_line[1])
    d_values=[]
    # Create the partiitons    
    # If the number of  not even add dummy edge 
    if num_of_vertex % 2:
        num_of_vertex = num_of_vertex + 1
        # Create list of partitions
        partitions = [range(1,num_of_vertex/2+1),range(num_of_vertex/2+1,num_of_vertex+1)]
        partitions[-1].remove(max(partitions[-1]))
        num_of_vertex =num_of_vertex -1
    else:
        # Create list of partitions
        partitions = [range(1,num_of_vertex/2+1),range(num_of_vertex/2+1,num_of_vertex+1)]     
    
        
    node = 1
    # Create a dictory for graph information the syntax is in the following form
    # graph_dict[node] = [connection to oder nodes][true/false][external -internal cost]
    graph_dict = {}
    for line in file_handle:
        line = line.rsplit()
        # input file is the description of the graph 
        # Lets put in in a dictionary
        # each dictonary entry represents a node which contains node info
        # graph_dict[node][0]=edges of node
        # graph_dict[node][1]=false if node in partition 1 true otherwise
        # graph_dict[node][2]= D value of node
        graph_dict[node] = [sorted(map(int,line)),[],[]]
        if node <= partitions[0][-1]:
            graph_dict[node][1] = False
        else:
            graph_dict[node][1] = True
        node = node + 1
        
    # Need to substract one since counter is greater than line in the file 
    num_nodes = node -1
     
    # lets make sure the input file is correct by checking number of nodes matches 
    # with the number of processed lines and also check that the edge count is correct
    edges = []
    node_pairs = []
   
    # Lets build a list of all edges including repetitions i.e. (1,2)=(2,1)
    # and a list of node pairs between partion 1 and 2 which wil be used later 
    # in the K-L algorith 
    for node in graph_dict.keys():
        for edge in graph_dict[node][0]:
            edges.append([node,edge])
    temp1=list(edges)
    # Lets remove all edges that repeat i.e (1,2)=(2,1)
    for edge in edges:
        # have to create temp variable because reversed creates an object
        temp2 = list(reversed(edge))
        if temp2 in edges:
            edges.remove(temp2)
    # now lets makes sure all edge data is correct
    for edge in edges:
        temp2 = list(reversed(edge))        
        if temp2 not in temp1:
            print 'Problem with edge: ',temp2
            sys.exit('\n**********\nERROR Missing edge data.\n') 
    del temp1
    del temp2      
    if num_nodes != num_of_vertex:
        sys.exit('\n**********\nERROR: Number of nodes does not match data.\n')   
    if len(edges) != num_of_edges:
        sys.exit('\n**********\nERROR: Number of edges does not match data.\n')   
      
    keep_going = True  
    
    iteration_count = 1
    while keep_going:
        # Print out partition info
        og_partition_for_iteration = copy.deepcopy(partitions)       
        node_to_ignore =[]
        num_partitions = 0
        node_pairs =[]
        print 'Iteration ', iteration_count
        for partition in partitions:
            print 'Partition', num_partitions + 1, partition
            num_partitions = num_partitions + 1
        
        reset = True
        node_pairs, total_cost = process_graph(graph_dict,partitions)    
        reset = False
        print 'Cost of Partition', total_cost, '\n'

        nodes_to_move = []
        max_gain_pair= [] 
        
        # The 'fast' algorithm is implementing by removing nodes with large negative
        # D values. a large negative D value means that the particular node
        # has a large internal cost which means that would not be convinient
        # to move. 
        if fast_process:
            #depending on option a percentage of nodes will be removed when compared 
            # to the largest negative d value
            min_d = min(d_values) * speed_coeff
            for node in graph_dict.keys():
                if graph_dict[node][2] < min_d:
                    node_to_ignore.append(node)
            count = 0
            for node in node_to_ignore:
                count = count +1 
                keep_checking = True
                counter = 0
                while keep_checking:
                    try:
                        pair = node_pairs[counter]            
                        if node in pair:
                            node_pairs.pop(counter) 
                        else:
                            counter = counter + 1 
                    except IndexError:
                        keep_checking = False
                    except:
                        keep_checking = False
                        print 'Unexpected error in removing node pairs'        
    
        while node_pairs:           
            node_pairs, partitions = calculate_gain(graph_dict,node_pairs,partitions,nodes_to_move)
            if node_pairs: 
                ignore, ignore2 = process_graph(graph_dict,partitions)
                
        partial_sum=0
        max_sum = 0
        node_counter = 1
        node_counter_max = 0
        # Lets calculate the partial sum and figure out which nodes to move
        for nodes in nodes_to_move:
            partial_sum = nodes[1] + partial_sum
            if partial_sum > max_sum:
                max_sum = partial_sum
                node_counter_max = node_counter
            node_counter = node_counter +1
        
        if max_sum > 0:
            # create new partitions and new dictonary
            if not fast_process:
                partitions=list(reversed(partitions))
            else:
                partitions = og_partition_for_iteration
            for move_nodes in nodes_to_move[0:node_counter_max]:
                graph_dict[move_nodes[0][0]][1] = not graph_dict[move_nodes[0][0]][1]
                graph_dict[move_nodes[0][1]][1] = not graph_dict[move_nodes[0][1]][1]
                partitions[0].remove(move_nodes[0][0])
                partitions[0].append(move_nodes[0][1])
                partitions[1].remove(move_nodes[0][1])
                partitions[1].append(move_nodes[0][0])
        else:
            print '********\nall done\n********'
            print 'Partition 1\n', sorted(og_partition_for_iteration[0])
            print 'Partition 2\n', sorted(og_partition_for_iteration[1])
            print 'Cost of partition', total_cost    
            keep_going = False
        iteration_count = iteration_count + 1