import subprocess
import sys

# Capture packets using TShark and save to a file
with open('packets.txt', 'w') as f:
    process = subprocess.Popen(
        ['tshark',  '-T', 'fields', '-e', 'frame.number', '-e', 'frame.time',
         '-e', 'ip.src', '-e', 'ip.dst', '-e', 'udp.srcport', '-e', 'udp.dstport', '-e',
         'tcp.srcport', '-e', 'tcp.dstport', '-e', 'frame.len', '-e', 'frame.protocols', '-e',
         'dns.qry.name', '-e', 'dns.a', '-e', 'dns.ns'],
        stdout=f, stderr=subprocess.PIPE, universal_newlines=True
    )

    try:
        print("tshark is running")
        # Wait for the process to complete
        process.wait()
        
    except KeyboardInterrupt:
        # Handle keyboard interrupt to stop the process
        print("Interrupted by user. Stopping TShark...")
        process.terminate()
        process.wait()  # Ensure the process has terminated
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}", file=sys.stderr)
        process.terminate()
        process.wait()  # Ensure the process has terminated
    finally:
        # Capture any stderr output if needed
        stderr_output = process.stderr.read()
        if stderr_output:
            print(f"TShark Error: {stderr_output}", file=sys.stderr)
