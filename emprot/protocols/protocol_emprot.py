# **************************************************************************
# *
# * Authors:   Blanca Pueche (blanca.pueche@cnb.csis.es)
# *
# * Unidad de  Bioinformatica of Centro Nacional de Biotecnologia , CSIC
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
import json
import shutil

import os
import pyworkflow.protocol.params as params
from pyworkflow.protocol.constants import LEVEL_ADVANCED
from pwem.protocols import EMProtocol
from pyworkflow.object import String

from emprot.__init__ import Plugin
from pwem.objects.data import AtomStruct

from emprot import EMPROT_DIC


class ProtEMProt(EMProtocol):
    """
    Protocol to use EMProt model.
    """
    _label = 'EMProt protein modelling'

    # -------------------------- DEFINE param functions ----------------------
    def _defineParams(self, form):
        """ Define the input parameters that will be used.
        Params:
            form: this is the form to be populated with sections and params.
        """
        form.addHidden('useGpu', params.BooleanParam, default=True,
                       label="Use GPU for execution",
                       help="This protocol has both CPU and GPU implementation. Choose one.")

        form.addHidden('gpuList', params.StringParam, default='0',
                       label="Choose GPU IDs",
                       help="Comma-separated GPU devices that can be used.")


        form.addSection(label='Input')
        form.addParam('inputVolume', params.PointerParam, allowsNull=False,
                      pointerClass='Volume',
                      label="Input volume: ",
                      help='Select the electron map of the structure in MRC2014')

        form.addParam('resolution', params.FloatParam,
                      default=0.0,
                      label='Resolution: ',
                      help='Map resolution.')

        form.addParam('inputSeq', params.PointerParam, allowsNull=True,
                      pointerClass="Sequence",
                      label="Input Sequence: ",
                      help="Input sequence file.")

        form.addParam('inputStructure', params.PointerParam, allowsNull=True,
                      pointerClass='AtomStruct',
                      label="Input predicted model: ",
                      help='Select the predicted model.')

        form.addParam('fast', params.BooleanParam, default=False,
                       label="Fast mode: ",
                       help="Use when structures have >30000 aminoacids.")


        form.addParallelSection(threads=4, mpi=1)

    # --------------------------- STEPS functions ------------------------------
    def _insertAllSteps(self):
        self._insertFunctionStep(self.runEMProtStep)
        self._insertFunctionStep(self.createOutputStep)


    def runEMProtStep(self):
        args = []
        args.extend([
            "--map", str(os.path.abspath(self.inputVolume.get().getFileName())),
            "--output", str(os.path.abspath(self._getExtraPath()))
        ])

        if self.inputSeq.get() is not None:
            args.append(f"--seq {str(os.path.abspath(self.inputSeq.get().getFileName()))}")
        if self.inputStructure.get() is not None:
            args.append(f"--complex {str(os.path.abspath(self.inputStructure.get().getFileName()))}")

        if self.resolution.get() != 0.0:
            args.append(f' --resolution {self.resolution.get()}')
        if self.useGpu.get():
            args.append(f'--device {self.gpuList.get()}')
        else:
            args.append(f'--nt {self.numberOfThreads.get()}')
        if self.fast.get():
            args.append(f'--fast')

        Plugin.runCondaCommand(
            self,
            args=" ".join(args),
            condaDic=EMPROT_DIC,
            program="emprot build",
            cwd=os.path.abspath(Plugin.getVar(EMPROT_DIC['home']))
        )

    def createOutputStep(self):
        outDir = (self._getExtraPath())

        finalOutput = os.path.join(outDir, 'output_fit.cif')
        bestStruct = AtomStruct(filename=finalOutput)

        self._defineOutputs(
            outputAtomStruct=bestStruct
        )



    # --------------------------- INFO functions -----------------------------------
    def _summary(self):
        summary = ["Two additional models have been created in the extra folder. \n"
                   "output_denovo.cif: de novo model.\n"
                   "output_fit.cif: fitted model."]
        return summary

    def _methods(self):
        methods = []
        return methods

    def _validate(self):
        validations = []
        return validations

    def _warnings(self):
        warnings = []
        return warnings

    # --------------------------- UTILS functions -----------------------------------

