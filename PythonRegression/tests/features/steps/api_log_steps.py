from aloe import step
from tests.features.steps import api_test_steps
import os 

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


logConfig = {}

@step(r'a response for "([^"]*)" exists')
def api_exists(step,apiCall):
    logger.info('Confirming response exists')
    logConfig['apiCall'] = apiCall
    exists = api_test_steps.check_responses_for_call(apiCall)
    logger.debug('Response for %s does not exist',apiCall)
    assert exists is True
    logger.info('Response exists')
 
@step(r'create the log directory "([^"]*)"')
def create_log_directory(step,path):
    logger.info('Creating Log directory %s',path)
    logConfig['logDirPath'] = path
    try:
        os.makedirs(path)
        logger.info('Log directory created')
    except:
        logger.info('%s already exists',path)
       
        
@step(r'log the response to the file "([^"]*)"')
def create_log_file(step,fileName):
    logging.info('Attempting to log response in %s',fileName)
    config = setup_logs(fileName)
    file = config[1]
    response = config[0]
        
    for i in response:
        nodeName = i
        responseVals = ""   
        for x in response[i]:
            responseVals += "\t" + x + ": " + str(response[i][x]) + "\n"
        statement = nodeName + ":\n" + responseVals
        logging.debug('Statement to write: %s',statement)
        file.write(statement)
                
    logging.info('Response logged')
    file.close()
    
      
@step(r'log the neighbor response to the file "([^"]*)"')
def create_neighbor_log_file(step,fileName):
    logging.info('Attempting to log response in %s',fileName)
    config = setup_logs(fileName)
    file = config[1]
    response = config[0]
    
    for i in response:
        nodeName = i
        for x in response[i]:
            if type(response[i][x]) != int:
                responseVals = ""
                for y in range(len(response[i][x])):
                    for a in response[i][x][y]: 
                        responseVals += "\t" + a + ": " + str(response[i][x][y][a]) + "\n"
                    responseVals += "\n"
                    
        statement = nodeName + ":\n" + responseVals + "\n\n"
        logging.debug('Statement to write: %s',statement)
        file.write(statement)
    
    logging.info('Response logged')
    file.close()
    

@step(r'log the tips response to the file "([^"]*)"')
def create_tips_log_file(step,fileName):
    logging.info('Attempting to log response in %s',fileName)
    config = setup_logs(fileName)
    file = config[1]
    response = config[0]
        
    for i in response:
        nodeName = i
        responseVals = ""   
        for x in response[i]:
            responseVals += "\n\t" + x + ": " 
            if type(response[i][x]) != int:
                    #Maximum 250 entries for the log
                    responseVals += "\n"
                    if len(response[i][x]) > 250:
                        max = 250
                    else: 
                        max = len(response[i][x])
                    
                    for y in range(max):
                        responseVals += "\t\tTip: " + str(response[i][x][y]) + "\n"
                       
            else: 
                responseVals += str(response[i][x])
        statement = nodeName + ":\n" + responseVals
        logging.debug('Statement to write: %s',statement)        
        file.write(statement)        
    
    logging.info('Response logged')
    file.close()
    







def setup_logs(fileName):
    logging.info('Setting up log file')
    path = logConfig['logDirPath'] + fileName
    file = open(path,'w')
    logging.debug('File path: %s',path)
   
    apiCall = logConfig['apiCall'] 
    logging.info('Fetching %s response', apiCall)
    response = api_test_steps.fetch_response(apiCall)
    logging.debug('API Response: %s', response)
    config = [response,file]
    
    logging.info('Log file and response set up')
    return config

