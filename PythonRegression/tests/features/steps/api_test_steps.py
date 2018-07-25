from aloe import *
from iota import Iota
from iota.commands.core import add_neighbors
from util import static_vals

neighbors = static_vals.TEST_NEIGHBORS
testHash = static_vals.TEST_HASH
testTrytes = static_vals.TEST_TRYTES

config = {}
<<<<<<< HEAD
responses = {'getNodeInfo':{},'getNeighbors':{},'getTips':{},'getTrytes':{}}   
=======
responses = {'getNodeInfo':{},'getNeighbors':{},'getTips':{},'getTransactionsToApprove':{},'getTrytes':{}}   

yamlPaths = ["./tests/features/machine1/output.yml","./tests/features/machine2/output.yml"]



#Configuration
@before.all
def configuration():
    logger.info('Start Node Configuration')
    machines = {}  
    count = 1  
    for i in range(len(yamlPaths)):
        stream = open(yamlPaths[i],'r')
        machine = load(stream,Loader=Loader)
        world.seeds = machine.get('seeds')
    
        nodes_final = {}
        keys = machine.keys()   
        logger.debug('Keys: %s',keys) 
        for i in keys:
            if i == 'nodes':
                for x in machine[i]:
                    name = x
                    host = machine[i][x]['host']
                    port = machine[i][x]['ports']['api']
                    logger.info(host + ":" + str(port))
                    nodes_final[name] = {'host': host, 'port': str(port)}
                    logger.info('%s configured', name)

        machine_tag = 'machine'+str(count)
        machines[machine_tag] = nodes_final
        logger.info('Machine %d configured', count)  
        count += 1

              
    world.machines = machines
    logger.info('Node Configuration Complete')
>>>>>>> 7c3e68d... Integrated ci glue code with test configuration

###
#Register API call    
@step(r'"([^"]*)" is called on "([^"]*)"')
def getNodeInfo_is_called(step,apiCall,nodeName):
    config['apiCall'] = apiCall
    config['nodeId'] = nodeName
     
<<<<<<< HEAD
    api = prepare_api_call(nodeName)
=======
        api = tests.prepare_api_call(i,machine)
        
        logger.info('Assigning call list...')
        
        callList = {
            'getNodeInfo': api.get_node_info,
            'getNeighbors': api.get_neighbors,
            'getTips': api.get_tips,
            'getTransactionsToApprove': api.get_transactions_to_approve
        }
>>>>>>> 7c3e68d... Integrated ci glue code with test configuration
    
    if apiCall == 'getNodeInfo':
        response = api.get_node_info()
    elif apiCall == 'getNeighbors':
        response = api.get_neighbors()
    elif apiCall == 'getTips':
        response = api.get_tips()
    elif apiCall == 'getTransactionsToApprove':
        response = api.get_transactions_to_approve(3)
    else:
        response = "Incorrect API call definition"
    
    assert type(response) is dict, "API call did not respond correctly: {}".format(response)
    
    responses[apiCall][nodeName] = response

###
#Response testing    
@step(r'a response with the following is returned:')
def compare_response(step):
    keys = step.hashes
    nodeId = config['nodeId']
    apiCall = config['apiCall']
    
    if apiCall == 'getNodeInfo' or apiCall == 'getTransactionsToApprove':
        response = responses['getNodeInfo'][nodeId]
        responseKeys = list(response.keys())
        responseKeys.sort()
        for i in range(len(response)):
            assert str(responseKeys[i]) == str(keys[i]['keys']), "There was an error with the response" 
    
    elif apiCall == 'getNeighbors' or apiCall == 'getTips':
        response = responses['getNeighbors'][nodeId] 
        responseKeys = list(response.keys())
        for x in range(len(response)):
            try:
                for i in range(len(response[x])):
                    assert str(responseKeys[i]) == str(keys[i])
            except:
                print("No neighbors to verify response with")        
 
 ###
 #Test GetTrytes 

@step(r'getTrytes is called with the hash static_vals.TEST_HASH')
def call_getTrytes(step):
    api = prepare_api_call(config['nodeId'])
    response = api.get_trytes(testHash)
    assert type(response) is dict, "Call may not have responded correctly: \n{}".format(response)
    responses['getTrytes'][config['nodeId']] = response

@step(r'the response should be equal to static_vals.TEST_TRYTES')
def check_trytes(step):
    response = responses['getTrytes'][config['nodeId']]
    if 'trytes' in response:
        assert response['trytes'][0] == testTrytes, "Trytes do not match"


###
#Test Add and Remove Neighbors
  
<<<<<<< HEAD
@step(r'2 neighbors are added with "([^"]*)" on "([^"]*)"')
def add_neighbors(step,apiCall,nodeName):
    config['nodeId'] = nodeName
    api = prepare_api_call(nodeName)
    response = api.add_neighbors(neighbors)
=======
@step(r'2 neighbors are added with "([^"]*)" on each node in "([^"]*)"')
def add_neighbors(step,apiCall,machine):
    logger.info('Adding neighbors')
    config['nodeId'] = world.machines[machine]
    for node in config['nodeId']:
        api = tests.prepare_api_call(node,machine)
        response = api.add_neighbors(neighbors)
        logger.debug('Addition response: %s',response)
<<<<<<< HEAD
>>>>>>> 7c3e68d... Integrated ci glue code with test configuration
=======
>>>>>>> 7c3e68d... Integrated ci glue code with test configuration
    
@step(r'"getNeighbors" is called, it should return the following neighbors:')
def check_neighbors_post_addition(step):
    containsNeighbor = check_neighbors(step)
    assert containsNeighbor[1] is True
    assert containsNeighbor[0] is True 
    
    
@step(r'"removeNeighbors" will be called to remove the same neighbors')
def remove_neighbors(step):
<<<<<<< HEAD
    api = prepare_api_call(config['nodeId'])
    response = api.remove_neighbors(neighbors)
=======
    logger.info('Removing neighbors')
    
    for node in config['nodeId']:
        api = tests.prepare_api_call(node,config['machine'])
        response = api.remove_neighbors(neighbors)
        logger.debug('Removal response: %s',response)
<<<<<<< HEAD
>>>>>>> 7c3e68d... Integrated ci glue code with test configuration
=======
>>>>>>> 7c3e68d... Integrated ci glue code with test configuration
    
@step(r'"getNeighbors" should not return the following neighbors:')
def check_neighbors_post_removal(step):
    containsNeighbor = check_neighbors(step)
    assert containsNeighbor[1] is False
    assert containsNeighbor[0] is False
            
 
    
    
      
  
  
                                
                    
    
def prepare_api_call(nodeName):
    host = world.machines[nodeName]
    address ="http://"+ host + ":14265"
    api = Iota(address)
    return api


def check_responses_for_call(apiCall):
    if len(responses[apiCall]) > 0:
        return True
    else:
        return False
    
def fetch_response(apiCall):
    return responses[apiCall]


def check_neighbors(step):
    api = prepare_api_call(config['nodeId'])
    response = api.getNeighbors()
    containsNeighbor = [False,False]
    
    for i in response:
        expectedNeighbors = step.hashes
        if type(response[i]) != int:
            for x in range(len(response[i])):    
                if expectedNeighbors[0]['neighbors'] == response[i][x]['address']:
                    containsNeighbor[0] = True  
                if expectedNeighbors[1]['neighbors'] == response[i][x]['address']:
                    containsNeighbor[1] = True  
    
    return containsNeighbor
     
    