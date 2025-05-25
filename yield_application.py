import threading
import subprocess

def run_script(script_name):
    subprocess.run(["python", script_name], check=True)

if __name__ == "__main__":

    script_list = ["yield_calculator.py", "graphing.py"]
    threads = []

    for script in script_list:
        thread = threading.Thread(target=run_script, args=(script,))
        threads.append(thread)
        thread.start()
        print(f"Starting: {script}")
    
    

    for thread in threads:
        thread.join()
