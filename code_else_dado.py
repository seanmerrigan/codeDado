__author__ = "steve.thorpe"

"""
Based on sean.merrigan's code_dado.py.
Added capability to process an "ELSE" delimiter.
"""

import sys

open_delimiter = '/*--['
delimiters = ['BEGIN:', 'ELSE:', 'END:']
close_delimiter = ']--*/'

def main():
    print ('Starting.')
    source_filename, target_filename, tag_names = get_args()
    new_file = get_file_with_tags_omitted(read_file(source_filename), tag_names)
    write_file(target_filename, new_file)


def get_args():
    # Get paramiters: source_filename, target_filename, tag_name_one, ... tag_name_n
    try:
        source_filename = sys.argv[1]
        target_filename = sys.argv[2]
        valid_tag_names = []
        for tag_name in sys.argv[3:]:
            valid_tag_names.append(tag_name)
        # todo: validation
        return [source_filename, target_filename, valid_tag_names]
    except:
        print ( 'code_else_dado source_filename, target_filename, tag_name_one, ... tag_name_n' )


def read_file(filename):
    f = open(filename, 'r')
    file_content = f.readlines()
    f.close()
    return file_content


def write_file(filename, file_content):
    f = open(filename, 'w')
    for line in file_content:
        f.write(line)
    f.close
    print('Wrote file to ' + filename)

def action_tag(line, tag_names):
    for delimiter in delimiters:
        if open_delimiter + delimiter in line and close_delimiter in line:
            tag = line.strip().strip(open_delimiter+delimiter+close_delimiter)
            return delimiter, tag, tag in tag_names
    return None, None, False

def get_file_with_tags_omitted(source_file, valid_tag_names):
    new_file_content = []
    currently_deleting_tag = False
    currently_keeping_tag = False
    for line in source_file:
        action, tag, include = action_tag(line, valid_tag_names)
        if currently_deleting_tag:
            if action is None:
                new_file_content.append('\r\n')  # Maintain line numbers for debugging (it's ok: prod file will be minified)
            else:
                new_file_content.append(line) # Keep all tags for clarity while debugging: they too will be minified away later
                if action in ["END:", "ELSE:"]:
                    currently_deleting_tag = False
                elif action in ["ELSE:"]:
                    currently_keeping_tag = tag
        elif currently_keeping_tag:
            new_file_content.append(line)
            if action in ["END:", "ELSE:"]:
                currently_keeping_tag = False
            if action in ["ELSE:"]:
                currently_deleting_tag = tag
        else:
            # copying un-tagged code
            new_file_content.append(line)
            if action == "BEGIN:":
                currently_keeping_tag = include
                currently_deleting_tag = not include
                
    return new_file_content

if __name__ == "__main__":
    main()
