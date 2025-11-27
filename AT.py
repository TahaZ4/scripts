#!/usr/bin/env python3
"""
Windows Forensic Analyzer - Windows Compatible Version
"""

import os
import sys

try:
    from Registry import Registry
except ImportError:
    print("ERROR: Please install python-registry first:")
    print("Run: pip install python-registry")
    sys.exit(1)

def analyze_system_hive():
    """Analyze SYSTEM hive for computer info and USB devices"""
    print("=== SYSTEM HIVE ANALYSIS ===")
    print("-" * 40)
    
    try:
        reg = Registry.Registry("SYSTEM")
        
        # Computer Name
        try:
            computer = reg.open("ControlSet001\\Control\\ComputerName\\ComputerName")
            name = computer.value("ComputerName").value()
            print(f"Computer Name: {name}")
        except:
            print("Computer Name: Not found")
        
        # Time Zone
        try:
            tz = reg.open("ControlSet001\\Control\\TimeZoneInformation")
            bias = tz.value("Bias").value()
            print(f"Time Zone Bias: {bias} minutes")
        except:
            print("Time Zone: Not found")
        
        # USB Devices
        try:
            usb = reg.open("ControlSet001\\Enum\\USBSTOR")
            print("USB Devices Found:")
            for device in usb.subkeys():
                print(f"  - {device.name()}")
        except:
            print("USB Devices: None found")
            
    except Exception as e:
        print(f"Error reading SYSTEM hive: {e}")

def analyze_software_hive():
    """Analyze SOFTWARE hive for OS info and installed programs"""
    print("\n=== SOFTWARE HIVE ANALYSIS ===")
    print("-" * 40)
    
    try:
        reg = Registry.Registry("SOFTWARE")
        
        # Windows Version
        try:
            cv = reg.open("Microsoft\\Windows NT\\CurrentVersion")
            print(f"OS: {cv.value('ProductName').value()}")
            print(f"Version: {cv.value('CurrentVersion').value()}")
        except:
            print("OS Version: Not found")
        
        # Installed Programs
        try:
            uninstall = reg.open("Microsoft\\Windows\\CurrentVersion\\Uninstall")
            programs = []
            for program in uninstall.subkeys():
                try:
                    name = program.value("DisplayName").value()
                    programs.append(name)
                except:
                    continue
            
            print(f"\nInstalled Programs ({len(programs)} found):")
            for program in programs[:10]:
                print(f"  - {program}")
            if len(programs) > 10:
                print(f"  ... and {len(programs) - 10} more")
                
        except:
            print("Installed Programs: None found")
            
    except Exception as e:
        print(f"Error reading SOFTWARE hive: {e}")

def analyze_sam_hive():
    """Analyze SAM hive for user accounts"""
    print("\n=== SAM HIVE ANALYSIS ===")
    print("-" * 40)
    
    try:
        reg = Registry.Registry("SAM")
        
        try:
            sam_key = reg.open("SAM\\Domains\\Account\\Users\\Names")
            users = []
            for user in sam_key.subkeys():
                users.append(user.name())
            
            if users:
                print("User Accounts:")
                for user in users:
                    print(f"  - {user}")
            else:
                print("User Accounts: None found")
                
        except:
            print("User Accounts: Not accessible")
            
    except Exception as e:
        print(f"Error reading SAM hive: {e}")

def main():
    """Main forensic analysis function"""
    print("WINDOWS FORENSIC ANALYZER")
    print("=" * 50)
    
    # Check if files exist in current directory
    files = os.listdir('.')
    print("Files in current directory:")
    for file in files:
        print(f"  - {file}")
    
    print("\n" + "=" * 50)
    
    # Run analyses
    analyze_system_hive()
    analyze_software_hive()
    analyze_sam_hive()
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()