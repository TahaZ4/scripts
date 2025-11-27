#!/usr/bin/env python3
"""
Check NTUSER.DAT for recent user activity
"""

from Registry import Registry

def analyze_ntuser():
    print("=== NTUSER.DAT USER ACTIVITY ===")
    print("-" * 40)
    
    try:
        reg = Registry.Registry("NTUSER.DAT.copy0")
        
        # Recent Run Commands
        try:
            runmru = reg.open("Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU")
            print("Recent Run Commands:")
            for value in runmru.values():
                if value.name() != "MRUList":
                    print(f"  - {value.value()}")
        except:
            print("Run Commands: Not found")
        
        # Recent Documents
        try:
            recent = reg.open("Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RecentDocs")
            print(f"\nRecent Documents Tracked: {len(recent.values()) - 1} files")
        except:
            print("Recent Documents: Not found")
            
    except Exception as e:
        print(f"Error: {e}")

analyze_ntuser()