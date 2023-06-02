import os
import sys
import subprocess
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(current_dir, 'frontend')
sys.path.append(frontend_dir)
import frontendApp

class RunApp():
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

    def main(self):
        front = frontendApp.Frontend()
        # subprocess.run('streamlit run '+ frontend_dir +'/frontendApp.py')
        front.main()


if __name__ == '__main__':
    run = RunApp()
    run.main()
