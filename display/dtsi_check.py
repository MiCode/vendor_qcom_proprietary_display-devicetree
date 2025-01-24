import re
import sys
import os
import glob

def check_command(dtsi_file, dtsi_content):
    pattern = r'([\w\-_,]+)-commands?\s*=\s*\[([^\]]+)\];'
    matches = re.findall(pattern, dtsi_content)

    if matches:
        for hex_string in matches:
            hex_list = hex_string[1].split()
            index = 0
            while index < len(hex_list):
                if hex_list[index] not in {'01', '02', '03', '04', '05', '06', '07', '08', '09', '0A', '0a', '0B',
                        '0b', '0C', '0c', '0D', '0d', '0E', '0e', '11', '12', '13', '14', '15', '16', '19', '1C', '1c', '1D', '1d',
                        '1E', '1e', '21', '22', '23', '24', '29', '2C', '2c', '2E', '2e', '31', '32', '37', '39', '3D', '3d', '3E', '3e'}:
                    print(f"invalid type {hex_list[index]} in {dtsi_file}:\n{hex_string[0]}-command: {hex_string[1]}")
                    sys.exit(1)
                index += 6
                if index >= len(hex_list):
                    print(f"invalid length in {dtsi_file}:\n{hex_string[0]}-command: {hex_string[1]}")
                    sys.exit(1)
                if index + int(hex_list[index], 16) >= len(hex_list):
                    print(f"invalid payload length in {dtsi_file}:\n{hex_string[0]}-command: {hex_string[1]}")
                    sys.exit(1)
                if hex_list[index - 6] in {'03', '13', '23', '04', '14', '24', '05', '15', '06', '37'} and int(hex_list[index], 16) > 2:
                    print(f"not suitable to use short type {hex_list[index - 6]} in {dtsi_file}:\n{hex_string[0]}-command: {hex_string[1]}")
                    sys.exit(1)
                index = index + int(hex_list[index], 16) + 1


def check_command_state(dtsi_file, dtsi_content):
    pattern = r'([\w\-_,]+)-commands?-state\s*=\s*\"([^\"]+)\";'
    matches = re.findall(pattern, dtsi_content)

    if matches:
        for state_string in matches:
            if state_string[1] != "dsi_lp_mode" and state_string[1] != "dsi_hs_mode":
                print(f"invalid command state in {dtsi_file}:\n{state_string[0]}-command-state: {state_string[1]}")
                sys.exit(1)

current_dir = os.getcwd() + '/' + sys.argv[1]
dtsi_files = glob.glob(os.path.join(current_dir, '*.dtsi'))

for dtsi_file in dtsi_files:
    with open(dtsi_file, 'r') as file:
        dtsi_content = file.read()

    pattern = r'(\/\/[^\n]*|\/\*(.*?)\*\/)'
    dtsi_content = re.sub(pattern, '', dtsi_content, flags=re.DOTALL)

    check_command(dtsi_file, dtsi_content)
    check_command_state(dtsi_file, dtsi_content)
