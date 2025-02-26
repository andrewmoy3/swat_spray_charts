import pandas as pd
import re

# Example roster DataFrame
roster = pd.DataFrame({
    "First Name": ["John", "Alex", "Emily"],
    "Last Name": ["Doe", "Smith", "Johnson"]
})
def get_full_name(name, roster):
    for index, row in roster.iterrows():
        first_name = row['First Name']
        last_name = row['Last Name']
        full_name = f"{first_name} {last_name}"
        
        if re.fullmatch(r'[A-Z]\. [A-Z][a-z]+', name):
            if name == f"{first_name[0]}. {last_name}":
                return full_name

        # Match "First Last"
        elif re.fullmatch(r'[A-Z][a-z]+ [A-Z][a-z]+', name):
            if name == full_name:
                return full_name

        # Match "Last, First"
        elif re.fullmatch(r'[A-Z][a-z]+, [A-Z][a-z]+', name):
            if name == f"{last_name}, {first_name}":
                return full_name

    return ""

print(get_full_name("J. Doe", roster))     # Output: "John Doe"
print(get_full_name("Alex Smith", roster)) # Output: "Alex Smith"
print(get_full_name("Smith, Alex", roster)) # Output: "Alex Smith"
print(get_full_name("Unknown Name", roster)) # Output: None
