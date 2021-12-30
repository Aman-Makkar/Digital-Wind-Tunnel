# CAD conversion script - written in Python 3.6.
# FreeCad version 0.18 has been used.
# Reference: freecad_convert/freecad_convert.py at 96c416f4bf3f317fc73701400864b5f2741e19e0 · faerietree/freecad_convert. (n.d.). Retrieved December 26, 2020, 
# from https://github.com/faerietree/freecad_convert/blob/96c416f4bf3f317fc73701400864b5f2741e19e0/freecad_convert.py

FREECAD_PATH = 'C:\\Program Files\\FreeCAD 0.18\\bin'  # path to the FreeCAD.pyd file

import sys
sys.path.append(FREECAD_PATH)   # This is necessary in order for python to find FREECAD
import os
import time
import FreeCAD
import Part
import Mesh

mesh_formats = ['.stl']


class ConvertorClass:
    """Class to convert CAD file formats"""
    def __init__(self):
        try:
            self.in_file = sys.argv[1]      # input filename and format
            self.out_file = sys.argv[2]     # output filename and format
        except IndexError:
            raise SystemExit(self.publish_help_screen())

    def convertor(self):
        """
        Conversion method, all the CAD file conversion take place through this method.
        """
        while len(sys.argv) == 3:
            try:
                # Splitting the path into a pair, root and ext - ext is the extension part of the file,
                # the root part is everything else in the path
                in_filename, in_ext = os.path.splitext(self.in_file)
                out_filename, out_ext = os.path.splitext(self.out_file)
                print(f"{in_ext} -> {out_ext}")

                # Calling the shape function from Part
                shape = Part.Shape()
                # Checking if the input file is in the mesh_formats list
                if in_ext in mesh_formats:
                    print("Mesh file: ", self.in_file)
                    Mesh.open(self.in_file)
                    freecad_document = FreeCAD.getDocument("Unnamed").findObjects()[0]
                    # Checking if the requested output file is in the mesh_formats list
                    if out_ext in mesh_formats:
                        tic = time.time()
                        print(f"Converting to a mesh file: {self.out_file}")
                        Mesh.export([freecad_document], self.out_file)
                        toc = time.time()
                        print(f"Converted the CAD model in {toc - tic:0.10f} seconds")
                        exit()
                    else:
                        # Setting the meshing tolerance, this can be changed depending on the requirements
                        # and convert to a part file from a mesh file format.
                        tic = time.time()
                        shape.makeShapeFromMesh(freecad_document.Mesh.Topology, 0.01)
                        self.part_convertor(shape, self.out_file, out_ext)
                        toc = time.time()
                        print(f"Converted the CAD model in {toc - tic:0.10f} seconds")
                        exit()
                # Checking if it is converting one part file to another i.e stp to igs for example
                else:
                    tic = time.time()
                    print(f"Opening a part file: {self.in_file}")
                    shape.read(self.in_file)
                    self.part_convertor(shape, self.out_file, out_ext)
                    toc = time.time()
                    print(f"Converted the CAD model in {toc - tic:0.10f} seconds")
                    exit()

            except IndexError:
                raise SystemExit(self.publish_help_screen())
        else:
            self.publish_help_screen()
            exit()

    @staticmethod
    def part_convertor(shape, out_file, out_ext):
        """Method to convert CAD part formats."""
        if out_ext == '.stp':
            print(f"Exporting to part file: {out_file}")
            shape.exportStep(out_file)
        elif out_ext == '.igs':
            print(f"Exporting to part file: {out_file}")
            shape.exportIges(out_file)
        elif out_ext == '.brp':
            print(f"Exporting to part file: {out_file}")
            shape.exportBrep(out_file)
        elif out_ext == '.stl':
            print(f"Exporting to a mesh file: {out_file}")
            shape.exportStl(out_file, 0.01)     # The second parameter is surface deviation
        else:
            print(f"Exporting to {out_ext} is not supported.")

    @staticmethod
    def publish_help_screen():
        """Help screen to show the usage of the program."""
        print("Usage:\n")
        print("<convertor.py> <input filename.ext> <output filename.ext>")
        print("\n")
        print("Example: main.py input.stp output.igs\n")


# This imports the script without running it.
if __name__ == '__main__':
    run_convertor = ConvertorClass()
    run_convertor.convertor()
