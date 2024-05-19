# Funscript Processing and Renaming Script

This Python script automates the process of fetching metadata for Funscript files and renaming them based on the metadata.

## Features

- Fetch metadata for Funscript files from the SLR API.
- Rename Funscript files based on metadata (title, paysite, resolution, ID).
- Handle duplicates during renaming (skip, replace, or rename).
- Clean and format title and paysite name by to ensure we have proper file names.

## Prerequisites

- Python 3.x installed on your system.

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/funscript-processing.git
   ```

2. Navigate to the cloned directory:

   ```bash
   cd funscript-processing
   ```

3. Run the setup script to create a virtual environment and install dependencies:

   ```bash
   python setup.py
   ```

4. Activate the virtual environment:

   On Unix/Linux/macOS:
   ```bash
   source venv/bin/activate
   ```

   On Windows:
   ```bash
   venv\Scripts\activate
   ```

## Usage

1. Place your Funscript files in the same directory as the script.

2. Run the script with the desired options:

   ```bash
   python process.py [--dupe {skip,replace,rename}]
   ```

   - `--dupe {skip,replace,rename}`: Action to take if a file with the new name already exists (default is `skip`).

3. The script will process the files in two phases:
   - **Phase 1: Getting Meta Data**: Fetch metadata for each Funscript file from the SLR API.
   - **Phase 2: Renaming**: Rename Funscript files based on the fetched metadata.

## Configuration

- `X`: Delay between requests in seconds (default is 2).
- Directories:
  - `./done`: Directory for final renamed Funscript files.
  - `./done/json`: Directory to store JSON metadata files.
  - `./processed`: Directory for files we processed through the API.
  - `./not_found`: Directory for files for which metadata could not be found.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This script was inspired by the need to automate the processing and renaming of Funscript files.
- Special thanks to the developers of the `requests` and `tqdm` libraries for their contributions.
