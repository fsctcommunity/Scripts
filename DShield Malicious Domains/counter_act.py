import xml.etree.cElementTree as ET
import requests


# Create the High XML
# Each function high, medium, low will parse the domains from the ISC endpoints and create the correctly formatted XML
def high():
    fsapi = ET.Element("FSAPI", TYPE="request", API_VERSION="2.0")
    trans = ET.SubElement(fsapi, "TRANSACTION", TYPE="add_list_values")
    lists = ET.SubElement(trans, "LISTS")
    # List name in CounterAct you want to update
    sensitivity = ET.SubElement(lists, "LIST", NAME="High Level Sensitivity (DShield)")

    # Make a request to the isc site for the list of domains
    r = requests.get('https://isc.sans.edu/feeds/suspiciousdomains_High.txt')
    str = r.text
    # Using 'Split' to parse the domains from the list
    # This looks at everything after the 'Site' but ends at the '# STAT', This way we get all the domains from the list
    strList = list(((str.split("#\nSite\n", 1)[1]).split("#\n# STAT", 1)[0]).split("\n"))
    # Delete the last newline from the file to prevent an empty list value
    del strList[-1]
    # Loop through the list and upload into the 'VALUE' of the XML
    for url in strList:
        value = ET.SubElement(sensitivity, "VALUE").text = url

    tree = ET.ElementTree(fsapi)
    # Name of the file and correct encoding
    tree.write("high.xml", xml_declaration=True, encoding='utf-8')


# Create the Medium XML
def med():
    fsapi = ET.Element("FSAPI", TYPE="request", API_VERSION="2.0")
    trans = ET.SubElement(fsapi, "TRANSACTION", TYPE="add_list_values")
    lists = ET.SubElement(trans, "LISTS")
    sensitivity = ET.SubElement(lists, "LIST", NAME="Medium Level Sensitivity (DShield)")

    r = requests.get('https://isc.sans.edu/feeds/suspiciousdomains_Medium.txt')
    str = r.text
    strList = list(((str.split("#\nSite\n", 1)[1]).split("#\n# STAT", 1)[0]).split("\n"))
    del strList[-1]
    for url in strList:
        value = ET.SubElement(sensitivity, "VALUE").text = url

    tree = ET.ElementTree(fsapi)
    tree.write("med.xml", xml_declaration=True, encoding='utf-8')


# Create the low XML
def low():
    fsapi = ET.Element("FSAPI", TYPE="request", API_VERSION="2.0")
    trans = ET.SubElement(fsapi, "TRANSACTION", TYPE="add_list_values")
    lists = ET.SubElement(trans, "LISTS")
    sensitivity = ET.SubElement(lists, "LIST", NAME="Low Level Sensitivity (DShield)")

    r = requests.get('https://isc.sans.edu/feeds/suspiciousdomains_Low.txt')
    str = r.text
    strList = list(((str.split("#\nSite\n", 1)[1]).split("#\n# STAT", 1)[0]).split("\n"))
    del strList[-1]
    for url in strList:
        value = ET.SubElement(sensitivity, "VALUE").text = url

    tree = ET.ElementTree(fsapi)
    tree.write("low.xml", xml_declaration=True, encoding='utf-8')


# Delete the 3 CounterACT Lists using the 'Delete' XML
def delete():
    headers = {
        'Content-Type': 'application/xml',
    }
    # Path to the delete XML file
    data = open('/home/centos/miscellaneous/counter_act/delete.xml')
    r = requests.post('SERVER/fsapi/niCore/Lists', headers=headers, data=data,
                             verify=False, auth=('USERNAME@ACCOUNT', 'PASSWORD'))
    # 200
    print(r.status_code)
    # <MESSAGE>Successfully deleted all values in the [3] lists.</MESSAGE>
    print(r.text)


""" Each function will push the XML files to CounterACT """
def pushHigh():
    headers = {
        'Content-Type': 'application/xml',
    }
    # Path to the file that is going to be uploaded
    data = open('/home/centos/miscellaneous/counter_act/high.xml')
    r = requests.post('SERVER/fsapi/niCore/Lists', headers=headers, data=data,
                             verify=False, auth=('USERNAME@ACCOUNT', 'PASSWORD'))
    print(r.status_code)
    # <MESSAGE>Successfully added values to the [1] lists.</MESSAGE>
    print(r.text)


def pushMed():
    headers = {
        'Content-Type': 'application/xml',
    }

    data = open('/home/centos/miscellaneous/counter_act/med.xml')
    r = requests.post('https://SERVER/fsapi/niCore/Lists', headers=headers, data=data,
                             verify=False, auth=('USERNAME@ACCOUNT', 'PASSWORD'))
    print(r.status_code)
    print(r.text)


def pushLow():
    headers = {
        'Content-Type': 'application/xml',
    }

    data = open('/home/centos/miscellaneous/counter_act/low.xml')
    r = requests.post('https://SERVER/fsapi/niCore/Lists', headers=headers, data=data,
                             verify=False, auth=('USERNAME@ACCOUNT', 'PASSWORD'))
    print(r.status_code)
    print(r.text)


# Start by Deleting all list contents, Creating each XML file, and Lastly pushing each file to CounterACT
if __name__ == '__main__':
    delete()
    high()
    med()
    low()
    pushHigh()
    pushMed()
    pushLow()
