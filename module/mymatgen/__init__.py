__author__ = ", ".join(["Shyue Ping Ong", "Anubhav Jain", "Geoffroy Hautier",
                        "William Davidson Richard", "Stephen Dacek",
                        "Sai Jayaraman", "Michael Kocher", "Dan Gunter",
                        "Shreyas Cholia", "Vincent L Chevrier",
                        "Rickard Armiento"])
__date__ = "Jul 23 2014"
__version__ = "2.9.13"

#Useful aliases for commonly used objects and modules.

#from .core import *
from .core import Element, Specie, DummySpecie, get_el_sp, Composition, \
    Structure, IStructure, Molecule, IMolecule, CovalentBond, get_bond_length, \
    Lattice, Site, PeriodicSite, SymmOp
from .serializers.json_coders import PMGJSONEncoder, PMGJSONDecoder, \
    pmg_dump, pmg_load
#from .electronic_structure.core import Spin, Orbital
#from .io.smartio import read_structure, write_structure, read_mol, write_mol
#from .matproj.rest import MPRester
