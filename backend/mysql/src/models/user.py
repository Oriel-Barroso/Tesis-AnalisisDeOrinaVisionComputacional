class User:
    def __init__(self, id: int, dni: str):
        self.id = id
        self.dni = dni

    def validate_dni(self):
        if not isinstance(self.dni, str):
            raise ValueError("DNI must be a string.")
        if len(self.dni) == 0:
            raise ValueError("DNI cannot be empty.")