@machine1 @static
Feature: Test API calls on Machine 1
	Test various api calls to make sure they are responding
	correctly 
	
	@nodeInfo
	Scenario: GetNodeInfo is called
		Given "getNodeInfo" is called on "nodeA" 
		Then a response with the following is returned:
		|keys								|
		|appName							|	
		|appVersion							|
		|duration							|
		|jreAvailableProcessors				|
		|jreFreeMemory						|
		|jreMaxMemory						|
		|jreTotalMemory						|
		|jreVersion							|		
		|latestMilestone					|
		|latestMilestoneIndex				|
		|latestSolidSubtangleMilestone		|
		|latestSolidSubtangleMilestoneIndex |
		|milestoneStartIndex				|
		|neighbors							|
		|packetsQueueSize					|
		|time								|
		|tips								|
		|transactionsToRequest				|
	
	@nodeInfo	
	Scenario: Log GetNodeInfo
		Given a response for "getNodeInfo" exists
		Then create the log directory "./tests/features/machine1/static_test_logs/get_node_info_logs/"
		And log the response to the file "getNodeInfoLog.txt"		 
		
	@neighbors
	Scenario: GetNeighbors is called
		Given "getNeighbors" is called on "nodeA"
		Then a response with the following is returned:
		|keys							|
		|address						|
		|numberOfAllTransactions		|
		|numberOfAllTransactionRequests	|
		|numberOfNewTransactions		|
		|numberOfInvalidTransactions	|
		|numberOfSentTransactions		|
		|connectionType					|
		
	@neighbors
	Scenario: Log GetNeighbors
		Given a response for "getNeighbors" exists
		Then create the log directory "./tests/features/machine1/static_test_logs/get_neighbors_logs/"
		And log the neighbor response to the file "getNeighborsLog.txt"		 
		
	@getTips	
	Scenario: GetTips is called
		Given "getTips" is called on "nodeA"
		Then a response with the following is returned:
		|keys 		|
		|hashes		|
		|duration	|
	@getTips 	
	Scenario: Log GetTips
		Given a response for "getTips" exists
		Then create the log directory "./tests/features/machine1/static_test_logs/get_tips_logs/"
		And log the tips response to the file "getTipsLog.txt"

	@getTrytes
	Scenario: GetTrytes is called 
		Given getTrytes is called with the hash static_vals.TEST_HASH
		Then the response should be equal to static_vals.TEST_TRYTES
	
	
	@transactionsToApprove	
	Scenario: GetTransactionsToApprove is called
<<<<<<< HEAD
<<<<<<< HEAD:PythonRegression/tests/features/machine1/m1_1_static_api_tests.feature
<<<<<<< HEAD
=======
>>>>>>> parent of 33a099b... Added Transaction Broadcast Tests
		Given "getTransactionsToApprove" is called on "nodeA"
		Then a response with the following is returned: 
		|keys				|
		|trunkTransaction	|
		|branchTransaction	|
		|duration			|
		
	@neighbors
	Scenario: Add and remove Neighbors
		Given 2 neighbors are added with "addNeighbors" on "nodeA"
		When "getNeighbors" is called, it should return the following neighbors:
			|neighbors 				|
			|178.128.236.6:14600 	|
			|167.99.178.3:14600		|
		Then "removeNeighbors" will be called to remove the same neighbors 
		And "getNeighbors" should not return the following neighbors:
			|neighbors 				|
			|178.128.236.6:14600 	|
			|167.99.178.3:14600		|		
<<<<<<< HEAD
=======
=======
>>>>>>> c0bd5fb... Merge remote-tracking branch 'upstream/glue' into glue:PythonRegression/tests/features/machine1/m1_1_static_api_tests.feature
		Given "getTransactionsToApprove" is called on each node in "machine1"
		Then a response with the following is returned: 
		|keys								|
		|trunkTransaction					|
		|branchTransaction					|
		|duration							|
		
	@neighbors
	Scenario: Add and remove Neighbors
		Given 2 neighbors are added with "addNeighbors" on each node in "machine1"
		When "getNeighbors" is called, it should return the following neighbor addresses:
		|neighbors 							|
		|178.128.236.6:14600 				|
		|167.99.178.3:14600					|
		Then "removeNeighbors" will be called to remove the same neighbors 
		And "getNeighbors" should not return the following neighbor addresses:
		|neighbors 							|
		|178.128.236.6:14600 				|
		|167.99.178.3:14600					|	
		
	@transactionDemo
	Scenario: Broadcast a test transacion
		Send a test transaction from one node in a machine, and find that transaction
		through a different node in the same machine

		Given "nodeA" and "nodeB" in "machine1" are neighbors
		When a transaction with the tag "TEST9TRANSACTION" is sent from "nodeA"
		And findTransaction is called with the same tag on "nodeB" 
		Then the transaction should be found 
		
		
<<<<<<< HEAD:PythonRegression/tests/features/machine1/m1_1_static_api_tests.feature
>>>>>>> 31a50a9... Added Transaction Broadcast Tests
=======
>>>>>>> c0bd5fb... Merge remote-tracking branch 'upstream/glue' into glue:PythonRegression/tests/features/machine1/m1_1_static_api_tests.feature
=======
>>>>>>> parent of 33a099b... Added Transaction Broadcast Tests
		