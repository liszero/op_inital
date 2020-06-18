from action.install_app import appinstall
from concurrent.futures import ThreadPoolExecutor
from common.read_json import rd_json
import sys,getopt

def main(filepath):
    file_data = rd_json(filepath)
    with ThreadPoolExecutor(max_workers=5) as t:
        for i in file_data:
            t.submit(appinstall,**i)

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in ["-h","-f"]:
        print("[*] Please use -h/--help to learn how to use")
    else:
        opts, args = getopt.getopt(sys.argv[1:], '-h-f:', ['help', 'filepath='])
        for opt_name, opt_value in opts:
            if opt_name in ('-h', '--help'):
                print("[*] Examples:python main.py -f/--filepath real_filepath")
                exit()
            if opt_name in ('-f', '--filepath'):
                fileName = opt_value
                main(fileName)
                exit()










