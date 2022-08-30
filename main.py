from youtube_transcript_api import YouTubeTranscriptApi

from argparse import ArgumentParser

parser = ArgumentParser(description="Grab video subtitles and convert them into an `.srt` file")
parser.add_argument("-o", "--output", dest="filename", default="subs.srt", help="Output filename")
parser.add_argument("video_id", help="Target video's ID (URL part after `watch?v=`)")

args = parser.parse_args()

transcript = YouTubeTranscriptApi.get_transcript(args.video_id)

def convert_timestamp(timestamp):
    converted = [timestamp, 0, 0]

    for i in range(2):
        leftover = converted[i] % 60**(i+1)
        overflow = converted[i] - leftover

        converted[i] = round(leftover, 3)
        converted[i+1] = int(overflow // (60**(i+1)))

    return converted

with open(args.filename, "w") as file:
    for i, sub in enumerate(transcript):
        # Convert timestamps
        # Start
        start = convert_timestamp(sub["start"])

        start_str = ":".join(reversed([str(point) for point in start])).replace(".", ",")

        # End
        if i < len(transcript)-1:
            end_time = transcript[i+1]["start"]
        else:
            end_time = sub["duration"]

        end = convert_timestamp(end_time)

        if not i < len(transcript)-1:
            end = [start[j] + point for j, point in enumerate(end)] # Since that was only duration, add it to starting point

        end_str = ":".join(reversed([str(point) for point in end])).replace(".", ",")

        file.write(f"{str(i+1)}\n") # Index
        file.write(f"{start_str} --> {end_str}\n") # Timestamp
        file.write(f"{sub['text']}\n") # Text

        file.write("\n")
