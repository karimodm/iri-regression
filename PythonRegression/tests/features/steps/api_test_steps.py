<<<<<<< HEAD
from aloe import step,world,before
from iota import *
from util import static_vals
<<<<<<< HEAD
=======
from util.test_logic import api_test_logic
from yaml import load, Loader
from time import sleep

import logging 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
>>>>>>> 31a50a9... Added Transaction Broadcast Tests
=======
from aloe import *
from iota import Iota
from iota.commands.core import add_neighbors
from util import static_vals
>>>>>>> parent of 33a099b... Added Transaction Broadcast Tests

<<<<<<< HEAD
neighbors = static_vals.TEST_NEIGHBORS
testHash = static_vals.TEST_HASH
testTrytes = static_vals.TEST_TRYTES
<<<<<<< HEAD
testAddress = static_vals.TEST_ADDRESS
<<<<<<< HEAD
=======
=======
static = static_vals

neighbors = static.TEST_NEIGHBORS
testHash = static.TEST_HASH
testTrytes = static.TEST_TRYTES
testAddress = static.TEST_ADDRESS
>>>>>>> 3b816d6... Tests now run from ciglue correctly

tests = api_test_logic
>>>>>>> c0bd5fb... Merge remote-tracking branch 'upstream/glue' into glue
=======
>>>>>>> parent of 33a099b... Added Transaction Broadcast Tests

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
=======
    config['nodeId'] = []
    responses[apiCall][machine] = {}
    
    for i in world.machines[machine]:
        logger.info('Node: %s',i)
        config['nodeId'].append(i)        
<<<<<<< HEAD
>>>>>>> 31a50a9... Added Transaction Broadcast Tests
=======
>>>>>>> c0bd5fb... Merge remote-tracking branch 'upstream/glue' into glue
=======
>>>>>>> parent of 33a099b... Added Transaction Broadcast Tests
     
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
    apiCall = config['apiCall']
    
    if apiCall == 'getNodeInfo' or apiCall == 'getTransactionsToApprove':
        response = responses['getNodeInfo'][nodeId]
        responseKeys = list(response.keys())
        responseKeys.sort()
        for i in range(len(response)):
            assert str(responseKeys[i]) == str(keys[i]['keys']), "There was an error with the response" 
<<<<<<< HEAD
=======
    machine = config['machine']    
    ###
    if apiCall == 'getNodeInfo' or apiCall == 'getTransactionsToApprove':
        response_list = responses[apiCall][machine]
        for i in response_list:
            response = responses[apiCall][machine][i]
            responseKeys = list(response.keys())
            responseKeys.sort()
        
            keyList = []
            for y in range(len(keys)):
                keyList.append(keys[y]['keys'])
        
            keyList.sort()
            
            for x in range(len(response)):
                assert str(responseKeys[x]) == str(keyList[x]), "There was an error with the response" 
<<<<<<< HEAD
>>>>>>> 31a50a9... Added Transaction Broadcast Tests
=======
>>>>>>> c0bd5fb... Merge remote-tracking branch 'upstream/glue' into glue
=======
>>>>>>> parent of 33a099b... Added Transaction Broadcast Tests
    
    elif apiCall == 'getNeighbors' or apiCall == 'getTips':
        response = responses['getNeighbors'][nodeId] 
        responseKeys = list(response.keys())
        for x in range(len(response)):
            try:
                for i in range(len(response[x])):
                    assert str(responseKeys[i]) == str(keys[i])
            except:
                print("No neighbors to verify response with")        
 
<<<<<<< HEAD
 ###
 #Test GetTrytes 
=======
    logger.info('Response Validated')
    
###
#Test GetTrytes 
>>>>>>> 3b816d6... Tests now run from ciglue correctly

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
def add_neighbors_to_nodes(step,apiCall,machine):
    logger.info('Adding neighbors')
    config['nodeId'] = world.machines[machine]
    for node in config['nodeId']:
        api = tests.prepare_api_call(node,machine)
        logger.info("Neighbors: %s",neighbors)
        response = api.add_neighbors(neighbors)
        logger.debug('Addition response: %s',response)
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 7c3e68d... Integrated ci glue code with test configuration
=======
>>>>>>> 7c3e68d... Integrated ci glue code with test configuration
=======
>>>>>>> c0bd5fb... Merge remote-tracking branch 'upstream/glue' into glue
    
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
<<<<<<< HEAD
>>>>>>> 7c3e68d... Integrated ci glue code with test configuration
=======
>>>>>>> 7c3e68d... Integrated ci glue code with test configuration
=======
>>>>>>> c0bd5fb... Merge remote-tracking branch 'upstream/glue' into glue
    
@step(r'"getNeighbors" should not return the following neighbors:')
def check_neighbors_post_removal(step):
    containsNeighbor = check_neighbors(step)
    assert containsNeighbor[1] is False
    assert containsNeighbor[0] is False
            
 
    
    
<<<<<<< HEAD
    api1 = tests.prepare_api_call(node1,machine)
    api2 = tests.prepare_api_call(node2,machine)
        
    response1 = api1.get_neighbors()
    response2 = api2.get_neighbors()
    neighbors1 = list(response1['neighbors'])
    neighbors2 = list(response2['neighbors'])
    address1 = "udp://" + str(hosts[0]) + ":" + ports[0]     
    address2 = "udp://" + str(hosts[1]) + ":" + ports[1] 
    
    logger.info("Checking if nodes are paired")
    
    containsNeighbor = False
    for neighbor in range(len(neighbors1)):
        if neighbors1[neighbor]['address']:
            containsNeighbor = True
            logger.info("Neighbor found")

    
    if containsNeighbor == False:
        api1.add_neighbors([address2])
        api2.add_neighbors([address1])
        logger.info("Nodes paired")
    
        
    containsNeighbor = False
    for neighbor in range(len(neighbors2)):
        if neighbors2[neighbor]['address']:
            containsNeighbor = True 
            logger.info("Neighbor found")

    if containsNeighbor == False:
        api2.add_neighbors([address1])
        api1.add_neighbors([address2]) 
        logger.info("Nodes paired")
        
        
    response = api1.get_neighbors()
    logger.info(response)
    response = api2.get_neighbors()
    logger.info(response)
        
     
@step(r'a transaction with the tag "([^"]*)" is sent from "([^"]*)"')
def send_transaction(step,tag,nodeName):
    logger.info('Preparing Transaction...')
    logger.info('Node: %s',nodeName)
    machine = config['machine']
    config['tag'] = tag
    api = tests.prepare_api_call(nodeName,machine)  
    txn = \
        ProposedTransaction(
            address = 
            Address(testAddress),
            
            message = TryteString.from_unicode('Test Transaction propagation'),
            tag = Tag(tag),
            value = 0,
            )
    
    logger.info("Sending Transaction...")
    api.send_transfer(depth=3, transfers=[txn])
    logger.info("Giving the transaction time to propagate...")
    sleep(10)
   
   
@step(r'findTransaction is called with the same tag on "([^"]*)"')
def find_transaction_is_called(step,nodeName):
    logger.info(nodeName)
    api = tests.prepare_api_call(nodeName, config['machine']) 
    logger.info("Searching for Transaction")
    response = api.find_transactions(tags=[config['tag']])    
    config['findTransactionResponse'] = response
    
@step(r'the Transaction should be found')
def check_transaction_response(step):
    logger.info("Checking response...")
    response = config['findTransactionResponse']
    assert len(response['hashes']) != 0, 'Transaction not found'
    logger.info("Response found")  

  
    
    
                                  
=======
      
  
  
                                
>>>>>>> parent of 33a099b... Added Transaction Broadcast Tests
                    
    
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
     
    