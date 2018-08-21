from aloe import *
from iota import Iota
from iota.commands.core import add_neighbors
from util import static_vals

from yaml import load, Loader

import logging 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

neighbors = static_vals.TEST_NEIGHBORS
testHash = static_vals.TEST_HASH
testTrytes = static_vals.TEST_TRYTES

config = {}
responses = {'getNodeInfo':{},'getNeighbors':{},'getTips':{},'getTransactionsToApprove':{},'getTrytes':{}}   

yamlPaths = ["./tests/features/machine1/config.yml","./tests/features/machine2/config.yml"]



#Configuration
@before.all
def configuration():
    logger.info('Start Node Configuration')
    machines = {}    
    for i in range(len(yamlPaths)):
        stream = open(yamlPaths[i],'r')
        machine = load(stream,Loader=Loader)
        world.seeds = machine.get('seeds')
    
        nodes = {}
        keys = machine.keys()  
        count = 1  
        logger.debug('Keys: %s',keys)   
        for i in keys:
            if i != 'seeds' and i != 'defaults':
                name = i
                host = machine[i]['host']
                nodes[name] = host

        machine_tag = 'machine'+str(count)
        machines[machine_tag] = nodes
        count += 1
              
    world.machines = machines
    logger.info('Node Configuration Complete')

###
#Register API call    
@step(r'"([^"]*)" is called on "([^"]*)" in "([^"]*)"')
def api_method_is_called(step,apiCall,nodeName,machine):
    logger.info('%s is called on %s',apiCall,nodeName)
    config['apiCall'] = apiCall
    config['nodeId'] = nodeName
     
    api = prepare_api_call(nodeName)
    
    if apiCall == 'getNodeInfo':
        response = api.get_node_info()
        logger.debug('Node Info Response: %s',response)
    elif apiCall == 'getNeighbors':
        response = api.get_neighbors()
        logger.debug('Neighbor Response: %s',response)
    elif apiCall == 'getTips':
        response = api.get_tips()
        logger.debug('Get Tips Response Error')
    elif apiCall == 'getTransactionsToApprove':
        response = api.get_transactions_to_approve(3)
        logger.debug('Get Transactions To Approve Error')
    else:
        response = "Incorrect API call definition"
    
    
    assert type(response) is dict, response
    
    responses[apiCall][machine] = {}
    responses[apiCall][machine][nodeName] = response


###
#Response testing    
@step(r'a response with the following is returned:')
def compare_response(step):
    logger.info('Validating response')
    keys = step.hashes
    nodeId = config['nodeId']
    apiCall = config['apiCall']
    machine = config['machine']
    
    if apiCall == 'getNodeInfo' or apiCall == 'getTransactionsToApprove':
        response = responses['getNodeInfo'][machine][nodeId]
        responseKeys = list(response.keys())
        responseKeys.sort()
        logger.debug('Response Keys: %s', responseKeys)
        for i in range(len(response)):
            assert str(responseKeys[i]) == str(keys[i]['keys']), "There was an error with the response" 
    
    elif apiCall == 'getNeighbors' or apiCall == 'getTips':
        response = responses['getNeighbors'][machine][nodeId] 
        responseKeys = list(response.keys())
        logger.debug('Response Keys: %s', responseKeys)

        for x in range(len(response)):
            try:
                for i in range(len(response[x])):
                    assert str(responseKeys[i]) == str(keys[i])
            except:
                logger.debug("No values to verify response with")        
 
 ###
 #Test GetTrytes 

@step(r'getTrytes is called with the hash static_vals.TEST_HASH')
def call_getTrytes(step):

    logger.info('Testing getTrytes on static transaction')
    machine = config['machine']
    nodeId = config['nodeId']
      
    api = prepare_api_call(nodeId,machine)
    response = api.get_trytes(testHash)
    logger.debug("Call may not have responded correctly: \n%s",response)
    assert type(response) is dict 
    responses['getTrytes'][machine] = {}
    responses['getTrytes'][machine][nodeId] = response


@step(r'the response should be equal to static_vals.TEST_TRYTES')
def check_trytes(step):
    logger.info('Validating response')
    machine = config['machine']
    nodeId = config['nodeId']  
    
    response = responses['getTrytes'][machine][nodeId]
    if 'trytes' in response:
        assert response['trytes'][0] == testTrytes, "Trytes do not match"



###
#Test Add and Remove Neighbors
  
@step(r'2 neighbors are added with "([^"]*)" on "([^"]*)"')
def add_neighbors(step,apiCall,nodeName):
    config['nodeId'] = nodeName
    api = prepare_api_call(nodeName)
    response = api.add_neighbors(neighbors)
    logger.debug('Response: %s',response)
    
@step(r'"getNeighbors" is called, it should return the following neighbors:')
def check_neighbors_post_addition(step):
    logger.info('Ensuring Neighbors were added correctly')
    containsNeighbor = check_neighbors(step)
    assert containsNeighbor[1] is True
    assert containsNeighbor[0] is True 
    
    
@step(r'"removeNeighbors" will be called to remove the same neighbors')
def remove_neighbors(step):
    api = prepare_api_call(config['nodeId'])
    response = api.remove_neighbors(neighbors)
    logger.debug('Response: %s',response)
    
@step(r'"getNeighbors" should not return the following neighbors:')
def check_neighbors_post_removal(step):
    logger.info('Ensuring Neighbors were removed correctly')
    containsNeighbor = check_neighbors(step)
    assert containsNeighbor[1] is False
    assert containsNeighbor[0] is False
            
 
    
    
      
  
  
                                
                    
    
def prepare_api_call(nodeName):
    host = world.machines[nodeName]
    address ="http://"+ host + ":14265"
    api = Iota(address)
    logger.info('API call prepared for %s',address)
    return api


def check_responses_for_call(apiCall):
    if len(responses[apiCall][config['machine']]) > 0:
        return True
    else:
        return False
    
def fetch_response(apiCall):
    return responses[apiCall][config['machine']]


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
     
    