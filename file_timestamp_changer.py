import argparse
import datetime
import os
import sys
from typing import Optional, Tuple

try:
    import win32file
    import win32con
    import pywintypes
except ImportError:
    print("Error: This script requires the pywin32 package.")
    print("Install it using: pip install pywin32")
    sys.exit(1)


def change_file_timestamp(
    file_path: str,
    new_date: datetime.datetime,
    change_creation: bool = True,
    change_access: bool = True,
    change_modified: bool = True
) -> bool:
    """
    Change the timestamps of a file.
    
    Args:
        file_path: Path to the file to modify
        new_date: New datetime to set
        change_creation: Whether to change creation time
        change_access: Whether to change last access time
        change_modified: Whether to change last modified time
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Convert the datetime to Windows format
        win_time = pywintypes.Time(new_date)
        
        # Get existing file times to preserve timestamps that shouldn't change
        h_existing = win32file.CreateFile(
            file_path,
            win32con.GENERIC_READ,
            win32con.FILE_SHARE_READ,
            None,
            win32con.OPEN_EXISTING,
            win32con.FILE_ATTRIBUTE_NORMAL,
            None
        )
        
        existing_times = win32file.GetFileTime(h_existing)
        h_existing.close()
        
        # Determine which timestamps to update
        creation_time = win_time if change_creation else existing_times[0]
        access_time = win_time if change_access else existing_times[1]
        modified_time = win_time if change_modified else existing_times[2]
        
        # Open the file for writing
        handle = win32file.CreateFile(
            file_path,
            win32con.GENERIC_WRITE,
            0,  # No sharing
            None,  # Default security
            win32con.OPEN_EXISTING,
            win32con.FILE_ATTRIBUTE_NORMAL,
            None  # No template file
        )
        
        # Set the file times
        win32file.SetFileTime(handle, creation_time, access_time, modified_time)
        handle.close()
        return True
        
    except pywintypes.error as e:
        print(f"Windows Error: {e}")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def parse_date_string(date_string: str) -> Optional[datetime.datetime]:
    """
    Parse a date string into a datetime object.
    
    Supports formats:
    - YYYY-MM-DD
    - YYYY-MM-DD HH:MM:SS
    
    Args:
        date_string: The date string to parse
        
    Returns:
        A datetime object or None if parsing failed
    """
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%Y %H:%M",
        "%m/%d/%Y"
    ]
    
    for fmt in formats:
        try:
            return datetime.datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    
    return None


def main():
    """Main function to parse arguments and change file timestamps."""
    parser = argparse.ArgumentParser(
        description="Change file timestamps on Windows",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument("-f", "--file", required=True, help="Path to the file to modify")
    parser.add_argument("-d", "--date", required=True, 
                        help="New date in format 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'")
    parser.add_argument("-c", "--creation", action="store_true", 
                        help="Change only creation time")
    parser.add_argument("-a", "--access", action="store_true", 
                        help="Change only access time")
    parser.add_argument("-m", "--modified", action="store_true", 
                        help="Change only modification time")
    
    args = parser.parse_args()
    
    # Validate file exists
    if not os.path.isfile(args.file):
        print(f"Error: File '{args.file}' does not exist.")
        return False
    
    # Parse the date
    new_date = parse_date_string(args.date)
    if not new_date:
        print(f"Error: Could not parse date '{args.date}'.")
        print("Supported formats: YYYY-MM-DD or YYYY-MM-DD HH:MM:SS")
        return False
    
    # Determine which timestamps to change
    # If none specified, change all
    change_creation = True
    change_access = True
    change_modified = True
    
    if args.creation or args.access or args.modified:
        change_creation = args.creation
        change_access = args.access
        change_modified = args.modified
    
    # Change the timestamps
    success = change_file_timestamp(
        args.file,
        new_date,
        change_creation,
        change_access,
        change_modified
    )
    
    if success:
        timestamp_types = []
        if change_creation:
            timestamp_types.append("creation")
        if change_access:
            timestamp_types.append("access")
        if change_modified:
            timestamp_types.append("modification")
        
        timestamps_str = ", ".join(timestamp_types)
        print(f"Successfully changed {timestamps_str} timestamp(s) of '{args.file}' to {new_date}.")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
