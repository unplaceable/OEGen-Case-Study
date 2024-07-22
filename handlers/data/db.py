import os
import pandas as pd

class Data:
    
    def __init__(self, table):
        self.table = table
        self.file_path = os.path.join('mock_data', f'{table}.csv')
        self.data_frame = pd.read_csv(self.file_path)
        
    def get_row_by_id(self, id):
        """
        Retrieve a row by its ID.
        """
        row = self.data_frame[self.data_frame['ID'] == id]
        return row.to_dict('records')
    
    def add_record(self, new_record):
        """
        Add a new record to the CSV file.
        """
        new_df = pd.DataFrame([new_record])
        self.data_frame = pd.concat([self.data_frame, new_df], ignore_index=True)
        self.data_frame.to_csv(self.file_path, index=False)
        
    def get_all(self, return_type='df'):
        """
        Retrieve all records from the CSV file.
        """

        if return_type=='raw':
            return self.data_frame.to_dict('records')
        elif return_type=='df':
            return pd.read_csv(self.file_path)
    
    def find(self, column=None, value=None, return_type='df', include_columns=None, exclude_columns=None):
        """
        Find records based on a specific column and value, case insensitive.
        Returns only the specified columns if include_columns is provided,
        or excludes the specified columns if exclude_columns is provided.
        """
        if column not in self.data_frame.columns:
            raise ValueError(f"Column '{column}' does not exist in the data.")
        
        matching_rows = self.data_frame[self.data_frame[column].astype(str).str.contains(value, case=False, regex=False)]
        
        if include_columns:
            matching_rows = matching_rows[include_columns]
        elif exclude_columns:
            matching_rows = matching_rows.drop(columns=exclude_columns)
        
        if return_type == 'raw':
            return matching_rows.to_dict('records')
        else:
            return matching_rows

    def search(self, query_text, return_type='df', include_columns=None, exclude_columns=None):
        """
        Search for records containing the query text in any field.
        Returns only the specified columns if include_columns is provided,
        or excludes the specified columns if exclude_columns is provided.
        """
        matching_rows = self.data_frame[self.data_frame.apply(lambda row: row.astype(str).str.contains(query_text, case=False, regex=False).any(), axis=1)]
        
        if include_columns:
            matching_rows = matching_rows[include_columns]
        elif exclude_columns:
            matching_rows = matching_rows.drop(columns=exclude_columns)
        
        if return_type == 'raw':
            return matching_rows.to_dict('records')
        else:
            return matching_rows

    def bulk_update(self, updates_df):
        """
        Bulk update the data with the given DataFrame.
        """
        # Check if the updates DataFrame has the same columns as the existing DataFrame
        if not all(col in self.data_frame.columns for col in updates_df.columns):
            raise ValueError("Updates DataFrame must have the same columns as the existing DataFrame.")
        
        # Set 'id' as the index for merging
        self.data_frame.set_index('ID', inplace=True)
        updates_df.set_index('ID', inplace=True)
        
        # Update the existing data with the updates
        self.data_frame.update(updates_df)
        
        # Reset the index to default
        self.data_frame.reset_index(inplace=True)
        
        # Save the updated DataFrame back to the CSV file
        self.data_frame.to_csv(self.file_path, index=False)