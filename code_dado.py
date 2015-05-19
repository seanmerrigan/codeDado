__author__ = 'sean.merrigan'

import sys

start_of_begin_delimiter = '/*--[BEGIN:'
end_of_begin_delimiter = ']--*/'
start_of_end_delimiter = '/*--[END:'
end_of_end_delimiter = ']--*/'


def main():
    print 'Starting.'
    source_filename, target_filename, tag_names = get_args()
    new_file = get_file_with_tags_omitted(read_file(source_filename), tag_names)
    write_file(target_filename, new_file)


def get_args():
    # Get parameters: source_filename, target_filename, tag_name_one, ... tag_name_n
    try:
        source_filename = sys.argv[1]
        target_filename = sys.argv[2]
        valid_tag_names = []
        for tag_name in sys.argv[3:]:
            valid_tag_names.append(tag_name)
        # todo: validation
        return [source_filename, target_filename, valid_tag_names]
    except:
        print 'code_dado source_filename, target_filename, tag_name_one, ... tag_name_n'


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


def get_file_with_tags_omitted(source_file, valid_tag_names):
    global start_of_begin_delimiter, end_of_begin_delimiter
    new_file_content = []
    currently_deleting_tag = False
    for line in source_file:
        if currently_deleting_tag is False:
            if start_of_begin_delimiter in line and end_of_begin_delimiter in line:
                if line.strip().index(start_of_begin_delimiter) == 0 and \
                        line.strip().index(end_of_begin_delimiter) == len(line.strip()) - len(end_of_begin_delimiter):
                    tag = line.strip()[len(start_of_begin_delimiter):line.strip().index(end_of_begin_delimiter)]
                    print ('Found Tag: ' + tag)
                    if tag not in valid_tag_names:
                        print ('Omitting Tag: ' + tag)
                        currently_deleting_tag = tag
        if currently_deleting_tag is False:
            new_file_content.append(line)
        else:
            new_file_content.append('\r\n')  # Maintain line numbers for debugging (it's ok: prod file will be minified)
        if start_of_end_delimiter in line and end_of_end_delimiter in line:
            if line.strip().index(start_of_end_delimiter) == 0 and \
                    line.strip().index(end_of_end_delimiter) == len(line.strip()) - len(end_of_end_delimiter):
                currently_deleting_tag = False
    return new_file_content


if __name__ == "__main__":
    main()
