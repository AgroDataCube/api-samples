#
# A very simple example fetchting ndvi data for field 8. You can get a free limited usage token at https://agrodatacube.wur.nl/api/register.jsp
#

import requests
import datetime 

     
if __name__ == "__main__":
    #
    # Create webserviceD
    #
    httpUrl = "https://AgrodataCube.wur.nl/api/v2/rest/fields/8/ndvi"
    httpResponse = requests.get(httpUrl, headers={"token":"<your token>"})
    print httpResponse.text;
    
    
