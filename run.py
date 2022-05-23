#!/usr/bin/ python3
import os
import datetime
from Helpers import logSearch,iterFile,getSummary
from config import DATA_DIRECTORY,OUTPUT_DIRECTORY,JSON_SCHEMA
import argparse

ap=argparse.ArgumentParser()
ap.add_argument("-D", "--DataDirectory",required=True,help="path to the data directory")
ap.add_argument("-o", "--OutputDirectory",default=OUTPUT_DIRECTORY,required=False,help="path to output directory")
ap.add_argument("-s", "--schema",required=True,help="path to json schema file")
args= vars(ap.parse_args())

now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
DATA_DIRECTORY=args["DataDirectory"]
OUTPUT_DIRECTORY=args["OutputDirectory"]
JSON_SCHEMA= args["schema"]
print(OUTPUT_DIRECTORY)
def main(data_directory=DATA_DIRECTORY):

    logList=logSearch(data_directory)
    eventsNumber=0
    with open(f"{OUTPUT_DIRECTORY}/{now}.dsv","x") as output_file:
        output_file.write("File|Event|Error_Path|Error\n")
        for log in logList:
            errors,logLen=iterFile(log,JSON_SCHEMA)
            eventsNumber+=logLen
            for error in errors:               
                output_file.write("\n".join(error))
                output_file.write("\n")
    # getSummary(f"""{OUTPUT_DIRECTORY}/{now}.dsv""",OUTPUT_DIRECTORY,f"{now}_Summary.txt",eventsNumber)
    print(f"output file in:{OUTPUT_DIRECTORY}")

if __name__=='__main__':
    main()


    