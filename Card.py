class Card:
    def __init__(self, color, number):
        self.color = color
        self.number = number

    def __repr__(self):
        return f"{self.color.capitalize()} {self.number}"
    
    def __eq__(self, obj):
        if isinstance(obj, Card):
            return (self.color == obj.color and self.number == obj.number)
        return False
    
    def __hash__(self):
        return hash((self.color, self.number))