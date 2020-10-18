from bs4 import BeautifulSoup
import re
import logging

logging.getLogger(__name__)

#############################################################
# state = 0- Agent not logged In                            #
# state = 1 Agent logged In                                 #
# state = 2 Agent logged In post forced logout              #
##############################################################

class jshtml(object):

    def __init__(self):
        self.userstate=0
        self.pagesource=""
        self.reasoncode = 'other'
        self.msg = 'You have been signed out and will be redirected to the sign-in page'
        self.NameofAgent = "NotFetched"

    def _get_agent(self):
        return self.NameofAgent

    def _set_agent(self,value):
        self.NameofAgent = value

    def parse_html(self,htmlstring):
        #https://stackoverflow.com/questions/51777725/how-to-get-javascript-variables-from-a-script-tag-using-python-and-beautifulsoup
        try:
            text=""
            ex_script=[]
            self.soup = BeautifulSoup(htmlstring, 'html.parser')
            #print(self.soup)
            for script in self.soup(["script","style"]):
                ex_script =script.extract()
            #print(ex_script)
            temptext =self.soup.get_text()
            text = self._check_logout(ex_script)
            if text:
                return text
            else:
                linetext = self._check_other_options(temptext)
                return linetext
        except Exception as e:
            logging.debug("failed parsing source page %s" %e)

    def _check_logout(self,ex_script):
        try:
            causecode=0
            logout=0
            for i in ex_script:
                if "logoutReason" in i:
                    m =re.findall(r'logoutReason\s*(.*)',i)
                    for j in m:
                        if self.reasoncode in j.strip('.;= '):
                            causecode = 2
                if "logoutMsg" in i:
                        n =re.findall(r'logoutMsg\s*(.*)',i)
                        for k in n:
                            if self.msg in k.strip('.;= '):
                                logout = 2
                else:
                    pass
            if logout==2 and causecode==2:
                text = "FORCEDLOGOUT"
                self.userstate=2
                logging.info("the text returned is : %s" % text)
            else:
                text=None
            return text
        except Exception as e:
            logging.debug("failed analysing error page %s" %e)

    def _check_other_options(self,temptext):
        try:
            lines = (line.strip() for line in temptext.splitlines())
            #break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            #drop blank lines
            checktext = '\n'.join(chunk for chunk in chunks if chunk)
            #print(checktext)
            text = self._get_error(checktext)
            logging.debug("the text returned is : %s" % text)
            return text

        except Exception as e:
            logging.debug("failed analysing error page %s" %e)

    def _get_error(self,text):
        try:
            logging.debug("detecting  complete text %s:" %text)
            #print("trying to read text %s" %text)
            for i in text.splitlines():
                #Connectivity errors
                if "ERR_INTERNET_DISCONNECTED" in i:
                    #print("cannot load finesse webpage %s" % "ERR_INTERNET_DISCONNECTED")
                    return "ERR_INTERNET_DISCONNECTED"

                elif "ERR_CONNECTION_ABORTED" in i:
                    #print("cannot load finesse webpage %s" % "ERR_CONNECTION_ABORTED")
                    return "ERR_CONNECTION_ABORTED"

                elif "ERR_NAME_NOT_RESOLVED" in i:
                    #print("cannot load finesse webpage %s" % "ERR_NAME_NOT_RESOLVED")
                    return "ERR_NAME_NOT_RESOLVED"

                elif "INET_E_RESOURCE_NOT_FOUND" in i:
                    return "PAGENOTLOADED"

                elif "Can’t connect securely to this page" in i:
                    return "PAGENOTLOADED"

                #login detection section
                elif "Sign in to Cisco Finesse" in i and self.userstate==0:
                    #print("First time login page detected %s" % "Sign in to Cisco Finesse")
                    return "NEWLOGINPAGE"

                elif "Sign in to Cisco Finesse" in i and self.userstate==1:
                    #need to get manual logout state
                    #print("Refresh login page detected %s" % "Sign in to Cisco Finesse")
                    return "REFRESHLOGINPAGE"

                elif "Sign in to Cisco Finesse" in i and self.userstate==2:
                    #print("Failed Login to Finesse detected... trying again")
                    #print("loop")
                    return "LOOPLOGINPAGE"

                #Post Logged IN section
                elif re.search("^Agent.*(.*).*Extension", i):
                    #need to get loggedin state
                    logging.debug("detected logged in state from text %s" %i)
                    if self.userstate==0:
                        #print("Agent logged In successfully")
                        self.userstate=1
                        match = re.search("^Agent\W+([^(]*)",i).group(1)
                        self._set_agent(match)
                        return "LOGGEDIN"
                    #print("Agent is already Logged In")
                    if self.userstate==2:
                        self.userstate=1
                        #print("after forcelogin")
                        match = re.search("^Agent\W+([^(]*)",i).group(1)
                        self._set_agent(match)
                        return "AFTERFORCED"
                    else:
                        self.userstate=1
                        return "ALREADYLOGGEDIN"
                elif re.search(".*dial.*number.*is.*invalid.OK",i):
                    #invoked to click on OK when dial number invalid error only
                    #at forced logout
                    if self.userstate==2:
                        return "LOGINATTEMPTFAILED"
                else:
                    pass

        except Exception as e:
            logging.debug("failed analysing error page %s" %e)
