import shlex
import argparse
from src import ObjFile
import sys
import os
import glob

def main(new_argv):
    # sys.argv = [new_argv.split()[0]] + new_argv.split()[1:]
    parser = argparse.ArgumentParser(description="Obj to png using MatPlotLib")

    parser = argparse.ArgumentParser(description="Obj to png using MatPlotLib")

    parser.add_argument(
        "-i",
        "--indir",
        dest="objdir",
        help="Directory containing .obj files to be converted to png",
    )

    parser.add_argument(
        "-o",
        "--outdir",
        dest="outdir",
        help="Output directory for converted png files",
    )

    parser.add_argument(
        "-a",
        "--azimuth",
        dest="azim",
        type=float,
        default=-90,
        help="Azimuth angle of view in degrees.",
    )

    parser.add_argument(
        "-e",
        "--elevation",
        dest="elevation",
        type=float,
        default=90,
        help="Elevation angle of view in degrees.",
    )

    parser.add_argument(
        "-q",
        "--quality",
        dest="quality",
        help="Image quality (HIGH,MEDIUM,LOW).  Default: LOW",
    )

    parser.add_argument(
        "--resolution",
        dest="resolution",
        help="Image resolution, takes precedence over quality argument. For example 640x480",
    )

    parser.add_argument(
        "-s",
        "--scale",
        dest="scale",
        type=float,
        help="Scale picture by decreasing boundaries. Lower than 1. gives a larger object.",
    )

    args = parser.parse_args(new_argv)
    args.azim = -90
    args.elevation = 90

    objdir = args.objdir
    outdir = args.outdir
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    res = {"HIGH": 1200, "MEDIUM": 600, "LOW": 300}
    dpi = None
    if args.quality:
        if type(args.quality) == int:
            dpi = args.quality
        elif args.quality.upper() in res:
            dpi = res[args.quality.upper()]

    width = dpi
    height = dpi
    if args.resolution:
        width, height = args.resolution.split("x")
        width = int(width)
        height = int(height)

    azim = args.azim
    elevation = args.elevation
    scale = args.scale

    for objfile in glob.glob(os.path.join(objdir, "*.obj")):
        outfile = os.path.join(outdir, os.path.basename(objfile).replace(".obj", ".png"))
        print("Converting %s to %s" % (objfile, outfile))
        ob = ObjFile.ObjFile(objfile)
        ob.Plot(
            outfile,
            elevation=elevation,
            azim=azim,
            width=width,
            height=height,
            scale=scale,
        )


def call(cmd):
    new_argv = []
    new_argv.extend(shlex.split(cmd))
    # new_argv = shlex.split(cmd)
    main(new_argv)

# def convert_obj_to_png(cmd):
#     sys.argv = [cmd.split()[0]] + cmd.split()[1:]
#
#     parser = argparse.ArgumentParser(description="Obj to png using MatPlotLib")
#
#     parser.add_argument(
#         "-i",
#         "--indir",
#         dest="objdir",
#         help="Directory containing .obj files to be converted to png",
#     )
#
#     parser.add_argument(
#         "-o",
#         "--outdir",
#         dest="outdir",
#         help="Output directory for converted png files",
#     )
#
#     parser.add_argument(
#         "-a",
#         "--azimuth",
#         dest="azim",
#         type=float,
#         help="Azimuth angle of view in degrees.",
#     )
#
#     parser.add_argument(
#         "-e",
#         "--elevation",
#         dest="elevation",
#         type=float,
#         help="Elevation angle of view in degrees.",
#     )
#
#     parser.add_argument(
#         "-q",
#         "--quality",
#         dest="quality",
#         help="Image quality (HIGH,MEDIUM,LOW).  Default: LOW",
#     )
#
#     parser.add_argument(
#         "--resolution",
#         dest="resolution",
#         help="Image resolution, takes precedence over quality argument. For example 640x480",
#     )
#
#     parser.add_argument(
#         "-s",
#         "--scale",
#         dest="scale",
#         type=float,
#         help="Scale picture by decreasing boundaries. Lower than 1. gives a larger object.",
#     )
#
#     args = parser.parse_args()
#     args.azim = -90
#     args.elevation = 90
#
#     objdir = args.objdir
#     outdir = args.outdir
#     if not os.path.exists(outdir):
#         os.makedirs(outdir)
#
#     res = {"HIGH": 1200, "MEDIUM": 600, "LOW": 300}
#     dpi = None
#     if args.quality:
#         if type(args.quality) == int:
#             dpi = args.quality
#         elif args.quality.upper() in res:
#             dpi = res[args.quality.upper()]
#
#     width = dpi
#     height = dpi
#     if args.resolution:
#         width, height = args.resolution.split("x")
#         width = int(width)
#         height = int(height)
#
#     azim = args.azim
#     elevation = args.elevation
#     scale = args.scale
#
#     for objfile in glob.glob(os.path.join(objdir, "*.obj")):
#         outfile = os.path.join(outdir, os.path.basename(objfile).replace(".obj", ".png"))
#         print("Converting %s to %s" % (objfile, outfile))
#         ob = ObjFile.ObjFile(objfile)
#         ob.Plot(
#             outfile,
#             elevation=elevation,
#             azim=azim,
#             width=width,
#             height=height,
#             scale=scale,
#         )

if __name__ == "__main__":
    command = r"-i D:\happyelements\obj2png\test_obj -o D:\happyelements\obj2png\test_png"
    call(command)