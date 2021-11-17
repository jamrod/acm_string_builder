import csv
from os.path import exists

def read_csv(path_to_file):
    #load csv file and return as a list of dictionaries for each row
    out = []
    with open(path_to_file) as csv_file:
        rows = csv.DictReader(csv_file)
        out = [row for row in rows]
    return out

<<<<<<< HEAD
def format_call_string(cp_data, node_number, net_name): 
=======
def format_call_string(cp_data, node_number, net_name):
    #returns a string representing a single call point
>>>>>>> 7350f0bc64368cb21b11ec588437779079e4afd3
    msg_4 = f"{node_number}{cp_data['CALL-POINT']}"
    msg_8_12 = f"{node_number}-{cp_data['CALL-POINT']}"
    nameString = cp_data["NAME"]
    name = nameString if len(nameString)>1 else msg_8_12
    input = cp_data["CALL-POINT"]
    if cp_data["DEVICE"] == "V":
        input = cp_data["INPUT"]
    output = f"""(CALL _{node_number}_{cp_data["CALL-POINT"]} _CALL-{cp_data["KIND"]} _CALL-LOCATION-{node_number}
	(_NAME NAME)
	(NETWORK _{net_name})
	(NAME \"{name}\")
	(_NAME-4 \"{msg_4}\")
	(_NAME-8 \"{msg_8_12}\")
	(_NAME-12 \"{msg_8_12}\")
	(_A2-MESSAGE-NUMBER \"{cp_data["CALL-POINT"]}\")
	(_CALL-NUMBER {cp_data["CALL-POINT"]})
	(RC _RC-{node_number} {input} {cp_data["CONDITION"]} {cp_data["CONDITION-INPUTS"]} TALK {cp_data["TALK"]}))\n"""
    return output

def format_group_string(group, group_members, node_number):
    #returns a string representing a call group and its member call points
    return f"""(CALL-GROUP _{group} {" ".join(group_members)} _CALL-LOCATION-{node_number}
	(NAME \"{group}\"))\n"""
    

def get_input():
    #prompt user for the node number, network name, csv file and output file and return values as a set
    check_input = False
    def prompt_inputs():
        node = input("What's the node number? ")
        net = input("What's the network name? ")
        csv_path = input("Path to csv: ")
        good_path = exists(csv_path)
        while not good_path:
            csv_path = input("File not found, re-enter path to csv: ")
        out_path = input("Save string to: ")
        out_exists = exists(out_path)
        write_flag = "w"
        write_flag_text = ""
        if out_exists:
            valid = False
            while not valid:          
                write_flag = input("File exists, enter 'w' to overwrite or 'a' to append new strings: ")
                valid = write_flag == 'w' or write_flag == 'a'
            if write_flag == 'w':
                write_flag_text = "--Overwrite"
            else:
                write_flag_text = "--Append"
        message = f"""I've got:\n node = {node}\n net = {net}\n Path to csv = {csv_path}\n Output to = {out_path} {write_flag_text}\nIs that right ('y' to accept or 'n' to start over)? """
        confirm = input(message)
        if confirm == 'y':
            return (node, net, csv_path, out_path, write_flag)
        else:
            return False
    while not check_input:
        check_input = prompt_inputs()
    return check_input
    
def process_csv_data(data, node_number, net_name):
    #Work through list of csv data generating call points string and call group strings and return a combined string
    call_groups = {}
    call_points = []
    for call_point in data:
        if len(call_point["KIND"]) >= 1:
            call_points.append(format_call_string(call_point, node_number, net_name))
            if len(call_point["CALL-GROUP"]) >= 1:
                cp_symbol = f"_{node_number}_{call_point['CALL-POINT']}"
                if call_point["CALL-GROUP"] in call_groups:
                    call_groups[call_point["CALL-GROUP"]].append(cp_symbol)
                else:
                    call_groups[call_point["CALL-GROUP"]] = [cp_symbol]
    call_point_output = "\n".join(call_points)
    call_group_strings = []
    for group in call_groups:
        call_group_strings.append(format_group_string(group, call_groups[group], node_number))
    call_group_ouput = "\n".join(call_group_strings)
    return f"{call_point_output}\n{call_group_ouput}"

def validate_csv_data(csv_data):
    #check the csv file for all necessary headers and confirm it holds data, returns True or False
    table_length = len(csv_data)
    if table_length <=1:
        print("Invalid csv data, no data")
        return False
    needed_headers = ["DEVICE", "INPUT", "CALL-POINT", "KIND", "NAME", "TALK", "CALL-GROUP", "CONDITION", "CONDITION-INPUTS"]
    column_headers = csv_data[0].keys()
    for header in needed_headers:
        if header not in column_headers:
            print(f"Invalid csv data, Header {header} not found")
            return False
    return True

def main():
    #Generate call point strings and call group strings and output to a text file, returns output file path on sucess or False on fail
    input = get_input()
    node_number = input[0]
    net_name = input[1]
    csv_data = read_csv(input[2])
    valid_csv = validate_csv_data(csv_data)
    if not valid_csv:
        return False
    full_string = process_csv_data(csv_data, node_number, net_name)
    path_to_output = input[3]
    write_condition = input[4]
    with open (path_to_output, write_condition) as write_file:
        write_file.write(full_string)
    return path_to_output


if __name__ == "__main__":
    file_written = main()
    if file_written:
        print(f"Sucess! check {file_written}")
    else:
        print("exiting...")