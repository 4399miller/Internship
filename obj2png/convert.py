import argparse
from src import ObjFile
import sys
import os
import glob

def convert_obj_to_png(cmd):
    new_argv = cmd.split()

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
        default=95,
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
        print(f"Using resolution: {width}x{height}")

    elevation = args.elevation
    scale = args.scale

    for objfile in glob.glob(os.path.join(objdir, "*.obj")):
        outfile = os.path.join(outdir, os.path.basename(objfile).replace(".obj", ".png"))
        print("Converting %s to %s" % (objfile, outfile))
        ob = ObjFile.ObjFile(objfile)
        ob.Plot(
            outfile,
            elevation=elevation,
            azim=args.azim,  
            width=width,
            height=height,
            scale=scale,
        )


def run_convertion(from_dir, to_dir, azimuth = -90, elevation = 95, resolution = "512x512"):
    command = f"-i {from_dir} -o {to_dir} -a {azimuth} -e {elevation} --resolution {resolution}"
    convert_obj_to_png(command)


if __name__ == "__main__":
    run_convertion("D:\\happyelements\\obj2png\\test_obj" ,"D:\\happyelements\\obj2png\\test_png")