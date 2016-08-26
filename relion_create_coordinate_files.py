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
import math

from pyrelion import MetaData
import argparse


class CreateCoordinateFiles():
    def define_parser(self):
        self.parser = argparse.ArgumentParser(
            description="Creates particle coordinate STAR files for repicking."
                        "Warning: this script will add to existing files.")
        add = self.parser.add_argument
        add('input_star', help="Input STAR filename with particles and micrograph names.")
        add('--suffix', help="Suffix to be added to the coordinate filenames (default \"repick\").")


    def usage(self):
        self.parser.print_help()


    def error(self, *msgs):
        self.usage()
        print "Error: " + '\n'.join(msgs)
        print " "
        sys.exit(2)

    def main(self):

        self.define_parser()
        args = self.parser.parse_args()

        if len(sys.argv) == 1:
            self.error("No input particles STAR file given.")


        print "Creating coordinate files..."

        md = MetaData(args.input_star)

        for particle in md:
           coordinates_file = os.path.splitext(particle.rlnMicrographName)[0] + "_" + args.suffix + ".star"

           if "rlnOriginX" in md.getLabels():
               particle.rlnCoordinateX = int(particle.rlnCoordinateX - particle.rlnOriginX)
           if "rlnOriginY" in md.getLabels():
               particle.rlnCoordinateY = int(particle.rlnCoordinateY - particle.rlnOriginY)

           if not os.path.isfile(coordinates_file):
               star = open(coordinates_file, "a")
               star.write("\n")
               star.write("data_images\n")
               star.write("\n")
               star.write("loop_\n")
               star.write("_rlnMicrographName #1\n")
               star.write("_rlnCoordinateX #2\n")
               star.write("_rlnCoordinateY #3\n")
               if "rlnAnglePsi" in md.getLabels():
                   star.write("_rlnAnglePsi #4\n")
               if "rlnAnglePsiPrior" in md.getLabels():
                   star.write("_rlnAnglePsiPrior #5\n")
               star.close()

           if os.path.isfile(coordinates_file):
               star = open(coordinates_file, "a")
               star.write("%s\t%f\t%f\t" % (
                  os.path.basename(particle.rlnMicrographName),
                  particle.rlnCoordinateX,
                  particle.rlnCoordinateY))
               if "rlnAnglePsi" in md.getLabels():
                   star.write("%f\t" % (particle.rlnAnglePsi))
               if "rlnAnglePsiPrior" in md.getLabels():
                   star.write("%f\t" % (particle.rlnAnglePsiPrior))
               star.write("\n")
               star.close()


if __name__ == "__main__":
    CreateCoordinateFiles().main()
