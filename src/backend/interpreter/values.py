from dataclasses import dataclass

@dataclass
class Number:
    Value: float

    def __repr__(self):
        return f"{self.Value}"