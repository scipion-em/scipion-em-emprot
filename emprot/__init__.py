# **************************************************************************
# *
# * Authors:     Blanca Pueche (blanca.pueche@cnb.csic.es)
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

from os.path import join, exists

import pwem
from scipion.install.funcs import InstallHelper

from pyworkflow import SPA, TOMO, MODELLING
from .constants import EMPROT_DIC


_version_ = '0.1'
_logo = ""
_references = ['']




class Plugin(pwem.Plugin):
    _homeVar = EMPROT_DIC['home']
    _pathVars = [EMPROT_DIC['home']]
    _supportedVersions = [EMPROT_DIC['version']]

    @classmethod
    def _defineVariables(cls):
        """ Return and write a variable in the config file.
        """
        cls._defineEmVar(EMPROT_DIC['home'], EMPROT_DIC['name'] + '-' + EMPROT_DIC['version'])

    @classmethod
    def defineBinaries(cls, env, default=True):
        installer = InstallHelper(EMPROT_DIC['name'],
                                  packageHome=cls.getVar(EMPROT_DIC['home']),
                                  packageVersion=EMPROT_DIC['version'])

        installer.addCommand(
            "git clone https://github.com/huang-laboratory/EMProt.git",
            f"{EMPROT_DIC['name']}_cloned"
        ).addCommand(
            f"cd EMProt && conda env create -f environment.yml -n {EMPROT_DIC['name']}-{EMPROT_DIC['version']}",
            f"{EMPROT_DIC['name']}_env_created"
        ).addCommand(
            f"cd EMProt && conda run -n {EMPROT_DIC['name']}-{EMPROT_DIC['version']} pip install -e . && touch ../emprot_installed",
            f"{EMPROT_DIC['name']}_installed"
        ).addCommand(
            # Download pretrained weights
            f"cd EMProt/emprot && "
            "wget http://huanglab.phys.hust.edu.cn/EMProt/pretrained_weights/weights.tgz && "
            "tar -zxvf weights.tgz && "
            "rm -f weights.tgz",
            f"{EMPROT_DIC['name']}_weights_downloaded"
        )

        installer.addPackage(
            env,
            dependencies=['conda', 'pip', 'git'],
            default=default
        )

    @classmethod
    def getEnvName(cls, packageDictionary):
        """ This function returns the name of the conda enviroment for a given package. """
        return '{}-{}'.format(packageDictionary['name'], packageDictionary['version'])

    @classmethod
    def getEnvActivationCommand(cls, packageDictionary, condaHook=True):
        """ This function returns the conda enviroment activation command for a given package. """
        return '{}conda activate {}'.format(cls.getCondaActivationCmd() if condaHook else '',
                                            cls.getEnvName(packageDictionary))

    @classmethod
    def runCondaCommand(cls, protocol, args, condaDic, program, cwd=None, popen=False, silent=True, retOut=False):
        """ General function to run conda commands """
        result = None
        fullProgram = f'{cls.getEnvActivationCommand(condaDic)} && {program} '
        if not popen and not retOut:
            protocol.runJob(fullProgram, args, env=cls.getEnviron(), cwd=cwd, numberOfThreads=1)
        else:
            if not retOut:
                kwargs = {}
                if silent:
                    kwargs = {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}
                run(fullProgram + args, env=cls.getEnviron(), cwd=cwd, shell=True, **kwargs)
            else:
                result = subprocess.check_output(fullProgram + args, cwd=cwd, shell=True, text=True)
        return result


