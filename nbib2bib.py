##################################################################
'''Script to convert .nbib to bibTeX. Written by Thiago Santos.'''
##################################################################
import os
from time import strftime
from time import sleep, time
import urllib.request as req
from urllib.error import HTTPError

def nbib_files(directory):
    '''Retrieves which files in the directory that can be converted'''
    return [file for file in os.listdir(directory)
            if file.lower().endswith('.nbib')]

def create_bibs_folder(directory):
    '''Creates a new directory within current directory called bibs'''
    directory = os.path.join(directory, 'bibs')
    if not os.path.exists(directory):
        os.makedirs(directory)

def read_doi(path):
    with open(path, "r") as f:
        for line in f:
            string = "doi"

            if string in line: # checking if string is present in line
                # the doi begins after "PID - ", what means the 7th character (6th, when considered that python starts to count on 0)
                # the doi string ends before " " (blank space)
                doi = line[6:line.rfind(" ")]
                print(f"DOI {i+1}: {doi}")
                return doi
    return ""

def bib_from_doi(doi):
    BASE_URL = 'http://dx.doi.org/'

    url = BASE_URL + doi
    r = req.Request(url, headers={"Accept": "application/x-bibtex"})
    with req.urlopen(r) as reqopen:
        return reqopen.read().decode()

if __name__ == "__main__":
    input('Press enter to continue...')

    process_start = time()

    directory = os.getcwd()

    files = nbib_files(directory)
    if len(files) == 0: # verifying how many nbib files are present in the current folder (if 0, the program doesn't do anything and stop)
        print('There are no files to convert')
        exit()

    create_bibs_folder(directory)

    print('Starting conversion... \n')

    try:
        print(f"I've found {len(files)} nbib files in folder {directory}")

        with open(f'bibs/ref.bib', 'w') as output:
            for i, file in enumerate(files):
                ending = '.nbib'

                doi = read_doi(file)

                if doi == "":
                    print(f"Can't find DOI in {file}.")
                    continue

                try:
                    bib = bib_from_doi(doi)
                except HTTPError as e:
                    if e.code == 404:
                        print('DOI not found')
                    else:
                        print(f'Service unavailable: {e}')

                output.write(f'{bib}\n\n')

        process_end = time()
        elapsed = process_end - process_start
        print(f"Processing time: {elapsed}")
        input("Press enter to finish process...")
    except Exception as e:
        print(e)

    print('\nConversion finished at ' + strftime("%H:%M:%S"))

