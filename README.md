# File Timestamp Changer for Windows

This tool allows you to easily modify the creation, access, and modification timestamps of files on Windows systems. It's particularly useful for changing timestamps of executable files or any other file type.

![picture](https://i.imgur.com/AZDrtUO.png)

## Features

- Change creation, last access, and last modification timestamps
- Copy timestamps from another file
- Interactive mode for easier usage
- Option to change only specific timestamps (creation, access, or modification)
- Command-line interface for easy integration into workflows
- Support for various date formats
- Comprehensive error handling

## Requirements

- Python 3.6+
- pywin32 package

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/kreedyk/file-timestamp-changer.git
   cd file-timestamp-changer
   ```

2. Install the required package:
   ```
   pip install pywin32
   ```

## Usage

### Interactive Mode

Run the script without any arguments to enter interactive mode:
```
python file_timestamp_changer.py
```

In interactive mode, you'll be guided through a series of prompts to:
- Select the file to modify
- Choose whether to set a specific date or copy timestamps from another file
- Select which timestamps to change (creation, access, or modification)

This mode is perfect for users who prefer a guided approach rather than command-line parameters.

### Command Line Arguments

- `-f, --file`: Path to the file to modify (required)
- `-d, --date`: New date in format 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'
- `-s, --source`: Path to source file to copy timestamps from
- `-c, --creation`: Change only creation time
- `-a, --access`: Change only access time
- `-m, --modified`: Change only modification time

Notes:
- You must specify either `-d` (date) or `-s` (source file), but not both
- If none of the `-c`, `-a`, or `-m` options are specified, all timestamps will be changed

### Examples

Change all timestamps to January 1, 2014:
```
python file_timestamp_changer.py -f "program.exe" -d "2014-01-01"
```

Change only the creation time to June 15, 2019 at 2:30 PM:
```
python file_timestamp_changer.py -f "document.pdf" -d "2019-06-15 14:30:00" -c
```

Change both access and modification times, but not creation time:
```
python file_timestamp_changer.py -f "image.jpg" -d "2018-03-22" -a -m
```

Copy all timestamps from one file to another:
```
python file_timestamp_changer.py -f "destination.exe" -s "source.exe"
```

Copy only the creation timestamp from one file to another:
```
python file_timestamp_changer.py -f "destination.exe" -s "source.exe" -c
```

## Supported Date Formats

The script supports multiple date formats:
- YYYY-MM-DD
- YYYY-MM-DD HH:MM:SS
- YYYY-MM-DD HH:MM
- DD/MM/YYYY
- MM/DD/YYYY
- And variations with time components

## Use Cases

- Forensics education and training
- Software development testing (testing date-dependent functionality)
- File organization and archiving
- Digital preservation projects
- Synchronizing timestamps between related files

## Disclaimer

This tool is provided for educational and legitimate purposes only. Altering file timestamps may have legal implications in certain contexts. Users are responsible for ensuring they use this tool in accordance with applicable laws and regulations.
