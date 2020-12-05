import http.client

application_id = '2f43e567-2772-41f5-9024-481a4123d812'
member_id = 'b1f36595-681e-408c-8776-99c5fdc6bf4d'
owner_id = '077313fc-5a35-4e4c-8a92-f79ed09bac37'
serviceName="keyrockIDM"
servicePort=3005
adminTokenHeaderName='Xtoken'
headers = {}

def createUser__request(userInfo, token):
	# REQUEST BODY
	payload = "{\n  \"user\": {" \
		"\n    \"username\": \" " + userInfo.userName + " \"," \
		"\n    \"email\": \"" + userInfo.email + "\"," \
		"\n    \"password\": \"" + userInfo.password + "\"," \
		"\n    \"enabled\": false\n  }\n}"
	# ADD HEADERS
	headers['X-Auth-Token'] = token
	headers['Content-Type'] = 'application/json'
	# REQUEST ENDPOINT
	endpoint = "/v1/users"
	# CREATE CONNECTION
	conn = http.client.HTTPConnection(serviceName, servicePort)
	# SENT REQUEST
	conn.request("POST", endpoint,  payload, headers)
	return conn.getresponse()


def deleteUser__request(userInfo, token):
	print('delete')
	# REQUEST BODY
	payload = ''
	# ADD HEADERS
	headers['X-Auth-Token'] = token
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
	headers['X-Auth-Token'] = token
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
	headers['X-Auth-Token'] = token
	headers['Content-Type'] = 'application/json'
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
	headers['X-Auth-Token'] = token
	headers['Content-Type'] = 'application/json'
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
	headers['Authorization'] = bearer
	# REQUEST ENDPOINT
	endpoint = "/user/"
	# CREATE CONNECTION
	conn = http.client.HTTPConnection(serviceName, servicePort)
	# SENT REQUEST
	conn.request("GET", endpoint, payload, headers)

	return conn.getresponse()















