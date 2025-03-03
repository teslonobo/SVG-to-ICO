import os
from io import BytesIO

import cairosvg
from PIL import Image

class SVG2ICO:
    """ Convert SVGS to ICO files with ease."""
    HEIGHT = 256
    WIDTH = 256
    def __init__(self, file_path:str, output_path:str, size: tuple[int,int]|tuple[None,None]=(None,None), verbose:bool=True):
        """
        Args:
            file_path(str): File path of SVG file.
            output_path(str): Output directory to save ICO file to.
            size(tuple(int,int)|tuple(None,None)):Defaults to (250,250).
            verbose: Prints to info. Defaults to True.
        """
        self.file = file_path
        self.out_dir = output_path
        self.v = verbose
        self.check_paths()
        self.out_fn = os.path.join(self.out_dir,os.path.basename(self.file).replace('.svg', '.ico'))
        self.HEIGHT = size[0] if size[0] is not None else self.HEIGHT
        self.WIDTH = size[1] if size[1] is not None else self.WIDTH

    def check_paths(self):
        """ Interal Check for file/directories existance """
        if not os.path.exists(self.file):
            raise FileNotFoundError(f"[!] The file or directory '{self.file}' does not exist.")
        if not os.path.exists(self.out_dir):
            raise FileNotFoundError(f"[!] The directory '{self.out_dir}' does not exist.")
    def svg_to_png_bytes(self)->bytes:
        """ Internal function to read/extract byte data.

        Returns:
            bytes
        """
        try:
            with open(self.file,'rb') as svg_bytes:
                png_bytes = cairosvg.svg2png(bytestring=svg_bytes.read(),output_height=self.HEIGHT,output_width=self.WIDTH)
                return png_bytes
        except PermissionError:
            raise PermissionError('[!] Might not have permissions to this directory.')

    def save_ico(self):
        """ Save as an ICO after initializing the SVG2ICO class"""
        png_bytes = self.svg_to_png_bytes()
        if not os.path.isfile(self.out_fn):
            try:
                with BytesIO(png_bytes) as data:
                    img = Image.open(data)
                    img.save(self.out_fn, format='ICO', sizes=[(self.HEIGHT, self.WIDTH)])
            except Exception as exc:
                raise exc(f"[!] Error Occured: {exc}")
            if self.v:
                print(f'[+] Created {os.path.basename(self.out_fn)} in {os.path.basename(self.out_dir)}')
        else:
            if self.v:
                print(f'[!] File already exist {self.out_fn}')