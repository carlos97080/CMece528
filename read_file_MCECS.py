
"""
Carlos Mariscal
ECE 528 
K-L Project
"""
import sys




if __name__ == '__main__':
  
    options = sys.argv[1:]  
    try:
       file_handle = open(options[0],'r')
    except:
        sys.exit('Input file error')
        
    #file_handle = open('./input.txt','r')
        
    node = 0
    graph_dict = {}
    
    for line in file_handle:
        temp = line.split(' ')
        # First line of input file, graph properties
        if node == 0:
            num_of_vertex = int(temp[0])
            num_of_edges = int(temp[1])
            node = node + 1
        # Rest of input file is the description of the graph 
        # Lets put in in a dictionary
        else:
            node_connections = sorted(map(int,temp))
            graph_dict[str(node)] = node_connections
            node = node + 1
    # lets make sure the input file is correct by checking number of nodes matches 
    # with the number of processed lines
    num_nodes = node -1
    
       
    # lets get all the edges withouth repetition
    edges = []
    # Lets build a list of all edges including repetitions i.e. (1,2)=(2,1)
    for node in graph_dict.keys():
        for edge in graph_dict[node]:
            edges.append([int(node),edge])
    # Lets remove all edges that repeat i.e (1,2)=(2,1)
    for edge in edges:
        temp = list(reversed(edge))
        if temp in edges:
            edges.remove(temp)
        
    if num_nodes != num_of_vertex:
        sys.exit('\n**********\nERROR: Number of nodes does not match data.\n')
    if len(edges) != num_of_edges:
        sys.exit('\n**********\nERROR: Number of edges does not match data.\n')
    
    # If the number of edges not even add dummy edge 
    if num_of_vertex % 2:
        num_of_vertex = num_of_vertex +1
        # Create list of partitions
        partitions = [range(1,num_of_vertex/2+1),range(num_of_vertex/2+1,num_of_vertex+1)]
        partitions[-1].remove(max(partitions[-1]))
    else:
        # Create list of partitions
        partitions = [range(1,num_of_vertex/2+1),range(num_of_vertex/2+1,num_of_vertex+1)]
    
    # Print out partition info
    num_partitions = 0
    print 'Iteration 1'
    for partition in partitions:
        print 'Partition', num_partitions + 1, partition
        num_partitions = num_partitions + 1    
    
    
    # Calculate cost of partition
    count = 0
    # Need to iterate thru all partitions
    # lets crete a list from 0 to 1 minus the number of partitions since 
    # we do not have to check teh last one. (checking all other is the same)
    for partition in range(num_partitions-1):
        # Lets iterate over all nodes in the partition        
        for node in partitions[partition]:
            # lets interate on all partiions that are not the current one
            for other_partition in range(partition+1,num_partitions):
                # Lets get all edges per node in partition
                for node_second in partitions[other_partition]:
                    # Lets check if the node has an edge to current node
                    if node in graph_dict[str(node_second)]:
                        count = count + 1
    print 'Cost of the partition = ', count





















