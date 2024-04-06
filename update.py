from enum import Enum
from urllib.request import urlretrieve
import version
import version_latest
from importlib import reload

# code has been tested, works fine in idle -mal

url_version =  'https://raw.githubusercontent.com/Dpeta/pesterchum-alt-servers/main/version.py'
url_changelog = 'https://raw.githubusercontent.com/Dpeta/pesterchum-alt-servers/main/CHANGELOG.md'

class pc(Enum):
    CURRENT_VERSION = 'current'
    LATEST_VERSION = 'latest'
    CHANGELOG = 'changelog'

def gitfetch(option):
    content = None
    match option.value:

        case 'current':
            content = version.buildVersion

        case 'latest':
            urlretrieve(url_version, 'version_latest.py')
            reload(version_latest)
            content = version_latest.buildVersion

        case 'changelog':
            urlretrieve(url_changelog, 'changelog.txt')      
            with open('changelog.txt', 'r') as file:
                content = file.read()

    return content


gitfetch(pc.CURRENT_VERSION)
gitfetch(pc.LATEST_VERSION)
gitfetch(pc.CHANGELOG)