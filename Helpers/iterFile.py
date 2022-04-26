import json
from jsonschema import validate,Draft4Validator, ValidationError, SchemaError

def validateJson(schemaPath,json_file,file_path):
    suberror_list=list()
    errors=list()
    event=list(json_file["GAEvent"].keys())[0]
    with open(schemaPath,"r") as jsonSchema:
        schema=json.load(jsonSchema)
    
    v = Draft4Validator(schema)
    errors = sorted(v.iter_errors(json_file), key=lambda e: e.path)
    for error in errors:
        for suberror in sorted(error.context, key=lambda e: e.schema_path)[:-6]:
            suberror_list.append(f"{file_path}|{list(suberror.path)[1]}|{list(suberror.path)}|{suberror.message}")
    if not errors:
        return [f"{file_path}|{event}|NaN|ValidEvent"]
    else:
        return suberror_list

    # try:
    #     validate(json_file, schema)
    #     return ("valid file")

    # except SchemaError as e:
    #     print("There is an error with the schema")
    #     print (e)
    #     return ("There is an error with the schema")
        
    # except ValidationError as e:
    #     # print(e.message)
    #     return(e.message)
    #     # print("---------")
    #     # print(e.absolute_path)
    
    #     # print("---------")
    #     # print(e.absolute_schema_path)


def iterFile(file_path,schema_path):
    fileResults=list()
    with open(file_path,"r") as file :
        for i,line in enumerate(file):
            try:
                json_file=json.loads(line)
                fileResults+=[validateJson(schema_path,json_file,file_path)]
            except:
                fileResults+=[[f"{file_path}|InvalidJson|NaN|Invalid Json Format"]]
    return (fileResults,i+1)
    


