import subprocess as sp

def build():
    sp.run('pyinstaller -F -w LinkKeeper.py', shell=True)
    
if __name__ == '__main__':
    build()