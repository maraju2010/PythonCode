import requests
from requests.auth import HTTPBasicAuth
#Removes request warnings from console
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class FinesseApi(object):

    def __init__(self,pub,username,password,SSL=False):
        self.PRIMARY_FINESSE_SERVER = pub
        self.SCHEME = "https"
        #self.username = "username"
        #self.password = "aaaaa"
        self.username = username
        self.password = password
        self.SSL = SSL

    def GET(self,url, username, password,params=''):
        """
            Call the GET HTTP Request using HTTP Basic Auth authentication

            Parameters:
                url (str): The URL to make the REST request
                username (str): The username of the user making the HTTP request
                password (str): The password of the user making the HTTP request
                params(dictionary, optional): Dictionary or bytes to be sent in the query string for the Request.
                                          (e.g. {"category" : "NOT_READY"})

                Returns: Response object (http://docs.python-requests.org/en/master/api/#requests.Response) - The HTTP Response as a result of the HTTP Request
                """
        print ("##### Executing GET '%s' ##### \n" % url)
        try:
            response = requests.get(url=url, auth=HTTPBasicAuth(username, password),params=params, verify=False)
            #print(response.content)
            return response
        except Exception as e:
            response = " ##### An exception-5XX occured in the GET request to %s -- %s #####" % (url,e)
            return response


    def PUT(self,url, username, password, data='',params=''):
        """
            Call the PUT HTTP Request using HTTP Basic Auth authentication

            Parameters:
                url (str): The URL to make the REST request
                username (str): The username of the user making the HTTP request
                password (str): The password of the user making the HTTP request
                params(dictionary, optional): Dictionary or bytes to be sent in the query string for the Request.
                                          (e.g. {"category" : "NOT_READY"})
                                          data(str, optional): The HTTP request body as a string

                Returns: Response object (http://docs.python-requests.org/en/master/api/#requests.Response) - The HTTP Response as a result of the HTTP Request
        """
        print ("###### Executing PUT '%s' ###### \n" % url)
        try:
            headers = {'Content-Type': 'application/xml'}
            #print ("PUT() data: %s\n" % data)
            response = requests.put(url=url, auth=HTTPBasicAuth(username, password), headers=headers, params=params, data=data, verify=False)
            return(response)
        except Exception as e:
            response = " ##### An exception-5XX occured in the GET request to %s -- %s #####" % (url,e)
            return response
