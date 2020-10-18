import prop
import datetime

causedict = {
1:"unallocated Number",
2:"No Route To Network",
3:"No Route To Destination",
16:"Normal Clearing",
17:"User Busy",
18:"No User Responding",
19:"No Answer From the User",
20:"Subscriber Absent",
21:"Call Rejected",
22:"Number Changed",
23:"Redirection to New Destination",
26:"Nonselected User Clearing or Misrouted Ported Number",
27:"Destination Out of Order",
28:"Address Incomplete",
29:"Facility Rejected",
31:"Normal Unspecified",
34:"No Circuit Available",
38:"Network Out of Order",
41:"Temporary Failure",
42:"Switching Equipment Congestion",
44:"Requested Circuit Not Available",
47:"Resource Unavailable",
55:"Incoming Calls Barred with CUG",
57:"Bearer Capability Not Authorized",
58:"Bearer Capability Not Presently Available",
63:"Service/Option Not Available",
65:"Bearer Capability Not Implemented",
69:"Requested Facility Not Implemented",
70:"Only Restricted Digit Available",
79:"Service or Option Not Implemented",
87:"User Not a Member of CUG",
88:"Incompatible Destination",
95:"Invalid Message",
102:"Recovery On Timer Expiry",
111:"Protocol error",
127:"Interworking Unspecified",
400:"Bad Request",
401:"Unauthorized",
402:"Payment Required",
403:"Forbidden",
404:"Not Found",
405:"Method Not Allowed",
406:"Not Acceptable",
407:"Proxy Authentication Required",
408:"Request Timeout",
409:"Conflict",
410:"Number Changed",
411:"Length Required",
413:"Request Entry Too Long",
414:"Request URI Too Long",
415:"Unsupported Media Type",
416:"Unsupported URI Scheme",
420:"Bad Extension",
421:"Extension Required",
423:"Interval Too Brief",
480:"Temporarily Unavailable",
481:"Call Transaction Does Not Exist",
482:"Loop Detected",
483:"Too Many Hops",
484:"Address Incomplete",
485:"Unallocated Number",
486:"Busy Here",
487:"Request Terminated",
488:"Not Acceptable",
500:"Server Internal Error",
501:"Not Implemented",
502:"Bad Gateway",
503:"Service Unavailable",
504:"Server Timeout",
505:"Version Not Supported",
513:"Message Too Long",
600:"Busy Everywhere",
603:"Decline",
604:"Does Not Exist Anywhere",
606:"Not Acceptable"}

def getcode(causevalue):
    try:
        dcodes = disable_codes(causevalue)
        if dcodes==1:
            return "DISABLED"
        causedesc = causedict.get(causevalue)
        if causedesc:
            return causedesc
        else:
            return None
    except Exception as e:
        print("%s : %s %s caught exception %s" % (datetime.datetime.now(),"causecodetable", "93", e))


def disable_codes(causevalue):
    disable_code = prop.disablecausecodes.get(causevalue,0)
    return disable_code
