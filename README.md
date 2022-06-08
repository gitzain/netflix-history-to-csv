# netflix-history-to-csv
Python script that screen scrapes your Netflix viewing/watch history and puts it in a CSV file.

## Table of content
- [Motivation](#motivation)
- [Installation & Usage](#installation--usage)
    - [Installation](#installation)
    - [Usage](#usage)
- [Contributing](#contributing)
- [History](#history)
- [Credits](#credits)
- [License](#license)

## Motivation
I wanted to programmatically grab my Netflix viewing/watch history because ultimately i want to update my trakt account. 

## Installation & Usage

### Installation
1. Download the contents of this repository. You can do this by clicking "Code" > "Download ZIP".
2. Unzip the contents of the ZIP file.
3. You'll need to know how to run a python program/script on your OS. For mac/linux, open up a terminal window and navigate to the folder you just unzipped in step 2 using the "CD" command.
4. You'll need to install the pre-requistes. You can do this by:
```bash
pip install -r requirements.txt
```
5. You're ready to run the script.

### Usage
To get all your history:
```bash
python netflix-history-to-csv.py --username <Replace this with your Netflix email address> --password <Replace this with your Netflix password> --profile <Replace this with the profile inside the Netflix account your want the history of>
```

To get only the last 7 days of your history:
```bash
python netflix-history-to-csv.py --username <Replace this with your Netflix email address> --password <Replace this with your Netflix password> --profile <Replace this with the profile inside the Netflix account your want the history of> --history 7 
```

## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -m 'Added some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History
07/06/22: v1 published to github.

## Credits
- Template for this README is <a href="https://github.com/gitzain/template-README">Template-README</a> created by <a href="https://iamzain.com">Zain Khan</a>
- Inspired by <a href="https://github.com/ManveerBasra/ActivityExtractor">ActivityExtractor</a> by <a href="https://github.com/ManveerBasra">Manveer Basra</a>

## License
See the LICENSE file in this project's directory.