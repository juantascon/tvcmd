"""Exceptions raised by TVCMD"""

class TVCMDError(Exception):
    """Base class for all TVCMD exceptions"""

class SourceError(TVCMDError):
    """Error contacting the source server or unexpected response"""

class ConfigError(TVCMDError):
    """Error on saving or loading a configuration file"""
