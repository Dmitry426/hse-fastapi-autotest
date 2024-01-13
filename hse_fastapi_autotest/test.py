original_string = "This is a {pk} string with {gk} curly braces."

# Dictionary with values
param_values = {"pk": 1, "gk": "example"}

# Replace placeholders with corresponding values
modified_string = original_string.format(**param_values)

print(modified_string)
