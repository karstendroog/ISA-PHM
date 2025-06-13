# ISA-PHM
The creating of ISA formatted data is split into two files.

# describe_experiment.py
This file asks questions to describe the experiment, it can be run using the command: python3 describe_experiment.py
The output of this file is the file experiment.json

# create_template.py
This file uses the experiment.json file to create the isa-tab or isa-json formatted data.
The file can be run with this command: python3 create_template.py experiment.json
If a tabular format is wanted add -t to the command.

# IsaPhmInfo.schema.json
This the the json schema of the experiment.json file.

# Usage
run describe_experiment.py and use the output file experiment.json as input for the create_template.py



