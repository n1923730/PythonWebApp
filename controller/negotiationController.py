import requests
import json

HEADER = {"Content-Type": "application/json"}

class NegotiationController():
   

    #die Reihenfolge der funktionen im Code entspricht der in der sie aufgerufen werden sollen

    #fetch the catalog from the pro
    def getCataloge(ProducerIp):
        json_str = "{}"
        try:
            file = open('resources/fetch-catalog.json')
            json_str = file.read()
            file.close()
            json_var = json.loads(json_str)
            json_var["counterPartyAddress"] = "http://" + ProducerIp + ":19194/protocol"
            json_str = json.dumps(json_var)
        finally:
            endpointUrl = "http://localhost:29193/management/v3/catalog/request"
            response = requests.post(endpointUrl, data=json_str, headers=HEADER)


        if (response.status_code == 200):
            response_json = response.json()
            contractOfferId = "none"
            try:
                dataset = response_json['dcat:dataset']
                policy = dataset['odrl:hasPolicy']
                contractOfferId = policy['@id']
            finally:
                print(str(response.json()))
                return contractOfferId
            
        print(str(response))
        return "none"


    #send the retrieved contract back to the provider, to show our agreement. If the provider aceppts, it returns a contract-negotiation-id
    def sendContractOffer(ProducerIp, contractOfferId):
        endpointUrl = "http://localhost:29193/management/v3/contractnegotiations"

        file = open('resources/negotiate-contract.json')
        json_str = file.read()
        file.close()
        try: 
            parameter =  json.loads(json_str)
            parameter['policy']['@id'] = contractOfferId
            parameter["counterPartyAddress"] =  "http://" + ProducerIp + ":19194/protocol"
            json_str = json.dumps(parameter)

            file = open('resources/negotiate-contract.json', 'w')
            file.truncate()
            file.write(json_str)
            file.close()


        finally:
            response = requests.post(endpointUrl, data=json_str, headers=HEADER)

        
        if (response.status_code == 200):
            response_json = response.json()
            contractNegotiationId = "none"
            try:
                contractNegotiationId = response_json['@id']
            finally:
                return contractNegotiationId
        return "none"



    # get the ID of the Contract Agreement, to reference it in futher Interactions
    def getContractAgreementId(ProducerIp, ContractNegotiationId):
        endpointUrl = "http://localhost:29193/management/v3/contractnegotiations/" + ContractNegotiationId
        response = requests.get(endpointUrl, headers=HEADER)
        contractAgreementId  = "none"

        print("Ergebnis von getContractAgreementId = " + str(response.json()))

        if (response.status_code == 200):
            response_json = response.json()

            try:
                contractAgreementId = response_json['contractAgreementId']
            finally:
                return contractAgreementId
        return "none"



    # request the data
    def startTransfer(ProducerIp, ContractAgreementId):
        endpointUrl = "http://localhost:29193/management/v3/transferprocesses"

        file = open('resources/start-transfer.json')
        json_str = file.read()
        file.close()
        json_var = json.loads(json_str)
        json_var["counterPartyAddress"] = "http://" + ProducerIp + ":19194/protocol"
        json_str = json.dumps(json_var)
       

        try: 
            parameter =  json.loads(json_str)
            parameter['contractId'] = ContractAgreementId
            json_str = json.dumps(parameter)

        finally:
            response = requests.post(endpointUrl, data=json_str, headers=HEADER)

        
        if (response.status_code == 200):
            response_json = response.json()
            TransferProcessId = "none"
            try:
                TransferProcessId = response_json['@id']
            finally:
                return TransferProcessId
        return "none"



    #check transfer status
    def getTransferStatus(ProducerIp, TransferProcessId):
        endpointUrl = "http://localhost:29193/management/v3/transferprocesses/" + TransferProcessId
        response = requests.get(endpointUrl, headers=HEADER)
        state  = "none"

        if (response.status_code == 200):
            response_json = response.json()
            try:
                state = response_json['state']
            finally:
                return state
        print(state)
        return state


    #nun brauchen wir noch ein Access Token um die Daten zu erreichen
    def getEndpointDataReference(ProducerIp, TransferProcessId):
        endpointUrl = "http://localhost:29193/management/v3/edrs/" + TransferProcessId + "/dataaddress"
        response = requests.get(endpointUrl, headers=HEADER)
        token = 'none'

        if (response.status_code == 200):
            response_json = response.json()
            try:
                token = response_json['authorization']
            finally:
                return token
        print(response.status_code)
        return token


    #und jetzt holen wir die Daten
    def readAllTheData(ProducerIp, AuthToken):
        print(AuthToken)
        endpointUrl = "http://" + ProducerIp + ":19291/public/"
        print(endpointUrl)
        header = {"Content-Type": "application/json", "Authorization": AuthToken}
        response = requests.get(url=endpointUrl, headers=header)
        data = 'none'
        print(response.status_code)
        print(response.is_redirect)
        if (response.status_code == 200):
            response_json = response.content
            try:
                data = response_json
            finally:
                return data
        return data