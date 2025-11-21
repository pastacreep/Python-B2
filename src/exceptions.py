
class ErreurBibliotheque(Exception):
    """Exception personnalisée pour la bibliothèque."""
    def __init__(self, message):
        super().__init__(message)
