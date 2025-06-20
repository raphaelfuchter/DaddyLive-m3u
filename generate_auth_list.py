import subprocess
import re
import os

# List of input files containing channel IDs
input_files = ['nfs.txt', 'wind.txt', 'zeko.txt', 'dokko1.txt']

# Clear or create channelAuth.txt
with open('channelAuth.txt', 'w') as f:
    f.write('')

# Function to extract numbers from premiumXXXX
def extract_channel_id(line):
    match = re.search(r'premium(\d+)', line)
    return match.group(1) if match else None

# Function to parse channelAuth.txt and extract variables
def parse_channel_auth():
    channel_data = {}
    current_id = None
    with open('channelAuth.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if 'var channelKey' in line:
                match = re.search(r'var channelKey = "premium(\d+)"', line)
                if match:
                    current_id = match.group(1)
                    channel_data[current_id] = {}
            elif current_id and 'var __c' in line:
                match = re.search(r'var __c = "(\d+)"', line)
                if match:
                    channel_data[current_id]['__c'] = match.group(1)
            elif current_id and 'var __d' in line:
                match = re.search(r'var __d = "(\d+)"', line)
                if match:
                    channel_data[current_id]['__d'] = match.group(1)
            elif current_id and 'var __e' in line:
                match = re.search(r'var __e = "([a-f0-9]+)"', line)
                if match:
                    channel_data[current_id]['__e'] = match.group(1)
    return channel_data

# Step 1: Execute first curl command for each channel ID
for file_name in input_files:
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            for line in f:
                channel_id = extract_channel_id(line.strip())
                if channel_id:
                    curl_cmd = (
                        f'curl -i -H "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) Gecko/20100101 Firefox/139.0" '
                        f'-H "origin: https://allupplay.xyz" -H "referer: https://allupplay.xyz/" '
                        f'"https://lefttoplay.xyz/premiumtv/daddylivehd.php?id={channel_id}" | '
                        f'grep -E "var channelKey|var __c|var __d|var __e" >>channelAuth.txt'
                    )
                    subprocess.run(curl_cmd, shell=True)
    else:
        print(f"File {file_name} not found.")
