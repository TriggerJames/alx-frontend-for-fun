#!/usr/bin/python3
"""
markdown2html.py: A simple script to convert Markdown files to HTML.
"""

import sys
import os
import re
import hashlib


def convert_headings(line):
    """
    Convert Markdown headings to HTML headings.
    """
    for i in range(6, 0, -1):
        if line.startswith('#' * i + ' '):
            return f"<h{i}>{line[i+1:].strip()}</h{i}>"
    return line


def convert_unordered_list(lines):
    """
    Convert Markdown unordered lists to HTML unordered lists.
    """
    html_lines = []
    inside_ulist = False
    for line in lines:
        if line.startswith('- '):
            if not inside_ulist:
                html_lines.append("<ul>")
                inside_ulist = True
            html_lines.append(f"<li>{line[2:].strip()}</li>")
        else:
            if inside_ulist:
                html_lines.append("</ul>")
                inside_ulist = False
            html_lines.append(line)
    if inside_ulist:
        html_lines.append("</ul>")
    return html_lines


def convert_ordered_list(lines):
    """
    Convert Markdown ordered lists to HTML ordered lists.
    """
    html_lines = []
    inside_olist = False
    for line in lines:
        if line.startswith('* '):
            if not inside_olist:
                html_lines.append("<ol>")
                inside_olist = True
            html_lines.append(f"<li>{line[2:].strip()}</li>")
        else:
            if inside_olist:
                html_lines.append("</ol>")
                inside_olist = False
            html_lines.append(line)
    if inside_olist:
        html_lines.append("</ol>")
    return html_lines


def convert_paragraphs(lines):
    """
    Convert plain text to HTML paragraphs and handle line breaks.
    """
    html_lines = []
    inside_paragraph = False
    for line in lines:
        if line.strip():
            if not inside_paragraph:
                html_lines.append("<p>")
                inside_paragraph = True
            html_lines.append(line.strip())
        else:
            if inside_paragraph:
                html_lines.append("</p>")
                inside_paragraph = False
    if inside_paragraph:
        html_lines.append("</p>")
    return html_lines


def convert_bold_and_emphasis(line):
    """
    Convert Markdown bold and emphasis to HTML.
    """
    line = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)  # Bold
    line = re.sub(r'__(.+?)__', r'<em>\1</em>', line)  # Emphasis
    return line


def convert_custom(line):
    """
    Convert custom Markdown syntax for MD5 and remove 'c' characters.
    """
    line = re.sub
    (r'\[\[(.+?)\]\]',
     lambda m: hashlib.md5(m.group(1).encode()).hexdigest(), line)

    line = re.sub
    (r'\(\((.+?)\)\)',
     lambda m: m.group(1).replace('c', '').replace('C', ''), line)
    return line

if __name__ == "__main__":
    # Check if the number of arguments is less than 2
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html",
              file=sys.stderr)
        sys.exit(1)

    # Get file names from arguments
    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    # Check if the Markdown file exists
    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    # Read the input Markdown file
    with open(markdown_file, 'r') as md:
        lines = md.readlines()

    # Process the Markdown file
    lines = convert_unordered_list(lines)
    lines = convert_ordered_list(lines)
    lines = convert_paragraphs(lines)

    # Write the output HTML file
    with open(html_file, 'w') as html:
        for line in lines:
            line = convert_headings(line)
            line = convert_bold_and_emphasis(line)
            line = convert_custom(line)
            html.write(line + '\n')

    # Exit successfully
    sys.exit(0)
