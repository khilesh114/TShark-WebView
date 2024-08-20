import subprocess
import asyncio
import websockets

async def capture_packets(websocket, path):
    # Start tshark process to capture packets
    process = subprocess.Popen(
        ['tshark', '-i', 'eth0', '-T', 'fields', '-e', 'frame.number', '-e', 'frame.time', 
         '-e', 'ip.src', '-e', 'ip.dst', '-e', 'frame.len', '-e', 'frame.protocols'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
    )

    # Stream captured packets to the WebSocket
    for line in process.stdout:
        await websocket.send(line)

# Start WebSocket server
start_server = websockets.serve(capture_packets, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
