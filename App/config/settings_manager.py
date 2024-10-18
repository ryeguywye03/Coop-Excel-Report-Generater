import json
import os
import pandas as pd
from utils import resource_path  # Import the centralized resource_path

class SettingsManager:
    def __init__(self, settings_file=None):
        # Use resource_path to handle dynamic paths
        if settings_file is None:
            self.settings_file = resource_path(os.path.join('assets', 'json', 'type_group_exclusion.json'))
        else:
            self.settings_file = settings_file
        self.exclusions = None

    def load_settings(self):
        """Load the current exclusions from the JSON file."""
        try:
            with open(self.settings_file, 'r') as file:
                self.exclusions = json.load(file)
            return self.exclusions
        except FileNotFoundError:
            print(f"Settings file not found: {self.settings_file}")
            return None
        except json.JSONDecodeError:
            print("Error parsing settings file.")
            return None

    def update_exclusions(self, excluded_sr_id, excluded_group_id):
        """Update the exclusions in the JSON file and save them."""
        if not self.exclusions:
            self.exclusions = self.load_settings()

        if self.exclusions:
            # Update the exclusion fields using the unique IDs
            self.exclusions['excluded_sr_type'] = excluded_sr_id
            self.exclusions['excluded_group'] = excluded_group_id

            # Write updated exclusions back to the JSON file
            try:
                with open(self.settings_file, 'w') as file:
                    json.dump(self.exclusions, file, indent=4)
                print("Exclusions updated successfully.")
            except Exception as e:
                print(f"Error saving settings: {str(e)}")
        else:
            print("No exclusions to update.")

    def create_json_from_excel(self):
        """Create or refresh the JSON file from the Excel files."""
        try:
            # Use resource_path to handle dynamic paths for the Excel files
            sr_types_file = resource_path(os.path.join('assets', 'Excel', '311_GIS_Type_Descriptions.xlsx'))
            group_descriptions_file = resource_path(os.path.join('assets', 'Excel', '311_GIS_Group_Descriptions.xlsx'))

            print(f"Reading SR Types from: {sr_types_file}")
            print(f"Reading Group Descriptions from: {group_descriptions_file}")

            sr_types_df = pd.read_excel(sr_types_file)
            group_descriptions_df = pd.read_excel(group_descriptions_file)

            # Assuming the relevant columns are named 'Description'
            sr_types = sr_types_df['Description'].tolist()
            group_descriptions = group_descriptions_df['Description'].tolist()

            # Convert to the JSON structure you're using
            data = {
                "type_descriptions": {str(i): {"description": desc} for i, desc in enumerate(sr_types, 1)},
                "group_descriptions": {str(i): {"description": desc} for i, desc in enumerate(group_descriptions, 1)}
            }

            # Write this data to the JSON file
            with open(self.settings_file, 'w') as file:
                json.dump(data, file, indent=4)

            print("Settings JSON file created/refreshed from Excel.")
        except FileNotFoundError as e:
            print(f"Excel file not found: {str(e)}")
        except Exception as e:
            print(f"Error generating JSON from Excel: {str(e)}")
