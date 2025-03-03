""" Script for cli interface"""
from argparse import ArgumentParser, RawDescriptionHelpFormatter

from svg_ico import SVG2ICO, os

def main():
    pgn = 'svg2ico'

    pgmDescript = """SVG to ICO conversion made easy, a few commands and done.\n
    Example: svg2ico -f assets/demo_svg/Firefox.svg -o assets/demo_icons -w 100 -ht 100 -v
    Example: svg2ico -fd assets/demo_svg -o assets/demo_icons
    """
    pgmu = 'svg2ico -f {filepath} -o {outpath} -w [100] -ht [100]'

    # Main parser
    parser = ArgumentParser(prog=pgn, usage=pgmu, description=pgmDescript, formatter_class=RawDescriptionHelpFormatter)

    # Add arguments to parser
    parser.add_argument('-f', metavar='--f', help='File path of the SVG file.', type=str)
    parser.add_argument('-fd', metavar='--fd', help='File directory of the SVG files.', type=str)
    parser.add_argument('-o', metavar='--o', help='Output file path for ICO file.', type=str)
    parser.add_argument('-w', metavar='--w', help='Width of SVG to set byte data in ICO file. Defaults to 250.', type=int, default=None)
    parser.add_argument('-ht', metavar='--ht', help='Height of SVG to set byte data in ICO file. Defaults to 250.', type=int, default=None)
    parser.add_argument('-v', action='store_false', help='Disable verbose mode. Defaults to True.')

    # Parse arguments
    args = parser.parse_args()

    # Run the conversion process
    if args.f and args.o:
        if os.path.basename(args.f).split('.')[-1] != 'svg':
            print('Can only pass SVG file/files.')
        else:
            SVG2ICO(file_path=args.f, output_path=args.o, size=(args.w, args.ht), verbose=args.v).save_ico()
    elif args.fd and args.o:
        files = [os.path.join(args.fd, f) for f in os.listdir(args.fd)]
        for f in files:
            SVG2ICO(file_path=f, output_path=args.o, size=(args.w, args.ht), verbose=args.v).save_ico()
    else:
        print("Both input and output file paths are required.")
