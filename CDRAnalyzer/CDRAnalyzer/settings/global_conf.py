"""
    module represents config file for CDRAnalyzer program.

"""
import pymysql.cursors
import sys
sys.path.append('C:/Users/manoraju/Desktop/pythonweb-app/pythonconfigure-karthik/CPO/Configuringpython/')

from CDRAnalyzer.util.file import filepath
#Debug Output
DEBUG = False

#Default Timezone
TIME_ZONE = 'America/Chicago'

#Default Path for Monitoring CDR Files.
MON_PATH = 'C:/Users/manoraju/Desktop/pythonweb-app/pythonconfigure-karthik/CPO/DATA/'

#DEFAULT MQ host and Port
#HOSTNAME = socket.gethostname()
#HOST = socket.gethostbyname(HOSTNAME)
# Configure Static IP for MQ
HOST = 'localhost'
PORT = 15672
if not HOST:
    import socket
    HOSTNAME = socket.gethostname()
    HOST = socket.gethostbyname(HOSTNAME)

# List of Queue Name for MQ
Queue = ["QCDR"]

# Default content type and charset to use for all HttpResponse objects,
DEFAULT_CONTENT_TYPE = 'text/html'
DEFAULT_CHARSET = 'utf-8'

# Email address that error messages come from
SERVER_EMAIL = 'root@localhost'

# Database connection info.
DATABASES = {}

# Host for sending email.
EMAIL_HOST = 'localhost'

# Port for sending email.
EMAIL_PORT = 25

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False


# Default email address to use for various automated correspondence from
# the site managers.
DEFAULT_FROM_EMAIL = 'webmaster@localhost'

# Default formatting for date objects.
DATE_FORMAT = 'N j, Y'

# Default formatting for datetime objects.
DATETIME_FORMAT = 'N j, Y, P'

# Default formatting for time objects.
TIME_FORMAT = 'P'

# Default formatting for date objects when only the year and month are relevant.
YEAR_MONTH_FORMAT = 'F Y'

# Default short formatting for date objects.
SHORT_DATE_FORMAT = 'm/d/Y'

DATABASES = {
    "ENGINE": {
        "MySQLdb"
    }
}
#Database Configuration
database = "db_name"
user = "root"
password = "XXXXXXXX"
charSet = "utf8mb4"
cursorType = pymysql.cursors.DictCursor

#Remote URL to post request
url = "http://dummyurl.com"

#Cache for storing file entry
try:
    f = filepath()
    cache = f.read_file()
except:
    cache = []

maxcount = 2  # max auth codes that can be used in maxtime interval
maxtime =  2  # max time interval
startchunk = 1 # Total rows to be fetched
endchunk = 1000 # Total end rows to be fetched
defaultchunk = 1001 # in case maxchunk is 0

defaultquery = "select count(*) from cdr_portal.cdr_main;"
