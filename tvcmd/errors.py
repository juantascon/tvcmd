"""Exceptions raised by TVCMD"""

class TVCMDError(Exception):
    """Base class for all TVCMD exceptions"""

class SourceError(TVCMDError):
    """Error contacting the source server or unexpected response"""

class ConfigError(TVCMDError):
    """Error saving or loading a configuration file"""

class TrackError(TVCMDError):
    """Error tracking a show"""
