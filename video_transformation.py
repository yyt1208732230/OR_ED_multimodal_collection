
# In this updated script, we first import the timedelta class from the datetime module in addition to the VideoFileClip class from the moviepy.video.io module.

# We then specify the specific time we want to get the timestamp for by setting the specific_time variable to a string in the format "hh:mm:ss.xx" (hours, minutes, seconds, and milliseconds). You should replace this string with the specific time you want to get the timestamp for.

# Next, we convert the specific time to a timedelta object using the timedelta() constructor. We extract the hours, minutes, seconds, and milliseconds from the specific_time string and pass them as arguments to the constructor. We then use the total_seconds() method of the timedelta object to convert it to a floating-point value representing the total number of seconds.

# We can then calculate the timestamp of the specific time in milliseconds by subtracting the end attribute of the VideoFileClip object (which represents the duration of the video in seconds) from the total number of seconds in the video up to the specific time, which we calculate by adding the specific time in seconds to the start attribute of the VideoFileClip object. We then multiply this result by 1000 to convert it to milliseconds.

# Finally, we print the timestamp in milliseconds using the print() function and close the video file using the close() method of the VideoFileClip object.
 

# from moviepy.video.io.VideoFileClip import VideoFileClip
# from datetime import timedelta

# # Replace "example.mp4" with the name of your MP4 file
# video = VideoFileClip("example.mp4")

# # Replace "00:01:30.00" with the specific time you want to get the timestamp for
# specific_time = "00:01:30.00"

# # Convert the specific time to a timedelta object
# specific_time_delta = timedelta(hours=int(specific_time[0:2]), 
#                                 minutes=int(specific_time[3:5]), 
#                                 seconds=int(specific_time[6:8]), 
#                                 milliseconds=int(specific_time[9:]))

# # Get the timestamp of the specific time in milliseconds
# timestamp = video.duration - video.end + specific_time_delta.total_seconds()

# # Print the timestamp in milliseconds
# print("Timestamp:", timestamp)

# # Close the video file
# video.close()


import datetime
import subprocess

def get_mp4_timestamp(filename, time):
    command = f"ffprobe -v error -select_streams v:0 -show_entries stream=pts_time -of csv=print_section=0 {filename}"
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    timestamps = result.stdout.split('\n')[:-1]
    for timestamp in timestamps:
        if float(timestamp) <= time:
            mp4_timestamp = datetime.datetime.utcfromtimestamp(float(timestamp)).strftime('%Y-%m-%d %H:%M:%S.%f')
    return mp4_timestamp

filename = "your_mp4_file.mp4"
time = 122.18333
mp4_timestamp = get_mp4_timestamp(filename, time)
print(mp4_timestamp)
