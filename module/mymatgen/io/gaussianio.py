#!/usr/bin/env python

"""
This module implements input and output processing from Gaussian.
"""

from __future__ import division

__author__ = "Shyue Ping Ong"
__copyright__ = "Copyright 2012, The Materials Project"
__version__ = "0.1"
__maintainer__ = "Shyue Ping Ong"
__email__ = "shyuep@gmail.com"
__date__ = "Apr 17, 2012"

import re

import numpy as np

from pymatgen.core.operations import SymmOp
from pymatgen.core import Element, Molecule, Composition
from monty.io import zopen
from pymatgen.util.coord_utils import get_angle


class GaussianInput(object):
    """
    An object representing a Gaussian input file.

    Args:
        mol: Input molecule. If molecule is a single string, it is used as a
            direct input to the geometry section of the Gaussian input
            file.
        charge: Charge of the molecule. If None, charge on molecule is used.
            Defaults to None. This allows the input file to be set a
            charge independently from the molecule itself.
        spin_multiplicity: Spin multiplicity of molecule. Defaults to None,
            which means that the spin multiplicity is set to 1 if the
            molecule has no unpaired electrons and to 2 if there are
            unpaired electrons.
        title: Title for run. Defaults to formula of molecule if None.
        functional: Functional for run.
        basis_set: Basis set for run.
        route_parameters: Additional route parameters as a dict. For example,
            {'SP':"", "SCF":"Tight"}
        input_parameters: Additional input parameters for run as a dict. Used
            for example, in PCM calculations.  E.g., {"EPS":12}
        link0_parameters: Link0 parameters as a dict. E.g., {"%mem": "1000MW"}
    """

    #Commonly used regex patterns
    zmat_patt = re.compile("^(\w+)*([\s,]+(\w+)[\s,]+(\w+))*[\-\.\s,\w]*$")
    xyz_patt = re.compile("^(\w+)[\s,]+([\d\.eE\-]+)[\s,]+([\d\.eE\-]+)[\s,]+"
                          "([\d\.eE\-]+)[\-\.\s,\w.]*$")

    def __init__(self, mol, charge=None, spin_multiplicity=None, title=None,
                 functional="HF", basis_set="6-31G(d)", route_parameters=None,
                 input_parameters=None, link0_parameters=None):
        self._mol = mol
        self.charge = charge if charge is not None else mol.charge
        nelectrons = - self.charge + mol.charge + mol.nelectrons
        if spin_multiplicity is not None:
            self.spin_multiplicity = spin_multiplicity
            if (nelectrons + spin_multiplicity) % 2 != 1:
                raise ValueError(
                    "Charge of {} and spin multiplicity of {} is"
                    " not possible for this molecule".format(
                        self.charge, spin_multiplicity))
        else:
            self.spin_multiplicity = 1 if nelectrons % 2 == 0 else 2
        self.functional = functional
        self.basis_set = basis_set
        self.link0_parameters = link0_parameters if link0_parameters else {}
        self.route_parameters = route_parameters if route_parameters else {}
        self.input_parameters = input_parameters if input_parameters else {}
        self.title = title if title else self._mol.composition.formula

    @property
    def molecule(self):
        """
        Returns molecule associated with this GaussianInput.
        """
        return self._mol

    @staticmethod
    def parse_coords(coord_lines):
        """
        Helper method to parse coordinates.
        """
        paras = {}
        var_pattern = re.compile("^([A-Za-z]+\S*)[\s=,]+([\d\-\.]+)$")
        for l in coord_lines:
            m = var_pattern.match(l.strip())
            if m:
                paras[m.group(1)] = float(m.group(2))

        species = []
        coords = []
        # Stores whether a Zmatrix format is detected. Once a zmatrix format
        # is detected, it is assumed for the remaining of the parsing.
        zmode = False
        for l in coord_lines:
            l = l.strip()
            if not l:
                break
            if (not zmode) and GaussianInput.xyz_patt.match(l):
                m = GaussianInput.xyz_patt.match(l)
                species.append(m.group(1))
                toks = re.split("[,\s]+", l.strip())
                if len(toks) > 4:
                    coords.append(map(float, toks[2:5]))
                else:
                    coords.append(map(float, toks[1:4]))
            elif GaussianInput.zmat_patt.match(l):
                zmode = True
                toks = re.split("[,\s]+", l.strip())
                species.append(toks[0])
                toks.pop(0)
                if len(toks) == 0:
                    coords.append(np.array([0, 0, 0]))
                else:
                    nn = []
                    parameters = []
                    while len(toks) > 1:
                        ind = toks.pop(0)
                        data = toks.pop(0)
                        try:
                            nn.append(int(ind))
                        except ValueError:
                            nn.append(species.index(ind) + 1)
                        try:
                            val = float(data)
                            parameters.append(val)
                        except ValueError:
                            if data.startswith("-"):
                                parameters.append(-paras[data[1:]])
                            else:
                                parameters.append(paras[data])
                    if len(nn) == 1:
                        coords.append(np.array([0, 0, parameters[0]]))
                    elif len(nn) == 2:
                        coords1 = coords[nn[0] - 1]
                        coords2 = coords[nn[1] - 1]
                        bl = parameters[0]
                        angle = parameters[1]
                        axis = [0, 1, 0]
                        op = SymmOp.from_origin_axis_angle(coords1, axis,
                                                           angle, False)
                        coord = op.operate(coords2)
                        vec = coord - coords1
                        coord = vec * bl / np.linalg.norm(vec) + coords1
                        coords.append(coord)
                    elif len(nn) == 3:
                        coords1 = coords[nn[0] - 1]
                        coords2 = coords[nn[1] - 1]
                        coords3 = coords[nn[2] - 1]
                        bl = parameters[0]
                        angle = parameters[1]
                        dih = parameters[2]
                        v1 = coords3 - coords2
                        v2 = coords1 - coords2
                        axis = np.cross(v1, v2)
                        op = SymmOp.from_origin_axis_angle(
                            coords1, axis, angle, False)
                        coord = op.operate(coords2)
                        v1 = coord - coords1
                        v2 = coords1 - coords2
                        v3 = np.cross(v1, v2)
                        adj = get_angle(v3, axis)
                        axis = coords1 - coords2
                        op = SymmOp.from_origin_axis_angle(
                            coords1, axis, dih - adj, False)
                        coord = op.operate(coord)
                        vec = coord - coords1
                        coord = vec * bl / np.linalg.norm(vec) + coords1
                        coords.append(coord)

        def parse_species(sp_str):
            """
            The species specification can take many forms. E.g.,
            simple integers representing atomic numbers ("8"),
            actual species string ("C") or a labelled species ("C1").
            Sometimes, the species string is also not properly capitalized,
            e.g, ("c1"). This method should take care of these known formats.
            """
            try:
                return int(sp_str)
            except ValueError:
                sp = re.sub("\d", "", sp_str)
                return sp.capitalize()

        species = map(parse_species, species)

        return Molecule(species, coords)

    @staticmethod
    def from_string(contents):
        """
        Creates GaussianInput from a string.

        Args:
            contents: String representing an Gaussian input file.

        Returns:
            GaussianInput object
        """
        lines = [l.strip() for l in contents.split("\n")]
        route_patt = re.compile("^#[sSpPnN]*.*")
        route = None
        for i, l in enumerate(lines):
            if route_patt.match(l):
                route = l
                route_index = i
                break
        route_paras = {}
        if route:
            for tok in route.split():
                if tok.strip().startswith("#"):
                    continue
                if re.match("[\S]+/.*", tok):
                    d = tok.split("/")
                    functional = d[0]
                    basis_set = d[1]
                else:
                    d = tok.split("=")
                    v = None if len(d) == 1 else d[1]
                    route_paras[d[0]] = v
        ind = 2
        title = []
        while lines[route_index + ind].strip():
            title.append(lines[route_index + ind].strip())
            ind += 1
        title = ' '.join(title)
        ind += 1
        toks = re.split("[\s,]", lines[route_index + ind])
        charge = int(toks[0])
        spin_mult = int(toks[1])
        coord_lines = []
        spaces = 0
        input_paras = {}
        ind += 1
        for i in xrange(route_index + ind, len(lines)):
            if lines[i].strip() == "":
                spaces += 1
            if spaces >= 2:
                d = lines[i].split("=")
                if len(d) == 2:
                    input_paras[d[0]] = float(d[1])
            else:
                coord_lines.append(lines[i].strip())
        mol = GaussianInput.parse_coords(coord_lines)
        mol.set_charge_and_spin(charge, spin_mult)

        return GaussianInput(mol, charge=charge, spin_multiplicity=spin_mult,
                             title=title, functional=functional,
                             basis_set=basis_set, route_parameters=route_paras,
                             input_parameters=input_paras)

    @staticmethod
    def from_file(filename):
        """
        Creates GaussianInput from a file.

        Args:
            filename: Gaussian input filename

        Returns:
            GaussianInput object
        """
        with zopen(filename, "r") as f:
            return GaussianInput.from_string(f.read())

    def _find_nn_pos_before_site(self, siteindex):
        """
        Returns index of nearest neighbor atoms.
        """
        alldist = [(self._mol.get_distance(siteindex, i), i)
                   for i in xrange(siteindex)]
        alldist = sorted(alldist, key=lambda x: x[0])
        return [d[1] for d in alldist]

    def get_zmatrix(self):
        """
        Returns a z-matrix representation of the molecule.
        """
        output = []
        outputvar = []
        for i, site in enumerate(self._mol):
            if i == 0:
                output.append("{}".format(site.specie))
            elif i == 1:
                nn = self._find_nn_pos_before_site(i)
                bondlength = self._mol.get_distance(i, nn[0])
                output.append("{} {} B{}".format(self._mol[i].specie,
                                                 nn[0] + 1, i))
                outputvar.append("B{}={:.6f}".format(i, bondlength))
            elif i == 2:
                nn = self._find_nn_pos_before_site(i)
                bondlength = self._mol.get_distance(i, nn[0])
                angle = self._mol.get_angle(i, nn[0], nn[1])
                output.append("{} {} B{} {} A{}".format(self._mol[i].specie,
                                                        nn[0] + 1, i,
                                                        nn[1] + 1, i))
                outputvar.append("B{}={:.6f}".format(i, bondlength))
                outputvar.append("A{}={:.6f}".format(i, angle))
            else:
                nn = self._find_nn_pos_before_site(i)
                bondlength = self._mol.get_distance(i, nn[0])
                angle = self._mol.get_angle(i, nn[0], nn[1])
                dih = self._mol.get_dihedral(i, nn[0], nn[1], nn[2])
                output.append("{} {} B{} {} A{} {} D{}"
                              .format(self._mol[i].specie, nn[0] + 1, i,
                                      nn[1] + 1, i, nn[2] + 1, i))
                outputvar.append("B{}={:.6f}".format(i, bondlength))
                outputvar.append("A{}={:.6f}".format(i, angle))
                outputvar.append("D{}={:.6f}".format(i, dih))
        return "\n".join(output) + "\n\n" + "\n".join(outputvar)

    def __str__(self):
        def para_dict_to_string(para, joiner=" "):
            para_str = ["{}={}".format(k, v) if v else k
                        for k, v in para.items()]
            return joiner.join(para_str)

        output = []
        if self.link0_parameters:
            output.append(para_dict_to_string(self.link0_parameters, "\n"))
        output.append("#P {func}/{bset} {route} Test"
                      .format(func=self.functional, bset=self.basis_set,
                              route=para_dict_to_string(self.route_parameters))
                      )
        output.append("")
        output.append(self.title)
        output.append("")
        output.append("{} {}".format(self.charge, self.spin_multiplicity))
        if isinstance(self._mol, Molecule):
            output.append(self.get_zmatrix())
        else:
            output.append(str(self._mol))
        output.append("")
        output.append(para_dict_to_string(self.input_parameters, "\n"))
        output.append("")
        return "\n".join(output)

    def write_file(self, filename):
        with zopen(filename, "w") as f:
            f.write(self.__str__())


class GaussianOutput(object):
    """
    Parser for Gaussian output files.

    Args:
        filename: Filename of Gaussian output file.

    .. note::

        Still in early beta.

    Attributes:

    .. attribute:: structures

        All structures from the calculation.

    .. attribute:: energies

        All energies from the calculation.

    .. attribute:: properly_terminated

        True if run has properly terminated

    .. attribute:: is_pcm

        True if run is a PCM run.

    .. attribute:: stationary_type

        If it is a relaxation run, indicates whether it is a minimum (Minimum)
        or a saddle point ("Saddle").

    .. attribute:: corrections

        Thermochemical corrections if this run is a Freq run as a dict. Keys
        are "Zero-point", "Thermal", "Enthalpy" and "Gibbs Free Energy"

    .. attribute:: functional

        Functional used in the run.

    .. attribute:: basis_set

        Basis set used in the run

    .. attribute:: charge

        Charge for structure

    .. attribute:: spin_mult

        Spin multiplicity for structure

    .. attribute:: num_basis_func

        Number of basis functions in the run.

    .. attribute:: pcm

        PCM parameters and output if available.
    """

    def __init__(self, filename):
        self.filename = filename
        self._parse(filename)

    @property
    def final_energy(self):
        return self.energies[-1]

    @property
    def final_structure(self):
        return self.structures[-1]

    def _parse(self, filename):
        start_patt = re.compile(" \(Enter \S+l101\.exe\)")
        route_patt = re.compile(" #[pPnNtT]*.*")
        charge_mul_patt = re.compile("Charge\s+=\s*([-\\d]+)\s+"
                                     "Multiplicity\s+=\s*(\d+)")
        num_basis_func_patt = re.compile("([0-9]+)\s+basis functions")
        pcm_patt = re.compile("Polarizable Continuum Model")
        stat_type_patt = re.compile("imaginary frequencies")
        scf_patt = re.compile("E\(.*\)\s*=\s*([-\.\d]+)\s+")
        mp2_patt = re.compile("EUMP2\s*=\s*(.*)")
        oniom_patt = re.compile("ONIOM:\s+extrapolated energy\s*=\s*(.*)")
        termination_patt = re.compile("(Normal|Error) termination of Gaussian")
        std_orientation_patt = re.compile("Standard orientation")
        end_patt = re.compile("--+")
        orbital_patt = re.compile("Alpha\s*\S+\s*eigenvalues --(.*)")
        thermo_patt = re.compile("(Zero-point|Thermal) correction(.*)="
                                 "\s+([\d\.-]+)")

        self.properly_terminated = False
        self.is_pcm = False
        self.stationary_type = "Minimum"
        self.structures = []
        self.corrections = {}
        self.energies = []
        self.pcm = None

        coord_txt = []
        read_coord = 0
        orbitals_txt = []
        parse_stage = 0
        num_basis_found = False
        terminated = False

        with zopen(filename) as f:
            for line in f:
                if parse_stage == 0:
                    if start_patt.search(line):
                        parse_stage = 1
                    elif route_patt.search(line):
                        self.route = {}
                        for tok in line.split():
                            sub_tok = tok.strip().split("=")
                            key = sub_tok[0].upper()
                            self.route[key] = sub_tok[1].upper() \
                                if len(sub_tok) > 1 else ""
                            m = re.match("(\w+)/([^/]+)", key)
                            if m:
                                self.functional = m.group(1)
                                self.basis_set = m.group(2)
                elif parse_stage == 1:
                    if charge_mul_patt.search(line):
                        m = charge_mul_patt.search(line)
                        self.charge = int(m.group(1))
                        self.spin_mult = int(m.group(2))
                        parse_stage = 2
                elif parse_stage == 2:

                    if self.is_pcm:
                        self._check_pcm(line)

                    if "FREQ" in self.route and thermo_patt.search(line):
                        m = thermo_patt.search(line)
                        if m.group(1) == "Zero-point":
                            self.corrections["Zero-point"] = float(m.group(3))
                        else:
                            key = m.group(2).strip(" to ")
                            self.corrections[key] = float(m.group(3))

                    if read_coord:
                        if not end_patt.search(line):
                            coord_txt.append(line)
                        else:
                            read_coord = (read_coord + 1) % 4
                            if not read_coord:
                                sp = []
                                coords = []
                                for l in coord_txt[2:]:
                                    toks = l.split()
                                    sp.append(Element.from_Z(int(toks[1])))
                                    coords.append(map(float, toks[3:6]))
                                self.structures.append(Molecule(sp, coords))
                    elif termination_patt.search(line):
                        m = termination_patt.search(line)
                        if m.group(1) == "Normal":
                            self.properly_terminated = True
                        terminated = True
                    elif (not num_basis_found) and \
                            num_basis_func_patt.search(line):
                        m = num_basis_func_patt.search(line)
                        self.num_basis_func = int(m.group(1))
                        num_basis_found = True
                    elif (not self.is_pcm) and pcm_patt.search(line):
                        self.is_pcm = True
                        self.pcm = {}
                    elif "FREQ" in self.route and "OPT" in self.route and \
                            stat_type_patt.search(line):
                        self.stationary_type = "Saddle"
                    elif mp2_patt.search(line):
                        m = mp2_patt.search(line)
                        self.energies.append(float(m.group(1).replace("D",
                                                                      "E")))
                    elif oniom_patt.search(line):
                        m = oniom_patt.matcher(line)
                        self.energies.append(float(m.group(1)))
                    elif scf_patt.search(line):
                        m = scf_patt.search(line)
                        self.energies.append(float(m.group(1)))
                    elif std_orientation_patt.search(line):
                        coord_txt = []
                        read_coord = 1
                    elif orbital_patt.search(line):
                        orbitals_txt.append(line)
        if not terminated:
            raise IOError("Bad Gaussian output file.")

    def _check_pcm(self, line):
        energy_patt = re.compile("(Dispersion|Cavitation|Repulsion) energy"
                                 "\s+\S+\s+=\s+(\S*)")
        total_patt = re.compile("with all non electrostatic terms\s+\S+\s+"
                                "=\s+(\S*)")
        parameter_patt = re.compile("(Eps|Numeral density|RSolv|Eps"
                                    "\(inf[inity]*\))\s*=\s*(\S*)")

        if energy_patt.search(line):
            m = energy_patt.search(line)
            self.pcm['{} energy'.format(m.group(1))] = float(m.group(2))
        elif total_patt.search(line):
            m = total_patt.search(line)
            self.pcm['Total energy'] = float(m.group(1))
        elif parameter_patt.search(line):
            m = parameter_patt.search(line)
            self.pcm[m.group(1)] = float(m.group(2))

    @property
    def to_dict(self):
        """
        Json-serializable dict representation.
        """
        structure = self.final_structure
        d = {"has_gaussian_completed": self.properly_terminated,
             "nsites": len(structure)}
        comp = structure.composition
        d["unit_cell_formula"] = comp.to_dict
        d["reduced_cell_formula"] = Composition(comp.reduced_formula).to_dict
        d["pretty_formula"] = comp.reduced_formula
        d["is_pcm"] = self.is_pcm

        unique_symbols = sorted(list(d["unit_cell_formula"].keys()))
        d["elements"] = unique_symbols
        d["nelements"] = len(unique_symbols)
        d["charge"] = self.charge
        d["spin_multiplicity"] = self.spin_mult

        vin = {"route": self.route, "functional": self.functional,
               "basis_set": self.basis_set,
               "nbasisfunctions": self.num_basis_func,
               "pcm_parameters": self.pcm}

        d["input"] = vin

        nsites = len(self.final_structure)

        vout = {
            "energies": self.energies,
            "final_energy": self.final_energy,
            "final_energy_per_atom": self.final_energy / nsites,
            "molecule": structure.to_dict,
            "stationary_type": self.stationary_type,
            "corrections": self.corrections
        }

        d['output'] = vout

        return d
