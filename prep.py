import re

# Get multiline input from the user
print("Enter your text (press enter twice to finish):")
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

print(clean_text)



