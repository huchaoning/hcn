import subprocess
import platform

__all__ = ['cpuid']

def cpuid():
    system = platform.system().lower()
    if system == "windows":
        return _cpuid_windows()
    elif system == "darwin":
        return _cpuid_macos()
    return None

def _cpuid_windows():
    try:
        cpu_id = subprocess.check_output("wmic cpu get processorid", shell=True).decode().strip().split("\n")[1]
        return cpu_id
    except Exception as e:
        print(f"Failed to get CPU ID (Windows): {e}")
        return None

def _cpuid_macos():
    try:
        serial_number = subprocess.check_output("system_profiler SPHardwareDataType | grep 'Serial Number (system)'", shell=True).decode().strip().split(":")[1].strip()
        return serial_number
    except Exception as e:
        print(f"Failed to get hardware serial number (macOS): {e}")
        return None

