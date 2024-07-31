from flask import render_template, Blueprint, redirect, send_file, url_for
from ..controller import negotiationController
# from time import sleep
# from threading import Thread
# from apscheduler.schedulers.background import BackgroundScheduler

negotiations_blueprint = Blueprint("negotiations", __name__, url_prefix="/negotiations")
ContractOfferId: str = "none"
ContractNegotiationId: str = "none"
ContractAgreementId: str = "none"
TransferProcessId: str = "none"
accessToken: str = "none"
ProducerIp: str = "128.0.0.1"
data: str  = "none"


class Negotiation:

    def registerProducerIp(Ip):
        global ProducerIp
        ProducerIp = Ip


    @negotiations_blueprint.route('/')
    def negotiations():
        return render_template('negotiation.html', content = {"ProducerIp":  ProducerIp})
    

    @negotiations_blueprint.route('/fetchCatalog')
    def fetchCatalog():
        global ContractOfferId
        ContractOfferId= negotiationController.NegotiationController.getCataloge(ProducerIp)
        if ContractOfferId != "none":
            return 'Das hat geklappt. Wir bekommen die ContractOfferId = ' + ContractOfferId
        return "Das hat nicht geklappt."


    @negotiations_blueprint.route('/negotiateContract')
    def negotiateContract():
        if ContractOfferId != "none":
            global ContractNegotiationId
            ContractNegotiationId = negotiationController.NegotiationController.sendContractOffer(ProducerIp, ContractOfferId)
        if ContractNegotiationId != "none":
            return 'Das hat geklappt. Wir bekommen die ContractNegotiationId = ' + ContractNegotiationId
        return "Das hat nicht geklappt."



    @negotiations_blueprint.route('/checkContractStatus')
    def checkContractStatus():
        if ContractNegotiationId != "none":
            global ContractAgreementId
            ContractAgreementId = negotiationController.NegotiationController.getContractAgreementId(ProducerIp, ContractNegotiationId)
        if ContractAgreementId != "none":
            return "Die Verhandlungen verliefen erfolgreich. Wir können sie mit der ContractAgreementId = " + ContractAgreementId + " bei der Datenabfrage referenzieren."
        return "Das hat nicht geklappt."


    @negotiations_blueprint.route('/requestTheData')
    def requestTheData():
        if ContractAgreementId != "none":
            global TransferProcessId
            TransferProcessId = negotiationController.NegotiationController.startTransfer(ProducerIp, ContractAgreementId)
        if TransferProcessId != "none":
            return "Der Transfer konnte gestartet werden. Wir können ihr mit der TransferProcessId = " + TransferProcessId + " referenzieren, um seinen Status zu überprüfen."
        return "Das hat nicht geklappt."


    @negotiations_blueprint.route('/checkTransferStatus')
    def checkTransferStatus():
        if TransferProcessId != "none":
            TransferStatus = negotiationController.NegotiationController.getTransferStatus(ProducerIp, TransferProcessId)
        match TransferStatus:
            case "STARTED": return "Der Transfer wurde gestartet."
            case "TERMINATED": return "Der Transfer verlief erfolgreich und ist abgeschlossen."
            case "DEPROVISIONED": return "Die Berechtigung ist abgelaufen."
            case "REQUESTED": return "Der Transfer wurde angefragt"

        print("Status = " + TransferStatus)
        return "Das hat nicht geklappt."


    @negotiations_blueprint.route('/checkTheData')
    def checkTheData():
        if ContractAgreementId != "none":
            global accessToken
            accessToken = negotiationController.NegotiationController.getEndpointDataReference(ProducerIp, TransferProcessId)
        if accessToken != "none":
            return "Wir haben ein Access Token. Jetzt können wir die Daten abholen."
        return "Das hat nicht geklappt."


    @negotiations_blueprint.route('/getTheData')
    def getTheData():
        if ContractAgreementId != "none":
            global data
            data = negotiationController.NegotiationController.readAllTheData(ProducerIp, accessToken)
        if data != "none" and data != '-1':
            return redirect('http://127.0.0.1:5000/negotiations/dataview', code=302)
        return "Das hat nicht geklappt."



    @negotiations_blueprint.route('/plot.png')
    def getThePlot():
         return send_file('./templates/plot.png', mimetype='image/png')
  
    def requestData() -> str:
         return data

