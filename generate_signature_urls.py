import re
import os
import base64

def generate_auth_urls_from_channel_auth_file(file_path):
    """
    Reads channelAuth.txt, extracts authentication parameters for each channel,
    decodes base64 values for authTs, authRnd, and authSig,
    and generates a list of auth.php URLs.
    """
    auth_urls = []
    
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            channel_key = None
            current_vars = {} # Use a dictionary to store found variables for the current block

            # Look for channelKey
            key_match = re.search(r'var channelKey = "([^"]+)"', line)
            if key_match:
                channel_key = key_match.group(1)
                
                # Read next lines to find __d, __c, __e, up to a reasonable limit (e.g., 5 lines)
                # or until another channelKey is found.
                j = i + 1
                while j < len(lines) and (j - (i + 1) < 5): # Limit lines to check per block
                    next_line = lines[j].strip()
                    
                    # Check if another channelKey appears, if so, stop reading for current block
                    if re.search(r'var channelKey = "([^"]+)"', next_line):
                        break

                    d_match = re.search(r'var __d\s*=\s*atob\("([^"]+)"\)', next_line)
                    c_match = re.search(r'var __c\s*=\s*atob\("([^"]+)"\)', next_line)
                    e_match = re.search(r'var __e\s*=\s*atob\("([^"]+)"\)', next_line)

                    if d_match:
                        current_vars['__d'] = d_match.group(1)
                    elif c_match:
                        current_vars['__c'] = c_match.group(1)
                    elif e_match:
                        current_vars['__e'] = e_match.group(1)
                    
                    # If all three variables are found, we can process this block
                    if all(v in current_vars for v in ['__d', '__c', '__e']):
                        break # Exit inner loop, found all needed variables

                    j += 1
                
                # Check if all variables were found for the current channelKey block
                if all(v in current_vars for v in ['__d', '__c', '__e']):
                    try:
                        # Corrected assignment based on content type:
                        # __c is timestamp (authTs)
                        # __d is random (authRnd)
                        # __e is signature (authSig)
                        auth_ts = base64.b64decode(current_vars['__c']).decode('utf-8')
                        auth_rnd = base64.b64decode(current_vars['__d']).decode('utf-8')
                        auth_sig = base64.b64decode(current_vars['__e']).decode('utf-8')

                        # Construct the URL using the extracted and decoded values
                        base_url = "https://top2new.newkso.ru/auth.php"
                        url = (f"{base_url}?channel_id={channel_key}"
                               f"&ts={auth_ts}"
                               f"&rnd={auth_rnd}"
                               f"&sig={auth_sig}")
                        auth_urls.append(url)
                        i = j + 1 # Move 'i' to the line after the last variable found for this block
                        continue # Continue to next iteration from the new position
                    except Exception as decode_e:
                        print(f"Warning: Base64 decoding or URL construction error for channelKey '{channel_key}' (starting line {i+1}): {decode_e}. Skipping this block.")
                        i = j + 1 # Move past this block
                        continue
                else:
                    print(f"Warning: Incomplete or malformed auth data block found for channelKey '{channel_key}' (starting line {i+1}). Missing some variables. Skipping this block.")
                    i = j + 1 # Move past this block
                    continue
            
            # If the current line is not a 'var channelKey' line, just move to the next line
            i += 1 

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found. Please ensure it exists in the same directory as the script.")
    except Exception as e:
        print(f"An unexpected error occurred while reading or parsing '{file_path}': {e}")
        
    return auth_urls

if __name__ == "__main__":
    channel_auth_file = "channelAuth.txt"
    output_urls_file = "signatureURLs.txt"

    generated_urls = generate_auth_urls_from_channel_auth_file(channel_auth_file)
    
    if generated_urls:
        try:
            with open(output_urls_file, 'w') as f:
                for url in generated_urls:
                    f.write(url + '\n')
            print(f"Successfully generated {len(generated_urls)} auth.php URLs and saved them to '{output_urls_file}'.")
        except IOError as e:
            print(f"Error writing to file '{output_urls_file}': {e}")
    else:
        print(f"No auth.php URLs generated. Please check your '{channel_auth_file}' file's content and format.")
