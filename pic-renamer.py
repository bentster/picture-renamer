
import argparse
import os
from PIL import Image
from datetime import datetime
from datetime import timedelta
from dateutil import parser
from shutil import copyfile

def start(source_dir, target_dir, hour_diff=0):
    print("Source: {} Target: {} Hourdiff: {}".format( source_dir, target_dir, hour_diff))
    files = sorted([f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))])
    for f in files:
        path_to_file = os.path.join(source_dir, f)
        original_extension = f.split('.')[-1]
        date = get_exif_date_taken(path_to_file)
        parsed_date = datetime.strptime(date, '%Y:%m:%d %H:%M:%S')
        delta = timedelta(hours=hour_diff)
        newdate = parsed_date + delta
        new_filename = newdate.strftime('%Y-%m-%d %H.%M.%S') + "." + original_extension
        print("Copying file {} with EXIF datetime {} to file {}".format(f, date, new_filename))
        copyfile(path_to_file, os.path.join(target_dir, new_filename))

def get_exif_date_taken(path):
    return Image.open(path)._getexif()[36867]

def main():
    parser = argparse.ArgumentParser(description='Works magic to create thumbnails')
    parser.add_argument('-s', '--source_dir', type=str, help='Name of source folder', required=True)
    parser.add_argument('-t', '--target_dir', type=str, help='Name of target folder', required=True)
    parser.add_argument('-d', '--hour_diff', type=int, help='Add hours to date', required=True)

    parsed_args = parser.parse_args()

    if not parsed_args.source_dir:
        print("Source dir required")
        exit(1)
    if not parsed_args.target_dir:
        print("Target dir required")
        exit(1)    
    
    start(parsed_args.source_dir, parsed_args.target_dir, parsed_args.hour_diff)


if __name__ == "__main__":
    main()