import json
import os
import re

# Ensure user_data directory exists
if not os.path.exists('user_data'):
        os.makedirs('user_data')

while True:
    record = {}

    # Get simple string input for most fields
    record['pageId'] = input("Enter pageId: ")
    record['title'] = input("Enter title: ")
    #record['comments'] = input("Enter comments: ")
    #record['labels'] = input("Enter labels: ")
    #record['editors'] = input("Enter editors: ")
    #record['fuzzy'] = input("Enter fuzzy: ")
    #record['url'] = input("Enter url: ")

    record['editors'] = "Vasiliy Kraskovskiy, Martins Svirksts"
    record['url'] = "https://wiki.spb.openwaygroup.com/pages/viewpage.action?pageId=" + record['pageId']
    record['comments'] = ""
    record['labels'] = ""
    record['fuzzy'] = ""


    # Get multiline input for the body
    print("Enter the body text (press enter twice to finish, '#' to end):")
    lines = []
    while True:
        line = input()
        if line:
           lines.append(line)
        if len(line) == 1 and line[0] == "#":
           break
    text = '\n'.join(lines)

    # Remove newlines
    single_line_text = text.replace('\n', ' ')

    # Remove special characters, including quotes and double quotes
    clean_text = re.sub(r'[^\w\s]', '', single_line_text)

    record['body'] = clean_text

    # Save the record as a JSON file in the user_data directory
    filename = os.path.join('user_data', f"{record['pageId']}.json")
    with open(filename, 'w') as f:
                json.dump(record, f)

    print(f"Record saved as {filename}")

    # Ask if the user wants to enter another record
    should_continue = input("Do you want to enter another record? (y/n): ")
    if should_continue.lower() != 'y':
                break



