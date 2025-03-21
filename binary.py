## Binary WAP Push message example
## Uses the Infobip API and contains a simple link
## Guranteed to work
## -renge 2025
import requests
import json
import time

key = "App infobipkeyimnotgoingtoshareherelol"
udh = "0605040B8423F0"
data = "400601AE02056A0045C60C036D2E72656E6765342E6E65740008010374657374696E6721000101"  # working link

payload = json.dumps({
    "messages": [
        {
            "binary": {
                "dataCoding": 4,
                "esmClass": 64,
                "hex": udh + data
            },
            "destinations": [
                {
                    "to": "420987654321"
                }
            ],
            "from": "420123456789",
            "flash": False,
            "validityPeriod": 720
        }
    ]
})
headers = {
    'Authorization': key,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

r = requests.post("https://nm1l58.api.infobip.com/sms/2/binary/advanced", headers=headers, data=payload)
print(r.status_code)
print(r.text)
