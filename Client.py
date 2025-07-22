import requests
import websockets
import asyncio
import getpass
import json

# Configuration for dev and production
DEV_IP = "127.0.0.1"
PROD_IP = "20.197.32.163"  # Change this to your production IP
PORT = "8000"

def choose_mode():
    mode = input("Select mode (dev/prod): ").strip().lower()
    if mode == "prod":
        print(f"[INFO] Running in PRODUCTION mode ({PROD_IP})")
        return PROD_IP
    else:
        print(f"[INFO] Running in DEVELOPMENT mode ({DEV_IP})")
        return DEV_IP

def get_sessionid(login_url):
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    session = requests.Session()
    print("[INFO] Logging in...")
    resp = session.post(login_url, data={"username": username, "password": password})
    if resp.status_code == 200 and resp.json().get("success"):
        print("[SUCCESS] Login successful.")
        return session.cookies.get("sessionid")
    else:
        print("[ERROR] Login failed:", resp.text)
        return None

class WebSocketClient:
    def __init__(self, ws_url, sessionid):
        self.ws_url = ws_url
        self.sessionid = sessionid
        self.ws = None

    async def connect(self):
        print(f"[INFO] Connecting to WebSocket at {self.ws_url} ...")
        self.ws = await websockets.connect(
            self.ws_url,
            additional_headers={"Cookie": f"sessionid={self.sessionid}"}
        )
        print("[SUCCESS] Connected to WebSocket.")

    async def disconnect(self):
        if self.ws:
            await self.ws.close()
            print("[INFO] Disconnected from WebSocket.")

    async def send(self, message):
        if self.ws:
            await self.ws.send(message)
            print(f"[SEND] {message}")

    async def receive(self):
        if self.ws:
            try:
                async for msg in self.ws:
                    print(f"[RECEIVED] {msg}")
            except websockets.ConnectionClosed:
                print("[INFO] Connection closed by server.")

async def main():
    ip = choose_mode()
    LOGIN_URL = f"http://{ip}:{PORT}/login/"
    sessionid = get_sessionid(LOGIN_URL)
    print(f"[DEBUG] sessionid={sessionid}")
    if not sessionid:
        print("[ERROR] Exiting due to failed login.")
        return

    group_name = input("Enter Group ID: ").replace(" ", "")
    ws_url = f"ws://{ip}:{PORT}/ws/{group_name}/"
    client = WebSocketClient(ws_url, sessionid)
    await client.connect()

    # Start the receive coroutine as a background task
    receive_task = asyncio.create_task(client.receive())

    try:
        while True:
            msg = await asyncio.get_event_loop().run_in_executor(None, input, "[INPUT] Type message (or 'exit' to quit): ")
            if msg.lower() == "exit":
                print("[INFO] Exiting chat...")
                break
            await client.send(json.dumps({"msg": msg}))
    finally:
        await client.disconnect()
        receive_task.cancel()
        try:
            await receive_task
        except asyncio.CancelledError:
            pass

if __name__ == "__main__":
    asyncio.run(main())