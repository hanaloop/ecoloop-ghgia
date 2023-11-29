from prisma import Client
_connection = None

def get_connection():
    global _connection
    if not _connection:
        _connection = Client()
    return _connection

# List of stuff accessible to importers of this module. Just in case
__all__ = [ 'getConnection' ]
