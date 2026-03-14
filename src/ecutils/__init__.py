# ecutils/__init__.py

"""ecutils — Elliptic Curve Cryptography utilities.

Quick start
-----------
>>> from ecutils import Point, get_curve, get_generator
>>>
>>> curve = get_curve("secp256k1")
>>> G = get_generator("secp256k1")
>>> pub = 0xDEADBEEF * G
"""

# Algorithms
from ecutils.algorithms.digital_signature import DigitalSignature
from ecutils.algorithms.koblitz import Koblitz
from ecutils.core.curve import CoordinateSystem, CurveParams
from ecutils.core.point import Point
from ecutils.curves.registry import get_curve, get_generator

# Protocols
from ecutils.protocols.diffie_hellman import DiffieHellman
from ecutils.protocols.massey_omura import MasseyOmura

__version__ = "2.0.0"

__all__ = [
    # Core
    "CoordinateSystem",
    "CurveParams",
    "Point",
    "get_curve",
    "get_generator",
    # Algorithms
    "DigitalSignature",
    "Koblitz",
    # Protocols
    "DiffieHellman",
    "MasseyOmura",
]
