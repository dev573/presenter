import re

PRESENTATION_CONFIG = """
[comment]: # (CODE_THEME = base16/zenburn)
[comment]: # (controls: true)
[comment]: # (keyboard: true)

"""


def get_presentation_config() -> str:
    return PRESENTATION_CONFIG


def get_safe_foldername(topic: str) -> str:
    return topic.replace(" ", "_").lower()


def sanitize_markdown(text: str) -> str:
    pattern = r"(?s)(```mermaid.*?)(^.*?Note over.*?$)(.*?```)"
    result = re.sub(
        pattern,
        lambda m: m.group(1)
        + re.sub(r"^.*?Note over.*?\n?", "", m.group(2), flags=re.M)
        + m.group(3),
        text,
        flags=re.M,
    )
    pattern2 = r"^(#{1,2})\s"
    result = re.sub(pattern2, r"### ", result, flags=re.M)
    pattern3 = r"!\[.+\]\(\./(.*?\.png)\)"
    result = re.sub(pattern3, r"![diagram](./media/\1)", result, flags=re.M)
    result = result.replace("flowchart TD", "flowchart LR")
    return result + "\n\n"


def generate_ffmpeg_command(
    input_files, output_file, transition="slideleft", duration=1
):
    """
    Generate an FFmpeg command to combine video files with sliding transitions.

    Args:
        input_files (list): List of input video file paths.
        output_file (str): The output video file path.
        transition (str): Transition type (default: "slideleft").
        duration (int): Duration of the transition in seconds (default: 1).
    """
    # Initialize the filter_complex string
    filter_complex = ""
    inputs = [f"-i {file}" for file in input_files]  # Prepare input list

    # Generate video streams and transition filters
    xfade_filters = []
    for i in range(len(input_files)):
        # Each video is assigned a labeled stream
        filter_complex += f"[{i}:v:0]trim=0,setpts=PTS-STARTPTS[v{i}];"
    for i in range(len(input_files) - 1):
        # Create xfade transitions between consecutive video pairs
        offset = i * 5  # Adjust offset (time before transition starts)
        xfade_filters.append(
            f"[v{i}][{i}:a:0][v{i + 1}][{i + 1}:a:0]xfade=transition={transition}:duration={duration}:offset={offset}[outv{i + 1}][outa{i + 1}]"
        )

    # Append all transition filters to filter_complex
    filter_complex += ";".join(xfade_filters)

    # Map the last output stream
    final_map = f"-map [outv{len(input_files) - 1}] -map [outa{len(input_files) - 1}]"

    # Combine everything into a final ffmpeg command
    command = f"ffmpeg {' '.join(inputs)} -filter_complex \"{filter_complex}\" {final_map} {output_file}"
    return command
