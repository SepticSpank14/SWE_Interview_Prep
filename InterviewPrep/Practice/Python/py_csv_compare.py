import pandas as pd
import os
from datetime import datetime
from packaging import version

csv1 = pd.read_csv('C:\\Data\\publisher_builds.csv')
csv2 = pd.read_csv('C:\\Data\\platform_builds.csv')
log_file_path = "C:\\Logs\\build_comparison.log"

# don't forget to create the log file if it doesn't exist, 
# otherwise the script will throw an error when trying to write to a 
# non-existent file. You can do this by adding a simple check at the 
# beginning of your script:
os.makedirs(os.path.dirname(log_file_path), exist_ok=True) # creates the directory if it doesn't exist

def log (message, log_file_path):
    with open(log_file_path, "a") as f:
        f.write(f"{message}\n")

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Read two CSV files - publisher_builds.csv and platform_builds.csv - 
# both have two columns, a game_title and a build_version.
results = []

# Merge the two CSV files on the game_title column, 
# adding suffixes to distinguish between the publisher and platform build versions.
merged = pd.merge(
    csv1,
    csv2,
    on="game_title",
    how="outer", # keeps all rows from both Dataframes
    suffixes=("_publisher", "_platform"),
)

#using packaging library, convert build version strings to numbers
#numbers should be converted BEFORE the comparison is made, 
# otherwise the comparison will be done on strings and not numbers, 
# which will lead to incorrect results.
merged["build_version_publisher"] = merged["build_version_publisher"].apply(version.parse)
merged["build_version_platform"] = merged["build_version_platform"].apply(version.parse)

# Compares build versions for matching game titles
# Create a a set where all the game titles that have a higher build version 
# in the publisher CSV than in the platform CSV are added to this set.
updates_needed = merged[
    merged["build_version_publisher"] > merged["build_version_platform"]
    ]

# Writes any mismatches to an output file called update_required.csv with 
# three columns: game_title, platform_version, publisher_version
updates_needed.to_csv(
    r"C:\Data\update_required.csv", 
    columns=["game_title", "build_version_platform", "build_version_publisher"], 
    index=False)

# Logs each comparison result with a timestamp to C:\Logs\build_comparison.log
for index, row in merged.iterrows():
    if pd.isna(row["build_version_publisher"]) or pd.isna(row["build_version_platform"]):
        log(f"{timestamp()} - {row['game_title']}: Publisher or platform version missing. Please update version.", log_file_path)
        results.append(False) # FIRST CHECK for missing values before comparing
    elif row["build_version_publisher"] == row["build_version_platform"]:
        log(f"{timestamp()} - {row['game_title']}: Build versions match", log_file_path)
        results.append(True)
    elif row["build_version_publisher"] > row["build_version_platform"]:
        log(f"{timestamp()} - {row['game_title']}: Publisher version is higher. Please update version.", log_file_path)
        results.append(False)
    else:
        log(f"{timestamp()} - {row['game_title']}: Unspecified error.", log_file_path)
        results.append(False)
# Prints a summary at the end — how many games checked, how many updates required

total = len(merged)
updates = len(updates_needed)
log(f"[{timestamp()}] SUMMARY: {total} games checked. {updates} updates required.", log_file_path)
print(f"Games checked: {total} | Updates required: {updates}")