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


def get_file_timestamps(file_path: str) -> Tuple[pywintypes.Time, pywintypes.Time, pywintypes.Time]:
    """
    Get the timestamps of a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Tuple of (creation_time, access_time, modified_time)
    """
    try:
        handle = win32file.CreateFile(
            file_path,
            win32con.GENERIC_READ,
            win32con.FILE_SHARE_READ,
            None,
            win32con.OPEN_EXISTING,
            win32con.FILE_ATTRIBUTE_NORMAL,
            None
        )
        
        times = win32file.GetFileTime(handle)
        handle.close()
        return times
        
    except Exception as e:
        print(f"Error getting file timestamps: {str(e)}")
        sys.exit(1)


def change_file_timestamp(
    file_path: str,
    new_date: datetime.datetime = None,
    source_file: str = None,
    change_creation: bool = True,
    change_access: bool = True,
    change_modified: bool = True
) -> bool:
    """
    Change the timestamps of a file.
    
    Args:
        file_path: Path to the file to modify
        new_date: New datetime to set (optional if source_file is provided)
        source_file: Path to file to copy timestamps from (optional if new_date is provided)
        change_creation: Whether to change creation time
        change_access: Whether to change last access time
        change_modified: Whether to change last modified time
        
    Returns:
        True if successful, False otherwise
    """
    try:
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
        if source_file:
            # Copy timestamps from source file
            source_times = get_file_timestamps(source_file)
            creation_time = source_times[0] if change_creation else existing_times[0]
            access_time = source_times[1] if change_access else existing_times[1]
            modified_time = source_times[2] if change_modified else existing_times[2]
        else:
            # Use the specified datetime
            win_time = pywintypes.Time(new_date)
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


def interactive_mode():
    """Run the script in interactive mode with prompts for user input."""
    print("\n===== Windows File Timestamp Changer =====")
    
    # Get target file
    while True:
        target_file = input("\nEnter the path of the file you want to modify: ").strip()
        if not target_file:
            print("You must specify a file.")
            continue
        
        if not os.path.isfile(target_file):
            print(f"Error: File '{target_file}' does not exist.")
            continue
        
        break
    
    # Determine timestamp source
    print("\nChoose the timestamp source:")
    print("1. Set a specific date")
    print("2. Copy from another file")
    
    while True:
        choice = input("\nEnter your choice (1 or 2): ").strip()
        if choice not in ["1", "2"]:
            print("Please enter 1 or 2.")
            continue
        break
    
    new_date = None
    source_file = None
    
    if choice == "1":
        # Get date
        print("\nAccepted date formats: YYYY-MM-DD, YYYY-MM-DD HH:MM:SS, DD/MM/YYYY, MM/DD/YYYY")
        while True:
            date_string = input("\nEnter the new date: ").strip()
            new_date = parse_date_string(date_string)
            if not new_date:
                print(f"Error: Could not parse date '{date_string}'.")
                print("Try one of these formats: 2021-12-31, 2021-12-31 23:59:59, 31/12/2021, 12/31/2021")
                continue
            break
    else:
        # Get source file
        while True:
            source_file = input("\nEnter the path of the source file to copy timestamps from: ").strip()
            if not source_file:
                print("You must specify a source file.")
                continue
            
            if not os.path.isfile(source_file):
                print(f"Error: File '{source_file}' does not exist.")
                continue
            
            break
    
    # Determine which timestamps to change
    print("\nWhich timestamps do you want to change?")
    print("1. All (creation, access, and modification)")
    print("2. Only specific ones (choose)")
    
    while True:
        timestamp_choice = input("\nEnter your choice (1 or 2): ").strip()
        if timestamp_choice not in ["1", "2"]:
            print("Please enter 1 or 2.")
            continue
        break
    
    change_creation = True
    change_access = True
    change_modified = True
    
    if timestamp_choice == "2":
        change_creation = input("\nChange creation timestamp? (y/n): ").lower().startswith('y')
        change_access = input("Change last access timestamp? (y/n): ").lower().startswith('y')
        change_modified = input("Change last modification timestamp? (y/n): ").lower().startswith('y')
    
    # Confirm the operation
    print("\n===== Confirmation =====")
    print(f"File to modify: {target_file}")
    
    if new_date:
        print(f"New date/time: {new_date}")
    else:
        print(f"Copy timestamps from: {source_file}")
    
    timestamp_types = []
    if change_creation:
        timestamp_types.append("creation")
    if change_access:
        timestamp_types.append("access")
    if change_modified:
        timestamp_types.append("modification")
    
    print(f"Timestamps to change: {', '.join(timestamp_types)}")
    
    confirm = input("\nConfirm this operation? (y/n): ").lower()
    if not confirm.startswith('y'):
        print("Operation cancelled by user.")
        return False
    
    # Perform the operation
    success = change_file_timestamp(
        target_file,
        new_date,
        source_file,
        change_creation,
        change_access,
        change_modified
    )
    
    if success:
        if new_date:
            print(f"\nSuccessfully changed {', '.join(timestamp_types)} timestamp(s) of '{target_file}' to {new_date}.")
        else:
            print(f"\nSuccessfully copied {', '.join(timestamp_types)} timestamp(s) from '{source_file}' to '{target_file}'.")
    
    # Ask if user wants to continue with another operation
    continue_choice = input("\nDo you want to perform another operation? (y/n): ").lower()
    if continue_choice.startswith('y'):
        return interactive_mode()
    
    return success


def main():
    """Main function to parse arguments and change file timestamps."""
    # Check if no arguments provided, run interactive mode
    if len(sys.argv) == 1:
        return interactive_mode()
    
    # Otherwise, process command-line arguments
    parser = argparse.ArgumentParser(
        description="Change file timestamps on Windows",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument("-f", "--file", required=True, help="Path to the file to modify")
    
    time_source_group = parser.add_mutually_exclusive_group(required=True)
    time_source_group.add_argument("-d", "--date", 
                        help="New date in format 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'")
    time_source_group.add_argument("-s", "--source", 
                        help="Path to source file to copy timestamps from")
    
    parser.add_argument("-c", "--creation", action="store_true", 
                        help="Change only creation time")
    parser.add_argument("-a", "--access", action="store_true", 
                        help="Change only access time")
    parser.add_argument("-m", "--modified", action="store_true", 
                        help="Change only modification time")
    
    args = parser.parse_args()
    
    # Validate target file exists
    if not os.path.isfile(args.file):
        print(f"Error: File '{args.file}' does not exist.")
        return False
    
    # Validate source file exists if using --source
    if args.source and not os.path.isfile(args.source):
        print(f"Error: Source file '{args.source}' does not exist.")
        return False
    
    # Parse the date if using --date
    new_date = None
    if args.date:
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
        args.source,
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
        
        if args.source:
            print(f"Successfully copied {timestamps_str} timestamp(s) from '{args.source}' to '{args.file}'.")
        else:
            print(f"Successfully changed {timestamps_str} timestamp(s) of '{args.file}' to {new_date}.")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
