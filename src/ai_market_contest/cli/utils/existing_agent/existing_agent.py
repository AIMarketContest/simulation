class ExistingAgent:
    def __init__(self, agent_name):
        self.agent_name = agent_name
    
    def get_name(self) -> str:
        return self.agent_name