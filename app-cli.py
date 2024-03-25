#!/usr/bin/env python3

from threading import Thread
import argparse, sys
from pathlib import Path
import os
import time
from markdown_to_html import convert_markdown_to_html

DEBUG_MODE = False

def convert_chunk(chunk_id, chunk_start, chunk_end, markdown_lines, output_dir, original_file_name):
    """Converts a chunk of Markdown to HTML and writes it to a separate file.
    Args:
        chunk_id: An integer for file generation
        chunk_start: integer, start line to process in @{markdown_lines}
        chunk_end: integer, end line to process in @{markdown_lines}
        markdown_lines: array of markdown text lines
        output_dir: output directory for generated html files
        original_file_name: original file name supplied by the user
    Returns:
        None. Write converted html as string to a new file.
    """
    html = ""
    numOfLines = len(markdown_lines)
    # Process lines within the assigned chunk range
    for i in range(chunk_start, min(chunk_end, numOfLines)):
        # markdown_lines is passed in as reference, no I/O overhead
        line = markdown_lines[i]
        # Core markdown-to-HTML conversion logic.
        # Process 1 line only because all the markdown lines have been split and passed into this function.
        html_line = convert_markdown_to_html(line)
        # Hence adding a new line for each html line
        html += html_line + '\n'
    
    # Pad file name for sorting
    file_path = f"{output_dir}/{original_file_name}-output-{chunk_id:02d}.html"
    with open(file_path, 'w') as f:
        f.write(html)

def main_slow(markdown_file_path):
    print("running slow markdown-to-html conversion. Converted html will be return on the console.")
    
    with open(markdown_file_path, 'r') as f:
        markdown_content = f.read()
    # Core markdown-to-HTML conversion logic.
    html = convert_markdown_to_html(markdown_content)
    print("converted html:\n" + html)

    return html

def main_fast(markdown_file_path):
    print("running fast markdown-to-html conversion. Check `html_result/` folder for the output")
    # generate UUID with timestamp - a naive version
    current_timestamp = time.time()
    # Parse the markdown input file to get the original name
    file_name = Path(markdown_file_path).stem
    if DEBUG_MODE:
        print("Timestamp:", current_timestamp)
        print("file_name:", file_name)

    output_dir = f"html_result/{current_timestamp}"
    # Check whether the specified path exists or not
    output_dir_exists = os.path.exists(output_dir)
    if not output_dir_exists:
        # Create a new directory because it does not exist
        os.makedirs(output_dir)
        if DEBUG_MODE:
            print(f"New output directory is created:{output_dir}")
    else:
        if DEBUG_MODE:
            print(f"{output_dir} exists. There is no need to create it.")

    # Number of worker threads, can be tuned based on your system
    num_threads = 4

    # Read the entire Markdown content into a string
    with open(markdown_file_path, 'r') as f:
        markdown_content = f.read()
    
    # Split markdown input to lines
    markdown_lines = markdown_content.splitlines()
    # Calculate the number of lines per chunk (rounded down for even distribution)
    lines_per_chunk = len(markdown_lines) // num_threads

    # Create worker threads and assign tasks
    threads = []
    
    # no queue or lock need her updating chunk_id, because it is never modified. 
    for chunk_id in range(num_threads):
        chunk_start = chunk_id * lines_per_chunk
        chunk_end = (chunk_id + 1) * lines_per_chunk
        thread = Thread(target=convert_chunk, args=(chunk_id, chunk_start, chunk_end, markdown_lines, output_dir, file_name))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    # boostrap code for CLI
    parser = argparse.ArgumentParser()
    parser.add_argument("--markdown_file_path", help="Path to the markdown file input")
    parser.add_argument("--optimized", action=argparse.BooleanOptionalAction, help="whether to run on optimized mode")
    parser.add_argument("--debug_mode", action=argparse.BooleanOptionalAction, help="Debug mode")
    args=parser.parse_args()
    print(f"Args: {args}\nCommand Line: {sys.argv}")
    print(f"Dict format: {vars(args)}")
    
    # Set debug_mode if needed
    if args.debug_mode:
        DEBUG_MODE = True

    # validation
    if not args.markdown_file_path:
        print("markdown_file_path is not present. Use `--help` flag for usage instruction.")
    else:
        if args.optimized:
            main_fast(args.markdown_file_path)
        else:
            main_slow(args.markdown_file_path)