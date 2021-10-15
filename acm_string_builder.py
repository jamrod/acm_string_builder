import csv

def read_csv(path_to_file):
    with open(path_to_file) as csv_file:
        return csv.DictReader(csv_file)

def format_call_string(cp_data, node_number, net_name):
    msg_4 = f"{node_number}{cp_data['CALL_POINT']}"
    msg_8_12 = f"{node_number}-{cp_data['CALL_POINT']}"
    input = cp_data["CALL_POINT"]
    if cp_data["DEVICE"] == "V":
        input = cp_data["INPUT"]
    output = f"""(CALL _{node_number}_{cp_data["CALL_POINT"]} _{cp_data["KIND"]} _CALL-LOCATION-{node_number}
	(_NAME NAME)
	(NETWORK _{net_name})
	(NAME \"{cp_data["NAME"]}\")
	(_NAME-4 \"{msg_4}\")
	(_NAME-8 \"{msg_8_12}\")
	(_NAME-12 \"{msg_8_12}\")
	(_A2-MESSAGE-NUMBER \"{cp_data["CALL_POINT"]}\")
	(_CALL-NUMBER {cp_data["CALL_POINT"]})
	(RC _RC-{node_number} {input} {cp_data["CONDITION"]} {cp_data["CONDITION-INPUTS"]} TALK {cp_data["TALK"]}))"""
    return output

def format_group_string(group, group_members):
    return f"""(CALL-GROUP _{group} {" ".join(group_members)} _CALL-LOCATION-{node_number}
	(NAME \"{group}\"))"""
    

def get_input():
    node = input("What's the node number? ")
    net = input("What's the network name?")
    csv_path = input("Path to csv: ")
    return (node, net, csv_path)

def main():
    print('I'm running!)
    input = get_input()
    node_number = input[0]
    net_name = input[1]
    csv_data = read_csv(input[3])
    call_groups = {}
    call_points = []
    for call_point in csv_data:
        call_points.push(format_call_string(call_point, node_number, net_name))
        if call_groups[call_point["CALL-GROUP"]]:
            call_groups[call_point["CALL-GROUP"].push(call.point["CALL-POINT"])]
        else:
            call_groups[call_point["CALL-GROUP"] = [call.point["CALL-POINT"]]
    call_point_output = "\n".join(call_points)
    call_group_strings = []
    for group in call_groups:
        call_group_strings.push(format_group_string(group, call_groups[group]))
    call_group_ouput = "\n".join(call_group_strings)
    return call_point_output


if __name__ == "__main__":
    main()