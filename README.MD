Builds a string representing a call table and call groups for Austco medcom nursecall siteconfig.

Uses a csv file for input

Needs to have these headers on the first line of the spread sheet:
 - `DEVICE`: set to 'V' to make a virtual call point
 - `Input`: Node input number
 - `KIND`: The name of the call point after 'CALL-' ie 'NURSE-PRESENCE' = 'CALL-NURSE-PRESENCE', this field can't be blank
 - `NAME`: Value for Name field
 - `TALK`: Talk point
 - `CALL-GROUP`: Adds call point to CALL GROUP named, creates CALL GROUP also if named for the first time, ie 'G-CODE'
 - `CONDITION`: 'RESET', 'LOW' or 'HIGH'
 - `CONDITION-INPUTS`: callpoint referenced by CONDITION, multiple entries separated by a single space 