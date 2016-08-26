#!/usr/bin/env python

# **************************************************************************
# *
# * Author:  Juha T. Huiskonen (juha@strubi.ox.ac.uk)
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
# **************************************************************************

import os
import sys

from pyrelion import MetaData
import argparse
import math


class AdjustParticlesFromClassaverages():
    def define_parser(self):
        self.parser = argparse.ArgumentParser(
            description="Allows modifying origins and orientations of all particles in class.")
        add = self.parser.add_argument
        add('input_star', help="Input STAR filename with particles.")
        add('--classes', help="Classes STAR filename with additional shifts are rotations for each class.")
        add('--output', help="Output STAR filename.")
        add('--size', type=int, default=0, help="Particle box size (pixels).")

    def angles_to_radians(self, particle, labels):
        """ Convert the particle angles to radians. """
        if "rlnAnglePsi" in labels:
            particle.rlnAnglePsi = math.radians(particle.rlnAnglePsi)
        if "rlnAngleTilt" in labels:
            particle.rlnAngleTilt = math.radians(particle.rlnAngleTilt)
        if "rlnAngleRot" in labels:
            particle.rlnAngleRot = math.radians(particle.rlnAngleRot)
        if "rlnAnglePsiPrior" in labels:
            particle.rlnAnglePsi = math.radians(particle.rlnAnglePsiPrior)
        if "rlnAngleTiltPrior" in labels:
            particle.rlnAngleTilt = math.radians(particle.rlnAngleTiltPrior)
        if "rlnAngleRotPrior" in labels:
            particle.rlnAngleRot = math.radians(particle.rlnAngleRotPrior)

    def angles_to_degrees(self, particle, labels):
        """ Convert the particle angles to radians. """
        if "rlnAnglePsi" in labels:
            particle.rlnAnglePsi = math.degrees(particle.rlnAnglePsi)
        if "rlnAngleTilt" in labels:
            particle.rlnAngleTilt = math.degrees(particle.rlnAngleTilt)
        if "rlnAngleRot" in labels:
            particle.rlnAngleRot = math.degrees(particle.rlnAngleRot)
        if "rlnAnglePsiPrior" in labels:
            particle.rlnAnglePsi = math.degrees(particle.rlnAnglePsiPrior)
        if "rlnAngleTiltPrior" in labels:
            particle.rlnAngleTilt = math.degrees(particle.rlnAngleTiltPrior)
        if "rlnAngleRotPrior" in labels:
            particle.rlnAngleRot = math.degrees(particle.rlnAngleRotPrior)


    #def validate(self, args):
    #    if len(sys.argv) == 1:
    #        self.error("Error: No input file given.")
    #
    #    if not os.path.exists(args.input_star):
    #        self.error("Error: Input file '%s' not found."
    #                   % args.input_star)


    def main(self):

        self.define_parser()
        args = self.parser.parse_args()

        #self.validate(args)

        md = MetaData(args.input_star)
        mdOut = MetaData()
        mdOut.addLabels(md.getLabels())
        cl = MetaData(args.classes)
        particle_halfsize = args.size/2

        particles_out = []

        for reference in cl:
            self.angles_to_radians(reference, cl.getLabels())

        for i, particle in enumerate(md):
            self.angles_to_radians(particle, md.getLabels())

            print "doing particle %s" % i

            referenceOriginX = 0
            referenceOriginY = 0

            # search for the right reference for this particle
            for reference in cl:
                if reference.rlnClassNumber == particle.rlnClassNumber:
                    referenceOriginX = reference.rlnCoordinateX - particle_halfsize
                    referenceOriginY = reference.rlnCoordinateY - particle_halfsize
                    psi = particle.rlnAnglePsi
                    particle.rlnOriginX = particle.rlnOriginX - (referenceOriginX * math.cos(-psi)
                                                                  - referenceOriginY * math.sin(-psi))
                    particle.rlnOriginY = particle.rlnOriginY - (referenceOriginY * math.cos(-psi)
                                                                  + referenceOriginX * math.sin(-psi))
                    if "rlnAngleRot" in cl.getLabels():
                        particle.rlnAngleRot = particle.rlnAngleRot + reference.rlnAngleRot
                    if "rlnAngleTilt" in cl.getLabels():
                        particle.rlnAngleTilt = particle.rlnAngleTilt + reference.rlnAngleTilt
                    if "rlnAnglePsi" in cl.getLabels():
                        particle.rlnAnglePsi = particle.rlnAnglePsi + reference.rlnAnglePsi

                    particles_out.append(particle)
                    break

            self.angles_to_degrees(particle, md)

        mdOut.addData(particles_out)
        mdOut.write(args.output)


if __name__ == "__main__":
    AdjustParticlesFromClassaverages().main()