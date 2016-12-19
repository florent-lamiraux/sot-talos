# -*- coding: utf-8 -*-
# Copyright 2016, Olivier STASSE, LAAS-CNRS
#
# This file is part of TALOSController.
# TALOSController is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# TALOSController is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Lesser Public License for more details.  You should have
# received a copy of the GNU Lesser General Public License along with
# TALOSController. If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

import numpy as np
from dynamic_graph.sot.core import \
    FeatureGeneric, FeatureJointLimits, Task, Constraint, GainAdaptive, SOT
from dynamic_graph.sot.dynamics import AngleEstimator
from dynamic_graph import enableTrace, plug

from dynamic_graph.sot.dynamics.humanoid_robot import AbstractHumanoidRobot

# Internal helper tool.
def matrixToTuple(M):
    tmp = M.tolist()
    res = []
    for i in tmp:
        res.append(tuple(i))
    return tuple(res)

class Talos(AbstractHumanoidRobot):
    """
    This class instanciates a Talos robot
    """

    forceSensorInLeftAnkle =  ((1.,0.,0.,0.),
                               (0.,1.,0.,0.),
                               (0.,0.,1.,-0.105),
                               (0.,0.,0.,1.))
    forceSensorInRightAnkle = ((1.,0.,0.,0.),
                               (0.,1.,0.,0.),
                               (0.,0.,1.,-0.105),
                               (0.,0.,0.,1.))

    accelerometerPosition = np.matrix ((
            (1., 0., 0., -.13,),
            (0., 1., 0., 0.,),
            (0., 0., 1., .118,),
            (0., 0., 0., 1.,),
            ))

    gyrometerPosition = np.matrix ((
            (1., 0., 0., -.13,),
            (0., 1., 0., 0.,),
            (0., 0., 1., .118,),
            (0., 0., 0., 1.,),
            ))

    def smallToFull(self, config):
        res = (config + 10*(0.,))
        return res

    def __init__(self, name, modelDir, xmlDir, device, dynamicType,
                 tracer = None):
        AbstractHumanoidRobot.__init__ (self, name, tracer)

        self.OperationalPoints.append('waist')
        self.OperationalPoints.append('chest')
        self.device = device
        self.modelDir = modelDir
        self.modelName = 'talos.wrl'
        self.specificitiesPath = xmlDir + '/TALOSSpecificitiesSmall.xml'
        self.jointRankPath = xmlDir + '/TALOSLinkJointRankSmall.xml'

        self.AdditionalFrames.append(
            ("accelerometer",
             matrixToTuple(self.accelerometerPosition), "chest"))
        self.AdditionalFrames.append(
            ("gyrometer",
             matrixToTuple(self.gyrometerPosition), "chest"))
        self.AdditionalFrames.append(
            ("leftFootForceSensor",
             self.forceSensorInLeftAnkle, "left-ankle"))
        self.AdditionalFrames.append(
            ("rightFootForceSensor",
            self.forceSensorInRightAnkle, "right-ankle"))

        self.dynamic = self.loadModelFromJrlDynamics(
            self.name + '_dynamic',
            modelDir,
            self.modelName,
            self.specificitiesPath,
            self.jointRankPath,
            dynamicType)

        self.dimension = self.dynamic.getDimension()
        
        self.plugVelocityFromDevice = True

        if self.dimension != len(self.halfSitting):
            raise RuntimeError("Dimension of half-sitting: {0} differs from dimension of robot: {1}".format (len(self.halfSitting), self.dimension))
        self.initializeRobot()

__all__ = [Talos]
