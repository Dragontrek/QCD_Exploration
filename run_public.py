import subprocess
import time
import sys
import threading
import re
import os

def main():
    print("Starting FastAPI server...")
    # Start the uvicorn server in a subprocess
    server_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    time.sleep(3)
    
    print("Creating public tunnel via localhost.run...")
    
    # Run SSH tunnel to localhost.run
    tunnel_process = subprocess.Popen(
        ["ssh", "-o", "StrictHostKeyChecking=no", "-R", "80:localhost:8000", "nokey@localhost.run"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    # Read output to find the URL
    def print_url():
        for line in iter(tunnel_process.stdout.readline, ''):
            if "localhost.run" in line and "tunneled with tls termination" in line:
                url = re.search(r'(https://[^\s]+)', line)
                if url:
                    public_url = url.group(1)
                    print("=" * 60)
                    print(f"✅ Your website is now live in public!")
                    print(f"👉 Share this URL with your students: {public_url}")
                    print("=" * 60)
                    print("Press Ctrl+C to stop the server and close the tunnel.")
                    
                    # Create a Windows URL shortcut file
                    shortcut_content = f"[InternetShortcut]\nURL={public_url}\n"
                    shortcut_path = os.path.join(os.path.dirname(__file__), "Public_Link.url")
                    with open(shortcut_path, "w") as f:
                        f.write(shortcut_content)
                    print(f"✅ Saved shortcut to {shortcut_path}")
            elif "Connection refused" in line or "error" in line.lower():
                print(f"Tunnel log: {line.strip()}")
                
    threading.Thread(target=print_url, daemon=True).start()

    try:
        server_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        tunnel_process.terminate()
        server_process.terminate()

if __name__ == "__main__":
    main()
