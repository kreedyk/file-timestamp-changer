# File Timestamp Changer for Windows

This tool allows you to easily modify the creation, access, and modification timestamps of files on Windows systems. It's particularly useful for changing timestamps of executable files or any other file type.

## Features

- Change creation, last access, and last modification timestamps
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

Basic usage:

```
python file_timestamp_changer.py -f "path/to/file.exe" -d "2014-01-01 12:00:00"
```

### Command Line Arguments

- `-f, --file`: Path to the file to modify (required)
- `-d, --date`: New date in format 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS' (required)
- `-c, --creation`: Change only creation time
- `-a, --access`: Change only access time
- `-m, --modified`: Change only modification time

If none of the `-c`, `-a`, or `-m` options are specified, all timestamps will be changed.

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

## Supported Date Formats

The script supports multiple date formats:
- YYYY-MM-DD
- YYYY-MM-DD HH:MM:SS
- YYYY-MM-DD HH:MM
- DD/MM/YYYY
- MM/DD/YYYY

## Use Cases

- Forensics education and training
- Software development testing (testing date-dependent functionality)
- File organization and archiving
- Digital preservation projects

## Disclaimer

This tool is provided for educational and legitimate purposes only. Altering file timestamps may have legal implications in certain contexts. Users are responsible for ensuring they use this tool in accordance with applicable laws and regulations.
