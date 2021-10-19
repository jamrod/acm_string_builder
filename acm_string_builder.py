import csv

def read_csv(path_to_file):
    out = []
    with open(path_to_file) as csv_file:
        rows = csv.DictReader(csv_file)
        out = [row for row in rows]
    return out

def format_call_string(cp_data, node_number, net_name):
    msg_4 = f"{node_number}{cp_data['CALL-POINT']}"
    msg_8_12 = f"{node_number}-{cp_data['CALL-POINT']}"
    input = cp_data["CALL-POINT"]
    if cp_data["DEVICE"] == "V":
        input = cp_data["INPUT"]
    output = f"""(CALL _{node_number}_{cp_data["CALL-POINT"]} _CALL-{cp_data["KIND"]} _CALL-LOCATION-{node_number}
	(_NAME NAME)
	(NETWORK _{net_name})
	(NAME \"{cp_data["NAME"]}\")
	(_NAME-4 \"{msg_4}\")
	(_NAME-8 \"{msg_8_12}\")
	(_NAME-12 \"{msg_8_12}\")
	(_A2-MESSAGE-NUMBER \"{cp_data["CALL-POINT"]}\")
	(_CALL-NUMBER {cp_data["CALL-POINT"]})
	(RC _RC-{node_number} {input} {cp_data["CONDITION"]} {cp_data["CONDITION-INPUTS"]} TALK {cp_data["TALK"]}))\n"""
    return output

def format_group_string(group, group_members, node_number):
    return f"""(CALL-GROUP _{group} {" ".join(group_members)} _CALL-LOCATION-{node_number}
	(NAME \"{group}\"))\n"""
    

def get_input():
    node = input("What's the node number? ")
    net = input("What's the network name? ")
    csv_path = input("Path to csv: ")
    out_path = input("Save string to: ")
    return (node, net, csv_path, out_path)

def main():
    input = get_input()
    node_number = input[0]
    net_name = input[1]
    csv_data = read_csv(input[2])
    call_groups = {}
    call_points = []
    for call_point in csv_data:
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
    full_string = f"{call_point_output}\n{call_group_ouput}"
    with open (input[3], "w") as write_file:
        write_file.write(full_string)
    return input[3]


if __name__ == "__main__":
    file_written = main()
    if file_written:
        print(f"Sucess! check {file_written}")