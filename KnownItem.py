class KnownItem:
    def __init__(self, id: int, name: str):
        self.id = int(id)
        self.name = name
        
    def __eq__(self, anotherId):
        return self.id == anotherId