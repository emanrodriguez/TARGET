import sys
import subprocess


def install(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
    return


if __name__ == '__main__':
    packages = ['selenium', 'tqdm', 'tkinter', 'json']
    for i in packages:
        install(i)
