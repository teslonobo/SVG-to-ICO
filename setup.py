import os, winreg, logging

logging.basicConfig(filename='setup_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PathWriter:
    cu = winreg.HKEY_CURRENT_USER
    root = winreg.HKEY_CLASSES_ROOT
    env = r'Environment'

    def __init__(self, file_path:str, bat_file:str|None=None, context:str='convert here', icon:str|None=None):
        self.exe_file = os.path.abspath(os.path.normpath(file_path))
        self.path = self.parse_exe_directory(self.exe_file)
        self.exe_name = self.parse_exe_name(self.exe_file)
        self.context = context
        self.icon_location = os.path.abspath(os.path.normpath(icon)) if icon is not None else r'%SystemRoot%\system32\shell32.dll,238'
        self.script = None if bat_file is None else os.path.abspath(os.path.normpath(bat_file))
        self.init_log_data()

    @staticmethod
    def parse_exe_name(file):
        """ Return the EXE name """
        return os.path.splitext(os.path.basename(file))[0]

    @staticmethod
    def parse_exe_directory(file):
        return os.path.dirname(file)


    def add_exe_to_path(self) -> 'PathWriter':
        """ Try to add EXE to User Path """
        try:
            with winreg.OpenKey(self.cu, self.env) as key:
                cp = winreg.QueryValueEx(key, 'PATH')
                if self.path not in cp[0].split(';'):
                    print('Attempting to add key to User PATH')

                    with winreg.OpenKey(self.cu, self.env) as key:
                        winreg.SetValueEx(key, 'PATH', 0, winreg.REG_SZ, self.path)
                        logging.info('Successfully added EXE to User Environment')
                else:
                    logging.info(f'{self.exe_name} Directory Path is already added to User PATH')
        except OSError as e:
            logging.error(f'OSError occured: {e}')
        except PermissionError:
            logging.error('Must be run with Elevated Privileges.')

        return self

    def init_log_data(self):
        logging.info(f'EXE FilePath: {self.exe_file}')
        logging.info(f'EXE FileName: {self.exe_name}')
        logging.info(f'REG FilePath: {self.path}')
        logging.info(f'Bat FilePath: {self.script}')
        logging.info(f'ICO FilePath: {self.icon_location}')

    def add_to_registry(self, rpath, command_path):
        try:
            with winreg.CreateKey(self.root, rpath) as key:
                winreg.SetValue(key, '', winreg.REG_SZ, f'{self.context}')
                winreg.SetValueEx(key, 'Icon', 0, winreg.REG_SZ, self.icon_location)
            with winreg.CreateKey(self.root, command_path) as key:
                winreg.SetValue(key, '', winreg.REG_SZ, f'{self.script} "%1"')
            return True
        except PermissionError:
            logging.error('Must be run with Elevated Privileges.')
        return False

    def contextmenu_for_directory(self) -> 'PathWriter':
        shell_path = os.path.normpath(f'Directory/shell/{self.exe_name}')
        shell_command = os.path.normpath(f'{shell_path}/command')

        if self.add_to_registry(shell_path, shell_command):
            logging.info(f'Shell Path: {shell_path}')
            logging.info(f'Shell Command: {shell_command}')

        return self

    def contextmenu_for_images(self, img_type:str|None=None) -> 'PathWriter':
        if img_type is None:
            fa = os.path.normpath(f"SystemFileAssociations/image/shell/{self.exe_name}")
        else:
            fa = os.path.normpath(f"SystemFileAssociations/.{img_type}/shell/{self.exe_name}")
        fa_command = os.path.normpath(f'{fa}/command')

        if self.add_to_registry(fa, fa_command):
            logging.info(f'FileAssocation Path: {fa}')
            logging.info(f'FileAssocation Command: {fa_command}')

        return self

# Paths to your executable, batch file, icon file
executable_path = 'svg2icoEXE/dist/svg2ico.exe' # Default where pyinstaller will install EXE 'svg2icoEXE/dist/svg2ico.exe'
bat_file_path = 'svg2icoEXE/s2i.bat'
icon_path = 'svg2icoEXE/assets/ConversionIcon.ico'
text = 'Convert SVG to ICO' #change to say what ever here

pathw = PathWriter(file_path=executable_path, bat_file=bat_file_path, context=text, icon=icon_path)

pathw.add_exe_to_path()
pathw.contextmenu_for_directory()
pathw.contextmenu_for_images(img_type='svg')


