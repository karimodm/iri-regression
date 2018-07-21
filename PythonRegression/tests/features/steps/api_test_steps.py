from aloe import *
from iota import Iota
from iota.commands.core import add_neighbors
from util import static_vals
from util.test_logic import api_test_logic
from yaml import load, Loader

import logging 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

neighbors = static_vals.TEST_NEIGHBORS
testHash = static_vals.TEST_HASH
testTrytes = static_vals.TEST_TRYTES

tests = api_test_logic

config = {}
responses = {'getNodeInfo':{},'getNeighbors':{},'getTips':{},'getTransactionsToApprove':{},'getTrytes':{}}   

yamlPaths = ["./tests/features/machine1/config.yml","./tests/features/machine2/config.yml"]



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
                    nodes_final[name] = host
                    logger.info('%s configured', name)

        machine_tag = 'machine'+str(count)
        machines[machine_tag] = nodes_final
        logger.info('Machine %d configured', count)  
        count += 1

              
    world.machines = machines
    logger.info('Node Configuration Complete')

###
#Register API call    
@step(r'"([^"]*)" is called on each node in "([^"]*)"')
def api_method_is_called(step,apiCall,machine):
    logger.info('%s is called on each node in %s',apiCall,machine)
    
    config['machine'] = machine 
    config['apiCall'] = apiCall
    config['nodeId'] = []
    responses[apiCall][machine] = {}

    for i in world.machines[machine]:
        logger.info('Node: %s',i)
        config['nodeId'].append(i)
        logger.info(config['nodeId'])
        
     
        api = tests.prepare_api_call(i,machine)
        
        callList = {
            'getNodeInfo': api.get_node_info,
            'getNeighbors': api.get_neighbors,
            'getTips': api.get_tips,
            'getTransactionsToApprove': api.get_transactions_to_approve
        }
    
        if apiCall == 'getTransactionsToApprove':
            response = callList.get(apiCall)(3)
        else: 
            response = callList.get(apiCall,"Invalid API Call")()
    
        logger.info('API call sent')
        logger.debug('Error with response')
        assert type(response) is dict, response
    
       
        responses[apiCall][machine][i] = response
        logger.info('Response Stored')


###
#Response testing    
@step(r'a response with the following is returned:')
def compare_response(step):
    logger.info('Validating response')
    keys = step.hashes
    nodeId = config['nodeId']
    apiCall = config['apiCall']
    machine = config['machine']    
    ###
    logger.info('apiCall %s',apiCall)
    if apiCall == 'getNodeInfo' or apiCall == 'getTransactionsToApprove':
        response_list = responses[apiCall][machine]
        for i in response_list:
            response = responses[apiCall][machine][i]
            responseKeys = list(response.keys())
            responseKeys.sort()
            logger.debug('Response Keys: %s', responseKeys)
            for x in range(len(response)):
                assert str(responseKeys[x]) == str(keys[x]['keys']), "There was an error with the response" 
    
    elif apiCall == 'getNeighbors' or apiCall == 'getTips':
        response_list = responses[apiCall][machine]
        for i in response_list:
            response = responses[apiCall][machine][i] 
            responseKeys = list(response.keys())
            logger.debug('Response Keys: %s', responseKeys)

            for x in range(len(response)):
                try:
                    for y in range(len(response[x])):
                        assert str(responseKeys[y]) == str(keys[y])
                except:
                    logger.debug("No values to verify response with")        
 
    logger.info('Response Validated')

 ###
 #Test GetTrytes 

@step(r'getTrytes is called with the hash static_vals.TEST_HASH')
def call_getTrytes(step):
    logger.info('Testing getTrytes on static transaction')
    machine = config['machine']
    nodeIds = config['nodeId']
    responses['getTrytes'][machine] = {}
    
    logging.info('Machine: %s',machine)  
    
    for node in nodeIds:
        api = tests.prepare_api_call(node,machine)
        response = api.get_trytes(testHash)
        logger.debug("Call may not have responded correctly: \n%s",response)
        assert type(response) is dict 
        responses['getTrytes'][machine][node] = response


@step(r'the response should be equal to static_vals.TEST_TRYTES')
def check_trytes(step):
    logger.info('Validating response')
    machine = config['machine']
    nodeId = config['nodeId']  
    
    for node in nodeId: 
        response = responses['getTrytes'][machine][node]
        if 'trytes' in response:
            logger.debug("Response: \n%s",response['trytes'][0])
            assert response['trytes'][0] == testTrytes, "Response doesn't match: \n{}".format(response['trytes'][0])
        
            logger.info('Response Validated')


###
#Test Add and Remove Neighbors
  
@step(r'2 neighbors are added with "([^"]*)" on each node in "([^"]*)"')
def add_neighbors(step,apiCall,machine):
    logger.info('Adding neighbors')
    config['nodeId'] = world.machines[machine]
    for node in config['nodeId']:
        api = tests.prepare_api_call(node,machine)
        response = api.add_neighbors(neighbors)
        logger.debug('Response: %s',response)
    
@step(r'"getNeighbors" is called, it should return the following neighbor addresses:')
def check_neighbors_post_addition(step):
    logger.info('Ensuring Neighbors were added correctly')
    
    for node in config['nodeId']:
        containsNeighbor = tests.check_neighbors(step,node)
        assert containsNeighbor[1] is True
        assert containsNeighbor[0] is True 
    
    
@step(r'"removeNeighbors" will be called to remove the same neighbors')
def remove_neighbors(step):
    logger.info('Removing neighbors')
    
    for node in config['nodeId']:
        api = tests.prepare_api_call(node,config['machine'])
        response = api.remove_neighbors(neighbors)
        logger.debug('Response: %s',response)
    
@step(r'"getNeighbors" should not return the following neighbor addresses:')
def check_neighbors_post_removal(step):
    logger.info('Ensuring Neighbors were removed correctly')
    for node in config['nodeId']:
        containsNeighbor = tests.check_neighbors(step,node)
        assert containsNeighbor[1] is False
        assert containsNeighbor[0] is False
 
    
    
      
  
  
                                
                    

    