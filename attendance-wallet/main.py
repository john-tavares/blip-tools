from uuid import uuid4
import requests

KEY = "Your API Key"
COMMAND_URL = "https://http.msging.net/commands"
HEADERS = {"Authorization": KEY}

def generate_identity(email:str):
    """
        Generate a wallet id for the given name
    """
    email = email.replace("@", "%40")
    return email+"@blip.ai"

def add_agent(identity:str, teams:list):
    """
        Add an agent to the wallet
    """
    data = {
        "id": str(uuid4()),
        "to": "postmaster@desk.msging.net",
        "method": "set",
        "uri": "/attendants",
        "type": "application/vnd.iris.desk.attendant+json",
        "resource": {
            "identity": identity,
            "teams": teams
        }
    }
    response = requests.post(COMMAND_URL, json=data, headers={"Authorization": KEY})
    return response.json()

def add_wallet_queue(identity:str, wallet_name:str):
    """
        Add a rule to the wallet
    """
    data = {
        "id": str(uuid4()),
        "to": "postmaster@desk.msging.net",
        "method": "set",
        "uri": "/rules",
        "type": "application/vnd.iris.desk.rule+json",
        "resource": {
            "id": str(uuid4()),
            "isActive": True,
            "property": "Contact.Extras.City",
            "relation": "Equals",
            "team": wallet_name,
            "title": f"FILA - {wallet_name}",
            "values": [
                wallet_name
            ],
            "conditions":[
                {
                    "property":"Contact.Extras.pool",
                    "relation":"Equals",
                    "values":[
                        wallet_name
                    ]
                }
            ],
            "operator":"Or",
            "priority":3,
            "storageDate":"2021-01-19T15:13:03.340Z"
        },
    }
    response = requests.post(COMMAND_URL, json=data, headers={"Authorization": KEY})
    return response.json()

def create_agent_wallet(wallet_name:str, teams:list, identity:str=None):
    """
        Add an agent to the wallet
    """    
    # TODO: add parameter to keep teams or not
    # For now, keep the teams
    teams.append(wallet_name)
    
    add_agent(identity, teams)
    add_wallet_queue(identity, wallet_name)

def get_all_attendants():
    """
        Get all attendants
    """
    data = {
        "id": str(uuid4()),
        "to": "postmaster@desk.msging.net",
        "method": "get",
        "uri": "/attendants"
    }
    response = requests.post(COMMAND_URL, json=data, headers=HEADERS)
    return response.json()['resource']['items']

def create_wallet_for_all_agents_in_bot():
    """
        Create a wallet for all agents in the bot
    """
    agents = get_all_attendants()
    
    for agent in agents:
        name = agent['fullName']
        
        wallet_name = name.upper()
        agent_teams = agent['teams']

        if wallet_name not in agent_teams:
            create_agent_wallet(wallet_name, agent_teams, agent['identity'])
            print(f"Agent: {name} wallet added")
        else:
            print(f"Agent: {name} wallet already exists")

if __name__ == "__main__":
    # TODO: add other fuction to import agents from a sheet
    create_wallet_for_all_agents_in_bot()