"""Exceptions raised by TVCMD"""

class TVCMDError(Exception):
    """Base class for all TVCMD exceptions"""

class ServerError(TVCMDError):
    """Error contacting the server or server unexpected response"""

class ConfigError(TVCMDError):
    """Error on saving or loading a configuration file
    """

class TrackError(TVCMDError):
    """Error tracking a tv show"""

class SearchError(TVCMDError):
    """Error searching a tv show or its episodes"""
