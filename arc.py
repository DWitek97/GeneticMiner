class ArcBase:
    def __init__(self, place, amount=1):
        """
        Arc in the petri net. 
        :place: The one place acting as source/target of the arc as arc in the net
        :amount: The amount of token removed/added from/to the place.
        """
        self.produced = 0
        self.consumed = 0
        self.missing = 0
        self.place = place
        self.amount = amount
        

class Out(ArcBase):
    def trigger(self):
        """
        Remove token.
        """
        self.place.holding -= self.amount
        self.consumed += 1

    def non_blocking(self):
        """
        Validate action of outgoing arc is possible.
        """
        if self.place.holding >= self.amount:
            return True
        else:
            self.missing +=1
            return False 
        

class In(ArcBase):  
    def trigger(self):
        """
        Add tokens.
        """
        self.place.holding += self.amount
        self.produced += 1
        
    def non_blocking(self):
        if self.place.holding < 1:
            return True
        else:
            return False
        #return self.place.holding == 0