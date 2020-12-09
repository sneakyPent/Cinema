import http.client
import json

application_id = 'e78aa12c-3722-4149-9ba2-a71669fb8e00'
member_id = '899e96ab-a5a6-4b24-8111-1d823c12e563'
owner_id = '16f381c9-7e90-41c8-9537-1b03222a12bc'
keyrockServiceName= "keyrockIDM"
keyrockServicePort=3005
orionServiceName= "orion-pep-proxy-wilma"
orionServicePort=1027
adminTokenHeaderName='Xtoken'

# ##################################################### KEYROCK REQUESTS #####################################################
def createUser__request(userInfo, token):
	# REQUEST BODY
	payload = "{\n  \"user\": {" \
		"\n    \"username\": \" " + userInfo.userName + " \"," \
		"\n    \"email\": \"" + userInfo.email + "\"," \
		"\n    \"password\": \"" + userInfo.password + "\"," \
		"\n    \"enabled\": false\n  }\n}"
	# ADD HEADERS
	headers = {'X-Auth-Token': token, 'Content-Type': 'application/json'}
	# REQUEST ENDPOINT
	endpoint = "/v1/users"
	# CREATE CONNECTION
	conn = http.client.HTTPConnection(keyrockServiceName, keyrockServicePort)
	# SENT REQUEST
	conn.request("POST", endpoint,  payload, headers)
	return conn.getresponse()


def deleteUser__request(userInfo, token):
	# REQUEST BODY
	payload = ''
	# ADD HEADERS
	headers = {'X-Auth-Token': token}
	# REQUEST ENDPOINT
	endpoint = "/v1/users/" + userInfo.userId
	# CREATE CONNECTION
	conn = http.client.HTTPConnection(keyrockServiceName, keyrockServicePort)
	# SENT REQUEST
	conn.request("DELETE", endpoint, payload, headers)
	return conn.getresponse()


def getUserRoles__request(userInfo, token):
	# REQUEST BODY
	payload = ''
	# ADD HEADERS
	headers = {'X-Auth-Token': token}
	# REQUEST ENDPOINT
	endpoint = "/v1/applications/" + application_id + "/users/" + userInfo.userId + "/roles"
	# CREATE CONNECTION
	conn = http.client.HTTPConnection(keyrockServiceName, keyrockServicePort)
	# SENT REQUEST
	conn.request("GET", endpoint, payload, headers)
	return conn.getresponse()


def assignRole__request(userInfo, token):
	# REQUEST BODY
	payload = "{}"
	# ADD HEADERS
	headers = {'X-Auth-Token': token, 'Content-Type': 'application/json'}
	# REQUEST ENDPOINT
	endpoint = ""
	if userInfo.role == 'member':
		endpoint = "/v1/applications/" + application_id + "/users/" + userInfo.userId + "/roles/" + member_id
	elif userInfo.role == 'owner':
		endpoint = "/v1/applications/" + application_id + "/users/" + userInfo.userId + "/roles/" + owner_id
	# CREATE CONNECTION
	conn = http.client.HTTPConnection(keyrockServiceName, keyrockServicePort)
	# SENT REQUEST
	conn.request("POST",endpoint, payload, headers)
	return conn.getresponse()


def deleteRole__request(userInfo, token):
	# REQUEST BODY
	payload = "{}"
	# ADD HEADERS
	headers = {'X-Auth-Token': token, 'Content-Type': 'application/json'}
	# REQUEST ENDPOINT
	endpoint = ""
	if userInfo.role == 'member':
		endpoint = "/v1/applications/" + application_id + "/users/" + userInfo.userId + "/roles/" + member_id
	elif userInfo.role == 'owner':
		endpoint = "/v1/applications/" + application_id + "/users/" + userInfo.userId + "/roles/" + owner_id
	# CREATE CONNECTION
	conn = http.client.HTTPConnection(keyrockServiceName, keyrockServicePort)
	# SENT REQUEST
	conn.request("DELETE",endpoint, payload, headers)
	return conn.getresponse()

def getOwnInfo__request(bearer):
	# REQUEST BODY
	payload = ''
	# ADD HEADERS
	headers = {'Authorization': bearer}
	# REQUEST ENDPOINT
	endpoint = "/user/"
	# CREATE CONNECTION
	conn = http.client.HTTPConnection(keyrockServiceName, keyrockServicePort)
	# SENT REQUEST
	conn.request("GET", endpoint, payload, headers)
	return conn.getresponse()

# ##################################################### ORION REQUESTS #####################################################

def createEntity__request(entity, bearer):
	# REQUEST BODY
	payload = json.dumps(entity)
	# ADD HEADERS
	headers = {'Authorization': bearer, 'Content-Type': 'application/json'}
	# REQUEST ENDPOINT
	endpoint = "/v2/entities"
	# CREATE CONNECTION
	conn = http.client.HTTPConnection(orionServiceName, orionServicePort)
	# SENT REQUEST
	conn.request("POST", endpoint, payload, headers)
	return conn.getresponse()

def updateEntity__request(entity_id, attributes, bearer):
	# REQUEST BODY
	payload = json.dumps(attributes)
	# ADD HEADERS
	headers = {'Authorization': bearer, 'Content-Type': 'application/json'}
	# REQUEST ENDPOINT
	endpoint = "/v2/entities/" + entity_id + "/attrs"
	# CREATE CONNECTION
	conn = http.client.HTTPConnection(orionServiceName, orionServicePort)
	# SENT REQUEST
	conn.request("PATCH", endpoint, payload, headers)
	return conn.getresponse()

def deleteEntity__request(entity_id, token):
	# REQUEST BODY
	payload = ''
	# ADD HEADERS
	headers = {'Authorization': token}
	# REQUEST ENDPOINT
	endpoint = "/v2/entities/" + entity_id
	# CREATE CONNECTION
	conn = http.client.HTTPConnection(orionServiceName, orionServicePort)
	# SENT REQUEST
	conn.request("DELETE",endpoint, payload, headers)
	return conn.getresponse()


def createSubscription__request(subscription, bearer):
	# REQUEST BODY
	payload = json.dumps(subscription)
	# ADD HEADERS
	headers = {'Authorization': bearer, 'Content-Type': 'application/json'}
	# REQUEST ENDPOINT
	endpoint = "/v2/subscriptions"
	# CREATE CONNECTION
	conn = http.client.HTTPConnection(orionServiceName, orionServicePort)
	# SENT REQUEST
	conn.request("POST", endpoint, payload, headers)
	return conn.getresponse()


def deleteSubscription__request(subscription_id, token):
	# REQUEST BODY
	payload = ''
	# ADD HEADERS
	headers = {'Authorization': token}
	# REQUEST ENDPOINT
	endpoint = "/v2/subscriptions/" + subscription_id
	# CREATE CONNECTION
	conn = http.client.HTTPConnection(orionServiceName, orionServicePort)
	# SENT REQUEST
	conn.request("DELETE",endpoint, payload, headers)
	return conn.getresponse()









