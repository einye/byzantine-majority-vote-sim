import socket
import threading
import json
import random

#create processes as dictionary (name, host and a unique port)
PROCESSES = {
    "P": {"host": "127.0.0.1", "port": 5000},
    "Q": {"host": "127.0.0.1", "port": 5001},
    "R": {"host": "127.0.0.1", "port": 5002},
    "S": {"host": "127.0.0.1", "port": 5003},
}

# process P
def faulty_behavior():
    return random.choice(["attack", "retreat"])

def start_process(name):
    def handle_connection(conn, addr):
        message = json.loads(conn.recv(1024).decode()) 
        print(f"[{name}] Received message: {message}") 
        responses[name] = message["command"]
        conn.close()

   
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((PROCESSES[name]["host"], PROCESSES[name]["port"]))
    server.listen(5)
    print(f"[{name}] Listening on {PROCESSES[name]['host']}:{PROCESSES[name]['port']}")

    
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_connection, args=(conn, addr)).start()

# function to send message to process
def send_message(target, message):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((PROCESSES[target]["host"], PROCESSES[target]["port"]))
    client.send(json.dumps(message).encode())
    client.close()

responses = {}
def reach_consensus(name):
    global responses

    if name == "P":
        command = faulty_behavior()
    else:
        command = "retreat"

    message = {"sender": name, "command": command}

    for process in PROCESSES:
        if process != name:
            send_message(process, message)

    print(f"[{name}] Sent command: {command} and waiting for responses")
    threading.Event().wait(3)  

    if name != "P":
        votes = {"attack": 0, "retreat": 0}
        for response in responses.values():
            if response in votes:
                votes[response] += 1

        majority = max(votes, key=votes.get)
        print(f"[{name}] Reached consensus on: {majority}")
    else:
        print(f"[{name}] Faulty behavior, no reliable consensus.")

for name in PROCESSES:
    threading.Thread(target=start_process, args=(name,), daemon=True).start()

for name in PROCESSES:
    threading.Thread(target=reach_consensus, args=(name,), daemon=True).start()

while True:
    pass
