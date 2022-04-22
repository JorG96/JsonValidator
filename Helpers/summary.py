import pandas as pd
import os

def getSummary(path,output_folder,output_file,events_number):
    df = pd.read_csv(path, sep='|')

    #common values
    totalEvents=events_number
    events=df['Event'].unique()
    eventsNumber=len(events)
    errorCount=df['Error'].value_counts()
    eventsCount=df['Event'].value_counts()
    validEvents=df[df['Error']=='ValidEvent']
    validEventsNumber=len(validEvents)
    validEventsCount=validEvents['Event'].value_counts()
    invalidEventsNumber=totalEvents-validEventsNumber

    # list of the schema path for each error
    errorPerEvent=df[['Event','Error_Path','Error']].drop_duplicates().sort_values('Event')

    # Percentages
    validEvents_p=round(len(validEvents)/totalEvents*100,2)
    invalidEvents_p=100-validEvents_p

    eventsCount_EV=pd.merge(eventsCount,validEventsCount,how='outer',suffixes=('_Total', '_Valid'),left_index=True,right_index=True)
    eventsCount_EV.fillna(0,inplace=True)
    eventsCount_EV['Event_Invalid']=eventsCount_EV['Event_Total']-eventsCount_EV['Event_Valid']
    eventsCount_EV['Event_Valid%']=eventsCount_EV['Event_Valid']/eventsCount_EV['Event_Total']*100
    eventsCount_EV['Event_Invalid%']=eventsCount_EV['Event_Invalid']/eventsCount_EV['Event_Total']*100
    eventsCount_EV=eventsCount_EV.astype({'Event_Valid':int,'Event_Invalid':int})
    eventsCount_EV=eventsCount_EV.round({'Event_Valid%':2,'Event_Invalid%':2})
    
    #output
    with open(os.path.join(output_folder, output_file),'w') as outfile:
        outfile.write(f"""Total number  of Events: {totalEvents}
    Valid Events:{validEventsNumber} Percentage:{validEvents_p}%
    Invalid Events: {invalidEventsNumber} Percentage:{invalidEvents_p}%\n""")
        outfile.write("\n------------------------Summary of Instances per Event------------------------\n")
        eventsCount_EV.to_string(outfile)
        outfile.write("\n------------------------Errors per Event-----------------------\n")
        errorPerEvent.to_string(outfile,index=False)
        return