class CrewManagement:
    def __init__(self, registration_module):
        self.registration = registration_module
        self.skills = {}

    def assign_role(self, name, role):
        if name not in self.registration.list_members():
            raise ValueError("Cannot assign role to unregistered member")
            
        current_role = self.registration.members[name]
        if role != current_role:
             self.registration.members[name] = role
             
        if name not in self.skills:
            self.skills[name] = 1 # base skill
            
        return True

    def assign_skill(self, name, level):
        if name not in self.registration.list_members():
            raise ValueError("Member not found")
        self.skills[name] = level

    def list_skills(self):
        return self.skills

    def get_skill_level(self, name):
        return self.skills.get(name, 0)
        
    def check_roles(self, required_roles):
        available_roles = list(self.registration.list_members().values())
        for req in required_roles:
            if req not in available_roles:
                return False
            available_roles.remove(req)
        return True
