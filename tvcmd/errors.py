"""Exceptions raised by TVCMD"""

class TVCMDError(Exception):
    """Base class for all TVCMD exceptions.
    """

class ServerError(TVCMDError):
    """Raised when an error ocurred contacting the server or the server
    reply an unexpected response
    """

class ConfigError(TVCMDError):
    """Raised when an error ocurred contacting the server or the server
    reply an unexpected response
    """
