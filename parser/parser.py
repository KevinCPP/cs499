import re
import os

if __name__ == "__main__":
    from file_io import *
    from line_rule import *
else:
    from parser.file_io import *
    from parser.line_rule import *

import pandas as pd
import matplotlib.pyplot as plt


class Parser:
    def __init__(self):
        # pattern for 9 digit numbers
        self.ssn_pattern = r'\b\d{9}\b'
        # for dates such as 07/06/2000
        ddmmyyyy = r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b'
        # for dates such as 2000/07/06
        yyyymmdd = r'\b\d{2,4}[-/]\d{1,2}[-/]\d{1,2}\b'
        # combined pattern for detecting dates
        self.date_pattern = f'({ddmmyyyy})|({yyyymmdd})'

    # strips html from the input string and returns the cleaned text
    def remove_html(self, input_string, replace_with=' '):
        pattern = '<.*?>'
        clean_text = re.sub(pattern, replace_with, input_string)
        pattern = '{.*?}'
        clean_text = re.sub(pattern, replace_with, clean_text)
        pattern = '&.*?;'
        clean_text = re.sub(pattern, replace_with, clean_text)
        return clean_text

    def _group_substr(self, input_string, start_matches, end_matches) -> list:
        # build up a list/stack containing all of the substrings
        substrings = []
        # no end position has been encountered yet, initialize to -1
        end_pos_last = -1

        # iterate through all start matches (start, end) indices
        for start_pos, start_end in start_matches:
            # if the start of this start match is before the end of the last
            # ending position, ignore. This will not be counted for the first
            # starting pos since end_pos_last is initialized to -1
            if start_pos < end_pos_last:
                continue
            
            # iterate through end positions, finding the first one that is after this start_pos
            for end_pos, end_end in end_matches:
                if end_pos >= start_end:
                    # add the substring to the list of solutions
                    substrings.append(input_string[start_pos:end_end])
                    # update last ending flag that was found
                    end_pos_last = end_end
                    break
        
        # return all of the substrings
        return substrings
    
    # return all substrings which start with start_regex and end with end_regex (not inclusive)
    def get_excerpt(self, input_string, start_regex, end_regex) -> list:
        # Find all matches for start and end regex
        start_matches = [(match.start(), match.end()) for match in re.finditer(start_regex, input_string)]
        end_matches = [(match.start(), match.end()) for match in re.finditer(end_regex, input_string)]

        # return the matches
        return self._group_substr(input_string, start_matches, end_matches)
    
    # return all substrings which start with the start_line_rule and end with the end_line_rule
    def get_section(self, input_string, start_line_rule, end_line_rule) -> list:
        # Find all matches for start/end line rules
        start_matches = start_line_rule(input_string)
        end_matches = end_line_rule(input_string)
        
        # build up a list/stack containing all of the substrings
        substrings = []
        # no end position has been encountered yet, initialize to -1
        end_pos_last = -1

        # iterate through all start matches (start, end) indices
        for start_pos, start_end in start_matches:
            # if the start of this start match is before the end of the last
            # ending position, ignore. This will not be counted for the first
            # starting pos since end_pos_last is initialized to -1
            if start_pos < end_pos_last:
                continue
            
            # iterate through end positions, finding the first one that is after this start_pos
            for end_pos, end_end in end_matches:
                if end_pos >= start_end:
                    lines = input_string.splitlines()
                    # add the substring to the list of solutions
                    substrings.append("\n".join(lines[start_pos:end_end]))
                    # update last ending flag that was found
                    end_pos_last = end_end
                    break
        
        # return all of the substrings
        return substrings

    def get_patients(self, input_string) -> list:
        return self.get_section(self.remove_html(input_string), lr_dob_and_ssn, lr_two_blank_lines)

    def extract_ages(self, patient_sections):
        age_dict = {'Email': [], 'Age': []}
        # Regex pattern to match ages followed by various indicators, case-insensitively
        age_pattern = re.compile(r"\b(\d{1,3})\s*(years? old|y\.o\.|yo|YOM|YOF|yM|yF|M|F|y/o)\b", re.IGNORECASE)
        
        for i, patient_section in enumerate(patient_sections, start=1):
            # Initialize first_age to None for each patient section
            first_age = None
            
            # Search the entire text for the patterns
            matches_age = age_pattern.findall(patient_section)
            age_dict['Email'].append(i)
            
            # Extract the first valid match (non-empty) for Age
            for match in matches_age:
                if match[0]:  # If the first group matched
                    first_age = match[0]  # Capture the first age found
                    break  # Exit loop after finding the first age
            
            # Append the first age found or None if no match was found
            if first_age != None:
                age_dict['Age'].append(int(first_age))
            else:
                age_dict['Age'].append(first_age)
        # Return the dictionary containing the first match for Age
        return age_dict


    
    def extract_VA(self, patient_sections):
        od_dict = {'Email': [], 'OD': []}
        os_dict = {'Email': [], 'OS': []}
        # Regex pattern to match "OD 20/___" and similarly for "OS"
        pattern_od = re.compile(r"OD.*?(20/\d+)")
        pattern_os = re.compile(r"OS.*?(20/\d+)")

        for i, patient_section in enumerate(patient_sections, start=1):
            # Reset the first "20/___" pattern found for each key for each patient section
            first_number_after_od = None
            first_number_after_os = None

            # Search the entire text for the first "20/___" pattern for OD and OS
            match_od = pattern_od.search(patient_section)
            match_os = pattern_os.search(patient_section)

            if match_od:
                first_number_after_od = match_od.group(1)  # The first valid "20/___" following "OD"

            if match_os:
                first_number_after_os = match_os.group(1)  # The first valid "20/___" following "OS"

            # Append the extracted values and their corresponding email index to the dictionaries
            od_dict['Email'].append(i)
            os_dict['Email'].append(i)
            od_dict['OD'].append(first_number_after_od if first_number_after_od else None)
            os_dict['OS'].append(first_number_after_os if first_number_after_os else None)

        # Return the dictionaries containing the first match for OD and OS for each patient section
        return od_dict, os_dict

    # Process email files and create dataframes
    def process_file(self, file_path):
        success, text = file_in(file_path)
        if not success:
            print(f"Failed to read email from {file_path}")
            return None

        parser = Parser()
        patients = parser.get_patients(text)

        age = parser.extract_ages(patients)
        od, os = parser.extract_VA(patients)

        # Create DataFrames
        age_df = pd.DataFrame(age)
        os_df = pd.DataFrame(os)
        od_df = pd.DataFrame(od)

        # Merge DataFrames
        merged_df1 = pd.merge(age_df, os_df, left_index=True, right_index=True)
        merged_df = pd.merge(merged_df1, od_df, left_index=True, right_index=True)

        return merged_df


    def plot_eyesight_age(self, files):
        dfs = []
        for file_name in files:
            if os.path.isfile(file_name):
                df = self.process_file(file_name)
                if df is not None:
                    dfs.append(df)

        # Concatenate all the DataFrames into a single one
        df = pd.concat(dfs, ignore_index=True)
        dropped_na_df = df.dropna()
        #print(dropped_na_df)
        
        # Save df to a csv file
        dropped_na_df.to_csv('final_output.csv', index=False)
        print("Results saved to final_output.csv.")

        # Copy the DataFrame explicitly
        new_cols_df = dropped_na_df.copy()

        # Use .loc to avoid SettingWithCopyWarning
        new_cols_df.loc[:, 'OD_denominator'] = dropped_na_df['OD'].str.extract(r'20/(\d+)').astype(float)
        new_cols_df.loc[:, 'OS_denominator'] = dropped_na_df['OS'].str.extract(r'20/(\d+)').astype(float)
        final_df = new_cols_df.sort_values(by='Age', ascending=True)
        #print(len(final_df))

        #----------------------------------Graphing--------------------------------------
        plt.figure(figsize=(10, 6))
        plt.plot(final_df['Age'], final_df['OD_denominator'], 'o-', label='OD')
        plt.plot(final_df['Age'], final_df['OS_denominator'], 's-', label='OS')

        plt.xlabel('Age')
        plt.ylabel('Denominator of VA (20/X)')
        plt.title('Visual Acuity Denominator vs Age')
        plt.legend()
        plt.grid(True)
        plt.show()


#-----------------------------------MAIN--------------------------------
if __name__ == "__main__":
    directory_path = '/home/fornzltoth/Documents/Programming/499/converted_messages'  # Adjust as needed
    all_files = os.listdir(directory_path)
    parser = Parser()
    dfs = []  # List to store DataFrames from all files

    for file_name in all_files:
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path):
            df = parser.process_file(file_path)
            if df is not None:
                dfs.append(df)
    
    # Concatenate all the DataFrames into a single one
    df = pd.concat(dfs, ignore_index=True)
    dropped_na_df = df.dropna()
    print(dropped_na_df)
    
    # Save df to a csv file
    dropped_na_df.to_csv('final_output.csv', index=False)
    print("Results saved to final_output.csv.")

    # Copy the DataFrame explicitly
    new_cols_df = dropped_na_df.copy()

    # Use .loc to avoid SettingWithCopyWarning
    new_cols_df.loc[:, 'OD_denominator'] = dropped_na_df['OD'].str.extract(r'20/(\d+)').astype(float)
    new_cols_df.loc[:, 'OS_denominator'] = dropped_na_df['OS'].str.extract(r'20/(\d+)').astype(float)
    final_df = new_cols_df.sort_values(by='Age', ascending=True)
    print(len(final_df))

    #----------------------------------Graphing--------------------------------------
    plt.figure(figsize=(10, 6))
    plt.plot(final_df['Age'], final_df['OD_denominator'], 'o-', label='OD')
    plt.plot(final_df['Age'], final_df['OS_denominator'], 's-', label='OS')

    plt.xlabel('Age')
    plt.ylabel('Denominator of VA (20/X)')
    plt.title('Visual Acuity Denominator vs Age')
    plt.legend()
    plt.grid(True)
    plt.show()
