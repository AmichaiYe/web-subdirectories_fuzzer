from sys import argv, exit
from getopt import error
import requests
from threading import Thread

html_codes = [404, 500]

# remove first argument (file name)
argumentList = argv[1:]

# default args
wordlist_path = None
num_of_threads = 2
url = None
timeout = 2

# the actual wordlist
wordlist = None

# mutex to print
mutex = True

def get_arguments():
    global wordlist_path
    global num_of_threads
    global url
    try:
        if argumentList in ("-h", "--help") or len(argumentList) == 0:
            print('    [must] -u, --url: url to fuzz # python fuzzer.py -u http://tempname.com/\n' \
                  '    [must] -w, --wordlist: path to wordlist # python fuzzer.py -w /usr/share/wordlist/big.txt\n' \
                  '    [option] -t, --threads: num of threads to run (default : 50)# python fuzzer.py -t 100\n')
            exit(0)

        for argument, argument_val in zip(argumentList[::2], argumentList[1::2]):
            if argument in ("-w", "--wordlist"):
                wordlist_path = argument_val

            elif argument in ("-u", "--url"):
                if not argument_val.endswith('/'):
                    url = '/'
                url = argument_val

            elif argument in ("-t", "--threads"):
                try:
                    num_of_threads = int(argument_val)
                finally:
                    pass

            else:
                print("Unexpected param parsed")
                exit(0)

    except error as err:
        # output error, and return with an error code
        print(str(err))

def main():
    global wordlist
    global wordlist_path
    get_arguments()

    with open(wordlist_path) as words:
        wordlist = words.read().split('\n')

    for thread_num in range(num_of_threads):
        t = Thread(target=fuzz, args=(thread_num,))
        t.start()


def fuzz(index_of_thread):
    global mutex
    for index in range(index_of_thread, len(wordlist), num_of_threads):
        word = wordlist[index]
        try:
            req = requests.get(url + word, timeout=2)
            if req.status_code not in html_codes:
                print(f'{url + word} : {req.status_code}')
        finally:
            pass
        if mutex:
            mutex = False
            print('                                                         ', end='')
            print('\r', end='')
            print(word, end='')
            mutex = True

if __name__ == '__main__':
    main()

