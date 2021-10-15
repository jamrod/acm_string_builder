import csv

def read_csv(path_to_file):
    with open(path_to_file) as csv_file:
        return csv.DictReader(csv_file)

def format_string(data):

    pass

def format_group_string(data):
    pass

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
        call_points.push(format_string(call_point))
        if call_groups[call_point["CALL-GROUP"]]:
            call_groups[call_point["CALL-GROUP"].push(call.point["CALL-POINT"])]
        else:
            call_groups[call_point["CALL-GROUP"] = [call.point["CALL-POINT"]]
    call_point_output = "\n".join(call_points)
    call_group_strings = []
    for group in call_groups:
        call_group_strings.push(format_group_string(group))
    call_group_ouput = "\n".join(call_group_strings)


if __name__ == "__main__":
    main()