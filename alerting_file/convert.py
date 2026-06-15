import yaml
import json
import os

input_dir = 'alerting_file'
output_dir = 'json_output'

os.makedirs(output_dir, exist_ok=True)

for file in os.listdir(input_dir):
    if file.endswith('.yaml') or file.endswith('.yml'):
        with open(f'{input_dir}/{file}', 'r') as f:
            data = yaml.safe_load(f)
        
        json_file = file.replace('.yaml', '.json').replace('.yml', '.json')
        with open(f'{output_dir}/{json_file}', 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Converted: {file} → {json_file}")
