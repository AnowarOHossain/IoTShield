"""
Run Multiple IoT Device Simulators
Starts both ESP32 and Raspberry Pi simulators
"""
import subprocess
import time
import sys
import os

def main():
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║      IoTShield Multi-Device Simulator Manager       ║
    ╚══════════════════════════════════════════════════════╝
    
    Starting multiple device simulators...
    """)
    
    # Get the simulator directory
    sim_dir = os.path.dirname(os.path.abspath(__file__))
    
    try:
        # Start ESP32 simulator in a separate process
        print("\n[1/2] Starting ESP32 Simulator...")
        esp32_process = subprocess.Popen(
            [sys.executable, os.path.join(sim_dir, 'simulator.py')],
            cwd=sim_dir
        )
        time.sleep(2)
        
        # Start Raspberry Pi simulator in a separate process
        print("[2/2] Starting Raspberry Pi Simulator...")
        rpi_process = subprocess.Popen(
            [sys.executable, os.path.join(sim_dir, 'rpi_simulator.py')],
            cwd=sim_dir
        )
        
        print("""
    ╔══════════════════════════════════════════════════════╗
    ║              Both Simulators Running!                ║
    ║                                                      ║
    ║  Device 1: ESP32 - Living Room Sensor Hub           ║
    ║  Device 2: Raspberry Pi - Kitchen Edge Gateway      ║
    ║                                                      ║
    ║  Press Ctrl+C to stop all simulators                ║
    ╚══════════════════════════════════════════════════════╝
        """)
        
        # Wait for both processes
        esp32_process.wait()
        rpi_process.wait()
        
    except KeyboardInterrupt:
        print("\n\nStopping all simulators...")
        esp32_process.terminate()
        rpi_process.terminate()
        print("All simulators stopped.")
    
    except Exception as e:
        print(f"\nError: {e}")
        if 'esp32_process' in locals():
            esp32_process.terminate()
        if 'rpi_process' in locals():
            rpi_process.terminate()

if __name__ == '__main__':
    main()
