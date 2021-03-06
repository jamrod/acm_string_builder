import csv
from os.path import exists

#Translation table from acm CALL-KIND to ccp Call Types and device model numbers
#"CALL KIND" : ("Call Type", "model"), no comma on the last line
CALL_KIND_TRANSLATION = {
    "NURSE-PRESENCE" : ("Staff Presence", "CPS-2MSP"),
    "CODE-BLUE" : ("Code Blue", "CPS-2MCB"),
    "TOILET-CALL" : ("Bathroom Call", "CPS-1PCRb"),
    "ALARM-CALL" : ("Patient Call", "CM-PMGb"),
    "EMERG-CALL" : ("Staff Assist", "CPS-2MEM"),
    "BED-EXIT" : ("Bed Exit", "CS-PMPAD")
}

def read_csv(path_to_file):
    #load csv file and return as a list of dictionaries for each row
    out = []
    with open(path_to_file) as csv_file:
        rows = csv.DictReader(csv_file)
        out = [row for row in rows]
    return out

def format_call_string(cp_data, node_number, net_name):
    #returns a string representing a single call point
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

def format_xml_callstring(cp_data, node_number):
    #returns an xml string representing one callpoint
    cpid = f"{node_number}.{cp_data['CALL-POINT']}"
    sctype = CALL_KIND_TRANSLATION.get(cp_data["KIND"])[0]
    if cp_data["DEVICE"] == "V":
        model = "CP-SCPGb"
    else:
        model = CALL_KIND_TRANSLATION.get(cp_data["KIND"])[1]
    location = ""
    if len(cp_data["LOCATION"]) >= 1:
        location = cp_data["LOCATION"]
    else:
        remove_words = ("PRESENCE", "CODE", "EXIT", "BED", "BATH", "ASSIST")
        check_words = cp_data["NAME"].split()
        for i, w in enumerate(check_words):
            if w in remove_words:
                check_words.pop(i)
        location = ".".join(check_words)
    xml_out = f"<callpoint><cpid>{cpid}</cpid><sctype>{sctype}</sctype><model>{model}</model><location>{location}</location></callpoint>"
    return xml_out

def format_xml_file(xml_strings):
    output = "<content>\n  "
    output += "\n  ".join(xml_strings)
    output += "\n</content>"
    return output  

def get_input():
    #prompt user for the node number, network name, csv file and return values as a set
    check_input = False
    def prompt_inputs():
        node = input("What's the node number? ")
        net = input("What's the network name? ")
        csv_path = input("Path to csv: ")
        good_path = exists(csv_path)
        while not good_path:
            csv_path = input("File not found, re-enter path to csv: ")
            good_path = exists(csv_path)
        message = f"""I've got:\n node = {node}\n net = {net}\n Path to csv = {csv_path}\nIs that right ('y' to accept or 'n' to start over)? """
        confirm = input(message)
        if confirm == 'y':
            return (node, net, csv_path)
        else:
            return False
    while not check_input:
        check_input = prompt_inputs()
    return check_input
    
def process_csv_data(data, node_number, net_name):
    #Work through list of csv data generating call points string, call group strings and xml strings and return as a set
    call_groups = {}
    call_points = []
    xml_call_points = []
    for call_point in data:
        if len(call_point["KIND"]) >= 1:
            call_points.append(format_call_string(call_point, node_number, net_name))
            if len(call_point["NAME"]) >= 1:
                xml_call_points.append(format_xml_callstring(call_point, node_number))
            if len(call_point["CALL-GROUP"]) >= 1:
                cp_symbol = f"_{node_number}_{call_point['CALL-POINT']}"
                if call_point["CALL-GROUP"] in call_groups:
                    call_groups[call_point["CALL-GROUP"]].append(cp_symbol)
                else:
                    call_groups[call_point["CALL-GROUP"]] = [cp_symbol]
    call_point_output = "\n".join(call_points)
    xml_call_point_output = format_xml_file(xml_call_points)
    call_group_strings = []
    for group in call_groups:
        call_group_strings.append(format_group_string(group, call_groups[group], node_number))
    call_group_output = "\n".join(call_group_strings)

    return (call_point_output, call_group_output, xml_call_point_output)#f"{call_point_output}\n{call_group_ouput}"

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
    files_name = input[2][:-4]
    output_strings = process_csv_data(csv_data, node_number, net_name)
    call_point_full_string = output_strings[0]
    call_groups_full_string = output_strings[1]
    ccp_import_data = output_strings[2]
    path_to_call_point_file = f"{files_name}_call_points.txt"
    path_to_call_group_file = f"{files_name}_call_groups.txt"
    path_to_xml_file = f"{files_name}_ccp_import.xml"
    with open (path_to_call_point_file, "w") as write_file:
        write_file.write(call_point_full_string)
    with open (path_to_call_group_file, "w") as write_file:
        write_file.write(call_groups_full_string)
    with open (path_to_xml_file, "w") as write_file:
        write_file.write(ccp_import_data)
    return (path_to_call_point_file, path_to_call_group_file, path_to_xml_file)


if __name__ == "__main__":
    files_written = main()
    if files_written:
        files = ", ".join(files_written)
        print(f"Sucess!\nFiles created - {files}")
    else:
        print("exiting...")