import datetime
from Helpers import logSearch,iterFile,getSummary
from config import DATA_DIRECTORY,OUTPUT_DIRECTORY,JSON_SCHEMA

now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def run(data_directory=DATA_DIRECTORY):

    logList=logSearch(data_directory)
    eventsNumber=0
    with open(f"""{OUTPUT_DIRECTORY}{now}.csv""",'w') as output_file:
        output_file.write("File|Event|Error_Path|Error\n")
        for log in logList:
            errors,logLen=iterFile(log,JSON_SCHEMA)
            eventsNumber+=logLen
            for error in errors:               
                output_file.write("\n".join(error))
                output_file.write("\n")
    getSummary(f"""{OUTPUT_DIRECTORY}{now}.csv""",OUTPUT_DIRECTORY,f"{now}_Summary.txt",eventsNumber)
    print(f"output file in:{OUTPUT_DIRECTORY}")

if __name__=='__main__':
    run()


    