import requests
import json

HEADER = {"Content-Type": "application/json"}

class NegotiationController():
   

    #die Reihenfolge der funktionen im Code entspricht der in der sie aufgerufen werden sollen

    #fetch the catalog from the provider
    def getCataloge(ProducerIp):
        json_str = "{}"
        try:
            file = open('resources/fetch-catalog.json')
            json_str = file.read()
        finally:
            endpointUrl = "http://" + ProducerIp + ":19193/management/v3/catalog/request"
            response = requests.post(endpointUrl, data=json_str, headers=HEADER)


        if (response.status_code == 200):
            response_json = response.json()
            contractOfferId = "none"
            try:
                dataset = response_json['dcat:dataset']
                policy = dataset['odrl:hasPolicy']
                contractOfferId = policy['@id']
            finally:
                return contractOfferId
        return -1


    #send the retrieved contract back to the provider, to show our agreement. If the provider aceppts, it returns a contract-negotiation-id
    def sendContractOffer(ProducerIp, contractOfferId):
        endpointUrl = "http://" + ProducerIp + ":19193/management/v3/contractnegotiations"

        file = open('resources/negotiate-contract.json')
        json_str = file.read()
        try: 
            parameter =  json.loads(json_str)
            parameter['policy']['@id'] = contractOfferId
            json_str = json.dumps(parameter)
        finally:
            response = requests.post(endpointUrl, data=json_str, headers=HEADER)

        
        if (response.status_code == 200):
            response_json = response.json()
            contractNegotiationId = "none"
            try:
                contractNegotiationId = response_json['@id']
            finally:
                return contractNegotiationId
        return -1



    # get the ID of the Contract Agreement, to reference it in futher Interactions
    def getContractAgreementId(ProducerIp, ContractNegotiationId):
        endpointUrl = "http://" + ProducerIp + ":19193/management/v3/contractnegotiations/" + ContractNegotiationId
        response = requests.get(endpointUrl, headers=HEADER)
        contractAgreementId  = "none"

        if (response.status_code == 200):
            response_json = response.json()
            try:
                contractAgreementId = response_json['contractAgreementId']
            finally:
                return contractAgreementId
        return -1



    # request the data
    def startTransfer(ProducerIp, ContractAgreementId):
        endpointUrl = "http://" + ProducerIp + ":19193/management/v3/transferprocesses"

        file = open('resources/start-transfer.json')
        json_str = file.read()
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
        return -1



    #check transfer status
    def getTransferStatus(ProducerIp, TransferProcessId):
        endpointUrl = "http://" + ProducerIp + ":19193/management/v3/transferprocesses/" + TransferProcessId
        response = requests.get(endpointUrl, headers=HEADER)
        state  = "none"

        if (response.status_code == 200):
            response_json = response.json()
            try:
                state = response_json['state']
            finally:
                return state
        return -1


    #nun brauchen wir noch ein Access Token um die Daten zu erreichen
    def getEndpointDataReference(ProducerIp, TransferProcessId):
        endpointUrl = "http://" + ProducerIp + ":19193/management/v3/edrs/" + TransferProcessId + "/dataaddress"
        response = requests.get(endpointUrl, headers=HEADER)
        token = 'none'

        if (response.status_code == 200):
            response_json = response.json()
            try:
                token = response_json['authorization']
            finally:
                return token
        print(response.status_code)
        return -1


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
        return -1