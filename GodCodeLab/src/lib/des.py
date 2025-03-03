from abc import ABC, abstractmethod

class Des:
    DES1: str = "DES1"
    DES8: str = "DES8"
    DEFAULT: str = DES8

    def __init__(self, text):
        self.text = text

    def get_ord(self, char):
        """Default implementation, can be overridden."""
        return ord(char)
    
    def gc_sum(self):
        return sum(self.get_ord(char) for char in self.text)
    
    def __str__(self):
        gc_sum = self.gc_sum()
        steps = []
        while gc_sum >= 10:
            steps.append(gc_sum)
            gc_sum = sum(int(digit) for digit in str(gc_sum))
        steps.append(gc_sum)
        return f"{'|'.join(map(str, steps[:-1]))}|{gc_sum}"
    
    @classmethod
    def get_instance(cls, des_to_get: str = None, 
        text: str = None):
        if des_to_get is None or des_to_get == cls.DEFAULT:
            return Des8(text)
        elif des_to_get == cls.DES1:
            return Des1(text)
        elif des_to_get == cls.DES8:
            return Des8(text)
        else:
            raise ValueError(f"Unknown des: {des_to_get}")
            
class Des1(Des):
    def get_ord(self, char):
        # Overrides the default get_ord implementation.
        return ord(char.upper()) - 64

class Des8(Des):
    # Inherits get_ord() from CharacterSet.
    pass
    