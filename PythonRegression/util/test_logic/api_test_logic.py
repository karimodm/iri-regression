from aloe import world
from iota import Iota
from tests.features.steps import api_test_steps 

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

steps = api_test_steps

def prepare_api_call(nodeName,machine):
    logger.info('Preparing api call')
    host = world.machines[machine][nodeName]
    address ="http://"+ host + ":14265"
    api = Iota(address)
    logger.info('API call prepared for %s',address)
    return api


def check_responses_for_call(apiCall):
    if len(steps.responses[apiCall][steps.config['machine']]) > 0:
        return True
    else:
        return False
    
def fetch_response(apiCall):
    return steps.responses[apiCall][steps.config['machine']]


def check_neighbors(step,node):
    api = prepare_api_call(node,steps.config['machine'])
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
     