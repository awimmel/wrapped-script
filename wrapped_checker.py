import os
import json

read_dir  = 'resources/listening_history'

song_count_output  = 'resources/output/song_count.csv'
song_duration_output  = 'resources/output/song_duration.csv'
artist_count_output  = 'resources/output/artist_count.csv'
artist_duration_output  = 'resources/output/artist_duration.csv'

song_count = {}
song_duration = {}
artist_count = {}
artist_duration = {}

# Read from file, storing in proper dictionaries
def read_file(file_path):
    with open(file_path, 'rb') as file:
        data = json.load(file)
        for stream in data:
            duration = stream['msPlayed']
            if stream['msPlayed'] > 12000 and '2024' in stream['endTime']:
                song = stream['trackName']
                if song in song_count and song in song_duration:
                    song_count[song] += 1
                    song_duration[song] += duration
                else:
                    song_count[song] = 1
                    song_duration[song] = duration
                artist = stream['artistName']
                if artist in artist_count and artist in artist_duration:
                    artist_count[artist] += 1
                    artist_duration[artist] += duration
                else:
                    artist_count[artist] = 1
                    artist_duration[artist] = duration

def write_csv(file_name, dictionary, first_header, second_header, duration):
    with open(file_name, 'w+', encoding="utf-8") as csv:
        csv.write('%s,%s\n' % (first_header, second_header))
        for key, value in dictionary:
            scaled_value = value
            if duration:
                scaled_value = (value / 60000)
            csv.write('%s,%s\n' % (key, scaled_value))

def generate_table(sorted_dict, first_header, second_header, duration):
    max_first = len(first_header)
    max_second = len(second_header)

    dict_iter = iter(sorted_dict)
    counter = 0
    while counter < 5:
        key, value = next(dict_iter)
        
        if len(key) > max_first:
            max_first = len(key)
        
        if len(str(value)) > max_second:
            max_second = len(str(value))

        counter += 1
    
    print('\t\t' + generate_line('_', max_first + max_second + 5, True))
    
    formatted_first_header = generate_line(first_header, max_first, False)
    formatted_second_header = generate_line(second_header, max_second, False)
    print('\t\t|' + formatted_first_header + '|' + formatted_second_header + '|')
    first_border = generate_line('-', max_first, True)
    second_border = generate_line('-', max_second, True)
    print('\t\t|' + first_border + '|' + second_border + '|')
    
    dict_iter = iter(sorted_dict)
    counter = 0
    while counter < 5:
        key, value = next(dict_iter)
        scaled_value = value / 60000 if duration else value
        formatted_key = generate_line(key, max_first, False)
        formatted_value = generate_line(str(scaled_value), max_second, False)
        print('\t\t|' + formatted_key + '|' + formatted_value + '|')
        counter += 1

    print('\t\t' + generate_line('_', max_first + max_second + 5, True))

def generate_line(val, req_len, duplicate):
    line = ''
    counter = 0
    if (duplicate):
        while counter < (req_len + 2):
            line += val
            counter += 1
    else:
        half = (req_len - len(val)) // 2 
        end_spaces = half + 1
        beg_spaces = half + ((req_len - len(val)) % 2) + 1

        while counter < beg_spaces:
            line += ' '
            counter += 1

        counter = 0
        line += val

        while counter < end_spaces:
            line += ' '
            counter += 1

    return line



# Iterate through all files in directory
print('Reading resources/listening_history JSON files')
for name in os.listdir(read_dir):
    file = os.path.join(read_dir, name)

    if os.path.isfile(file):
        read_file(file)
print('Finished reading resources/listening_history JSON files. Beginning to write output files')

sorted_song_count = sorted(song_count.items(), key=lambda x: x[1], reverse=True)
write_csv(song_count_output, sorted_song_count, 'Song', 'Count', False)

sorted_song_duration = sorted(song_duration.items(), key=lambda x: x[1], reverse=True)
write_csv(song_duration_output, sorted_song_duration, 'Song', 'Duration (mins.)', True)

sorted_artist_count = sorted(artist_count.items(), key=lambda x: x[1], reverse=True)
write_csv(artist_count_output, sorted_artist_count, 'Artist', 'Count', False)

sorted_artist_duration = sorted(artist_duration.items(), key=lambda x: x[1], reverse=True)
write_csv(artist_duration_output, sorted_artist_duration, 'Song', 'Duration (mins.)', True)
print('Finished writing output files')

print()
print('Summary:')
print()

print('\tMost played songs (by number of streams):')
print()
generate_table(sorted_song_count, 'Song', 'Streams', False)
print()

print('\tMost played songs (by duration):')
print()
generate_table(sorted_song_duration, 'Song', 'Duration (mins.)', True)
print()

print('\tMost played artists (by count):')
print()
generate_table(sorted_artist_count, 'Song', 'Streams', False)
print()

print('\tMost played artists (by duration):')
print()
generate_table(sorted_artist_duration, 'Song', 'Duration (mins.)', True)
print()




