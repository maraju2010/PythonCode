import requests
from requests.auth import HTTPBasicAuth

class finesseapi(object):

    def __init__(self):
        pass

    def GET(self,url, username, password):
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
        print ("Executing GET '%s'" % url)
        try:
            response = requests.get(url=url, auth=HTTPBasicAuth(username, password))            
            return(response.text)
        except:
            print ("An error occured in the GET request to %s" % url)
