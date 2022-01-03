
##############################################################################
#                Serialization and deserialization classes
##############################################################################

class BaseSerializer:
    pass

class SaveManager:
    pass

class BaseSaveBackend:
    """
    Saves the serialized data as well as metadata to disk
    e.g. a to a sqlite database or plain text file depending on the serializer used
    """
