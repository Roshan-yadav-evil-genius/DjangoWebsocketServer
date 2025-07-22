import requests
import websockets
import asyncio
import getpass
import json

IP="127.0.0.1"
PORT="8000"
LOGIN_URL = f"http://{IP}:{PORT}/login/"

def get_sessionid():
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    session = requests.Session()
    resp = session.post(LOGIN_URL, data={"username": username, "password": password})
    if resp.status_code == 200 and resp.json().get("success"):
        print("Login successful.")
        return session.cookies.get("sessionid")
    else:
        print("Login failed:", resp.text)
        return None

class WebSocketClient:
    def __init__(self, ws_url, sessionid):
        self.ws_url = ws_url
        self.sessionid = sessionid
        self.ws = None

    async def connect(self):
        print("Connecting to WebSocket...")
        self.ws = await websockets.connect(
            self.ws_url,
            additional_headers={"Cookie": f"sessionid={self.sessionid}"}
        )
        print("Connected.")

    async def disconnect(self):
        if self.ws:
            await self.ws.close()
            print("Disconnected.")

    async def send(self, message):
        if self.ws:
            await self.ws.send(message)
            print("Sent:", message)

    async def receive(self):
        if self.ws:
            try:
                async for msg in self.ws:
                    print("Received:", msg)
            except websockets.ConnectionClosed:
                print("Connection closed.")

async def main():
    sessionid = get_sessionid()
    if not sessionid:
        return
    
    
    GROUP_NAME=input("Group ID:").replace(" ","")

    client = WebSocketClient(f"ws://{IP}:{PORT}/ws/{GROUP_NAME}/", sessionid)
    await client.connect()

    # Start the receive coroutine as a background task
    receive_task = asyncio.create_task(client.receive())

    try:
        while True:
            msg = await asyncio.get_event_loop().run_in_executor(None, input, "Type message (or 'exit' to quit): ")
            
            if msg.lower() == "exit":
                break
            await client.send(json.dumps({"msg":msg}))
    finally:
        await client.disconnect()
        receive_task.cancel()
        try:
            await receive_task
        except asyncio.CancelledError:
            pass

if __name__ == "__main__":
    asyncio.run(main())