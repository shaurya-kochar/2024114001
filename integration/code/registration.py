class Registration:
    def __init__(self):
        self.members = {}

    def register_member(self, name, role):
        if not name or not role:
            raise ValueError("Name and role cannot be empty")
        valid_roles = ["driver", "mechanic", "strategist"]
        if role not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of {valid_roles}")
        
        if name in self.members:
            raise ValueError("Member already registered")
            
        self.members[name] = role
        return True

    def list_members(self):
        return self.members
