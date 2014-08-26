#!/usr/bin/python
# -*- coding:  utf-8 -*-
"""
共有のグローバル変数を保管
"""

COLOR_PALETTE = {'blue': ('blue', 'cyan'),
                 'magenta': ('magenta', 'pink'),
                 'green': ('green', '#00ff00'),
                 0: ('#EF6F00', '#FFAF30'), 1: ('#EF7000', '#FFB030'),
                 2: ('#EF4400', '#FF7430'), 3: ('#EF0000', '#FF3030'),
                 4: ('#EF001A', '#FF304A'), 5: ('#EF0044', '#FF3074'),
                 6: ('#EF006F', '#FF309F'), 7: ('#EF009A', '#FF30DA'),
                 8: ('#EF00C4', '#FF30F4'), 9: ('#CF00EF', '#FF30FF'),
                 10: ('#9900EF', '#D930FF'), 11: ('#6F00EF', '#AF30FF'),
                 12: ('#4400EF', '#8430FF'), 13: ('#1A00EF', '#5A30FF'),
                 14: ('#0000EF', '#3030FF'), 15: ('#001AEF', '#305AFF'),
                 16: ('#0045EF', '#3085FF'), 17: ('#006FEF', '#30AFFF'),
                 18: ('#009AEF', '#30DAFF'), 19: ('#00C4EF', '#30F4FF'),
                 20: ('#00EFEF', '#30FFFF'), 21: ('#00EFC4', '#30FFF4'),
                 22: ('#00EF99', '#30FFD9'), 23: ('#00EF6F', '#30FFAF'),
                 24: ('#00EF44', '#30FF84'), 25: ('#00EF1A', '#30FF5A'),
                 26: ('#00EF00', '#30FF30'), 27: ('#45EF00', '#85FF30'),
                 28: ('#6FEF00', '#AFFF30'), 29: ('#9AEF00', '#DAFF30'),
                 30: ('#C4EF00', '#F4FF30'), 31: ('#EFEF00', '#FFFF30'),
                 32: ('#EFC400', '#FFF430'), 33: ('#EF9900', '#FFD930')}

ELEMENTS = {'Vac': {'Z': 0, 'Rwigs': 1.5}, 'H': {'Z': 1, 'Rwigs': 1.39},
            'He': {'Z': 2, 'Rwigs': 2.55}, 'Li': {'Z': 3, 'Rwigs': 3.04},
            'Be': {'Z': 4, 'Rwigs': 2.27}, 'B': {'Z': 5, 'Rwigs': 1.96},
            'C': {'Z': 6, 'Rwigs': 1.66}, 'N': {'Z': 7, 'Rwigs': 1.90},
            'O': {'Z': 8, 'Rwigs': 1.90}, 'F': {'Z': 9, 'Rwigs': 2.17},
            'Ne': {'Z': 10, 'Rwigs': 2.89}, 'Na': {'Z': 11, 'Rwigs': 3.76},
            'Mg': {'Z': 12, 'Rwigs': 3.25}, 'Al': {'Z': 13, 'Rwigs': 2.95},
            'Si': {'Z': 14, 'Rwigs': 2.63}, 'P': {'Z': 15, 'Rwigs': 2.56},
            'S': {'Z': 16, 'Rwigs': 2.70}, 'Cl': {'Z': 17, 'Rwigs': 2.85},
            'Ar': {'Z': 18, 'Rwigs': 3.71}, 'K': {'Z': 19, 'Rwigs': 4.66},
            'Ca': {'Z': 20, 'Rwigs': 3.88}, 'Sc': {'Z': 21, 'Rwigs': 3.31},
            'Ti': {'Z': 22, 'Rwigs': 2.99}, 'V': {'Z': 23, 'Rwigs': 2.76},
            'Cr': {'Z': 24, 'Rwigs': 2.64}, 'Mn': {'Z': 25, 'Rwigs': 2.57},
            'Fe': {'Z': 26, 'Rwigs': 2.52}, 'Co': {'Z': 27, 'Rwigs': 2.52},
            'Ni': {'Z': 28, 'Rwigs': 2.55}, 'Cu': {'Z': 29, 'Rwigs': 2.62},
            'Zn': {'Z': 30, 'Rwigs': 2.78}, 'Ga': {'Z': 31, 'Rwigs': 2.75},
            'Ge': {'Z': 32, 'Rwigs': 2.79}, 'As': {'Z': 33, 'Rwigs': 2.83},
            'Se': {'Z': 34, 'Rwigs': 2.94}, 'Br': {'Z': 35, 'Rwigs': 3.13},
            'Kr': {'Z': 36, 'Rwigs': 4.32}, 'Rb': {'Z': 37, 'Rwigs': 4.95},
            'Sr': {'Z': 38, 'Rwigs': 4.22}, 'Y': {'Z': 39, 'Rwigs': 3.61},
            'Zr': {'Z': 40, 'Rwigs': 3.28}, 'Nb': {'Z': 41, 'Rwigs': 3.03},
            'Mo': {'Z': 42, 'Rwigs': 2.91}, 'Tc': {'Z': 43, 'Rwigs': 2.82},
            'Ru': {'Z': 44, 'Rwigs': 2.77}, 'Rh': {'Z': 45, 'Rwigs': 2.78},
            'Pd': {'Z': 46, 'Rwigs': 2.84}, 'Ag': {'Z': 47, 'Rwigs': 2.95},
            'Cd': {'Z': 48, 'Rwigs': 3.14}, 'In': {'Z': 49, 'Rwigs': 3.30},
            'Sn': {'Z': 50, 'Rwigs': 3.45}, 'Sb': {'Z': 51, 'Rwigs': 3.30},
            'Te': {'Z': 52, 'Rwigs': 3.31}, 'I': {'Z': 53, 'Rwigs': 3.50},
            'Xe': {'Z': 54, 'Rwigs': 4.31}, 'Cs': {'Z': 55, 'Rwigs': 5.30},
            'Ba': {'Z': 56, 'Rwigs': 4.20}, 'La': {'Z': 57, 'Rwigs': 3.91},
            'Ce': {'Z': 58, 'Rwigs': 3.80}, 'Pr': {'Z': 59, 'Rwigs': 3.75},
            'Nd': {'Z': 60, 'Rwigs': 3.70}, 'Pm': {'Z': 61, 'Rwigs': 3.65},
            'Sm': {'Z': 62, 'Rwigs': 3.60}, 'Eu': {'Z': 63, 'Rwigs': 3.55},
            'Gd': {'Z': 64, 'Rwigs': 3.52}, 'Tb': {'Z': 65, 'Rwigs': 3.61},
            'Dy': {'Z': 66, 'Rwigs': 3.67}, 'Ho': {'Z': 67, 'Rwigs': 3.70},
            'Er': {'Z': 68, 'Rwigs': 3.73}, 'Tm': {'Z': 69, 'Rwigs': 3.75},
            'Yb': {'Z': 70, 'Rwigs': 3.56}, 'Lu': {'Z': 71, 'Rwigs': 3.44},
            'Hf': {'Z': 72, 'Rwigs': 3.23}, 'Ta': {'Z': 73, 'Rwigs': 3.04},
            'W': {'Z': 74, 'Rwigs': 2.93}, 'Re': {'Z': 75, 'Rwigs': 2.86},
            'Os': {'Z': 76, 'Rwigs': 2.82}, 'Ir': {'Z': 77, 'Rwigs': 2.83},
            'Pt': {'Z': 78, 'Rwigs': 2.88}, 'Au': {'Z': 79, 'Rwigs': 2.98},
            'Hg': {'Z': 80, 'Rwigs': 3.27}, 'Tl': {'Z': 81, 'Rwigs': 3.57},
            'Pb': {'Z': 82, 'Rwigs': 3.62}, 'Bi': {'Z': 83, 'Rwigs': 3.37},
            'Po': {'Z': 84, 'Rwigs': 3.46}, 'At': {'Z': 85, 'Rwigs': 3.63},
            'Rn': {'Z': 86, 'Rwigs': 4.44}, 'Fr': {'Z': 87, 'Rwigs': 5.81},
            'Ra': {'Z': 88, 'Rwigs': 4.30}, 'Ac': {'Z': 89, 'Rwigs': 3.84},
            'Th': {'Z': 90, 'Rwigs': 3.52}, 'Pa': {'Z': 91, 'Rwigs': 3.32},
            'U': {'Z': 92, 'Rwigs': 3.13}, 'Np': {'Z': 93, 'Rwigs': 3.02},
            'Pu': {'Z': 94, 'Rwigs': 2.96}, 'Am': {'Z': 95, 'Rwigs': 2.93},
            'Cm': {'Z': 96, 'Rwigs': 2.93}, 'Bk': {'Z': 97, 'Rwigs': 2.95},
            'Cf': {'Z': 98, 'Rwigs': 2.99}, 'Es': {'Z': 99, 'Rwigs': 3.05},
            'Fm': {'Z': 100, 'Rwigs': 3.17}, 'Md': {'Z': 101, 'Rwigs': 0.000},
            'No': {'Z': 102, 'Rwigs': 0.000}, 'Lr': {'Z': 103, 'Rwigs': 3.500}}

REFERENCE = {"Fe": -8.30986305725147, "Co": -7.10646786208887,
             "Mn": -9.04116583023117, "Ni": -5.57058693907496,
             "Cr": -9.64529903086873, "V": -9.08055004986443,
             "Ti": -7.89042111815724, "Cu": -3.71797397606303,
             "Zn": -1.26775730145801, "Ga": -3.0281282763815,
             "Ge": -4.62163453127987, "In": -3.18887807809515,
             "Sn": -4.00527149401934, "Pd": -5.18089045007217,
             "Rh": -7.26929051746743, "Pt": -6.05335455763213,
             "Ru": -9.20388484292648, "Nb": -10.0945900627376,
             "Zr": -8.54761937261647, "Al": -3.74129357979325,
             "Si": -5.42476168374865, "Sb": -4.12207679803694,
             "Pb": -3.70719513700551, "N": -8.31608161824619,
             "B": -6.67811265223554, "C": -9.1094663584899,
             "F": -1.85748416912446, "P": -5.37439133969137,
             "S": -4.25214836550994, "Cl": -1.78700714451757}

POT_DICT = {'Vac': 'non', 'H': 'H', 'He': 'non', 'Li': 'Li_sv', 'Be': 'Be',
            'B': 'B', 'C': 'C', 'N': 'N', 'O': 'O', 'F': 'F', 'Ne': 'non',
            'Na': 'Na_pv', 'Mg': 'Mg', 'Al': 'Al', 'Si': 'Si', 'P': 'P',
            'S': 'S', 'Cl': 'Cl', 'Ar': 'non', 'K': 'K_sv', 'Ca': 'Ca_pv',
            'Sc': 'Sc_sv', 'Ti': 'Ti_pv', 'V': 'V_pv', 'Cr': 'Cr_pv',
            'Mn': 'Mn', 'Fe': 'Fe', 'Co': 'Co', 'Ni': 'Ni', 'Cu': 'Cu',
            'Zn': 'Zn', 'Ga': 'Ga_d', 'Ge': 'Ge_d', 'As': 'As', 'Se': 'Se',
            'Br': 'Br', 'Kr': 'non', 'Rb': 'Rb_sv', 'Sr': 'Sr_sv',
            'Y': 'Y_sv', 'Zr': 'Zr_sv', 'Nb': 'Nb_pv', 'Mo': 'Mo_pv',
            'Tc': 'Tc_pv', 'Ru': 'Ru', 'Rh': 'Rh', 'Pd': 'Pd', 'Ag': 'Ag',
            'Cd': 'Cd', 'In': 'In_d', 'Sn': 'Sn_d', 'Sb': 'Sb', 'Te': 'Te',
            'I': 'I', 'Xe': 'non', 'Cs': 'Cs_sv', 'Ba': 'Ba_sv',
            'La': 'non', 'Ce': 'non', 'Pr': 'non', 'Nd': 'non',
            'Pm': 'non', 'Sm': 'non', 'Eu': 'non', 'Gd': 'non',
            'Tb': 'non', 'Dy': 'non', 'Ho': 'non', 'Er': 'non',
            'Tm': 'non', 'Yb': 'non', 'Lu': 'non', 'Hf': 'Hf_pv',
            'Ta': 'Ta_pv', 'W': 'W_pv', 'Re': 'Re', 'Os': 'Os_pv',
            'Ir': 'Ir', 'Pt': 'Pt', 'Au': 'Au', 'Hg': 'Hg', 'Tl': 'Tl_d',
            'Pb': 'Pb_d', 'Bi': 'Bi_d', 'Po': 'non', 'At': 'non'}
