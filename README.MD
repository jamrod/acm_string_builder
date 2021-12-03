Used to speed developement of Austco medcom nursecall with Tacera.

Uses a csv file for input and outputs 3 files 
 - ..._call_points.txt containing text strings representing all the call points to build the CALL-TABLE in the acm file
 - ..._call_groups.txt containing text strings representing call groups to build and assign in the CALL-GROUP section of the acm file 
 - ..._ccp_import.xml containing xml output to be imported into the ccp file as devices and device assignments
 
Needs to have these headers on the first line of the spread sheet:
 - `DEVICE`: set to 'V' to make a virtual call point otherwise reflects the number of the device on the dataline
 - `INPUT`: Device input number unless DEVICE = 'V' then original call-point number effected by condition inputs
 - `CALL-POINT`: Node input number
 - `KIND`: The name of the call kind after 'CALL-' ie 'NURSE-PRESENCE' = 'CALL-NURSE-PRESENCE', this field can't be blank
 - `NAME`: Value for Name field
 - `TALK`: Talk point
 - `CALL-GROUP`: Adds call point to CALL GROUP named, creates CALL GROUP also if named for the first time, ie 'G-CODE'
 - `CONDITION`: 'RESET', 'LOW' or 'HIGH'
 - `CONDITION-INPUTS`: callpoint referenced by CONDITION, multiple entries separated by a single space
 - `LOCATION` : Use to match location in ccp file, if left blank, the script will use the NAME field and remove the any of following words "PRESENCE", "CODE", "EXIT", "BED", "BATH", "ASSIST", then join any remaining terms with a '.' ie "110 BED A" becomes "110.A"

If the KIND column is empty the entire row will be ignored

If the NAME is empty no xml data will be created for that row, but a default value will be rendered for the acm file representing the input number
