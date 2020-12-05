import http.client

application_id = '309984b0-3222-4da8-8208-c41846483079'
member_id = '5fc82c72-664f-49c7-9db1-4197ff187951'
owner_id = '279b54bc-74bb-44df-9e8c-dabbb7b4816a'
serviceName="keyrockIDM"
servicePort=3005
adminTokenHeaderName='Xtoken'

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
	conn = http.client.HTTPConnection(serviceName, servicePort)
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
	conn = http.client.HTTPConnection(serviceName, servicePort)
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
	conn = http.client.HTTPConnection(serviceName, servicePort)
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
	conn = http.client.HTTPConnection(serviceName, servicePort)
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
	conn = http.client.HTTPConnection(serviceName, servicePort)
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
	conn = http.client.HTTPConnection(serviceName, servicePort)
	# SENT REQUEST
	conn.request("GET", endpoint, payload, headers)
	return conn.getresponse()















