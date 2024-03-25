import re

# Declarative config for heading tags
# This config provides a centralized place, not only to manage existing html tags,
# but also easy to include more tags in the future
html_tag_map = {
  'heading_1':{'md_tag':'# ','html_tag':'h1','heading_level':1},
  'heading_2':{'md_tag':'## ','html_tag':'h2','heading_level':2},
  'heading_3':{'md_tag':'### ','html_tag':'h3','heading_level':3},
  'heading_4':{'md_tag':'#### ','html_tag':'h4','heading_level':4},
  'heading_5':{'md_tag':'##### ','html_tag':'h5','heading_level':5},
  'heading_6':{'md_tag':'###### ','html_tag':'h6','heading_level':6}
}

# the used by web service and CLI
def convert_markdown_to_html(markdown_text):
  """Converts a markdown string to HTML.
  Args:
      markdown_text: The markdown string to convert.
  Returns:
      The converted HTML string.
  """
  print("starting to convert markdown")
  markdown_lines = markdown_text.splitlines()
  html_lines = []

  for line in markdown_lines:
    # Process tag by order of importance
    # Priotity 1: hyper links
    # Process links within the line first, regardless of heading or paragraph
    processed_line = re.sub(r"\[([^\]]+)]\(([^)]+)\)", lambda match: f'<a href="{match.group(2)}">{match.group(1)}</a>', line)

    # Priotity 2: Check for headings
    if processed_line.startswith('#'):
      heading_level = 0
      if processed_line.startswith(html_tag_map['heading_1']['md_tag']):
        heading_level = html_tag_map['heading_1']['heading_level']
      elif processed_line.startswith(html_tag_map['heading_2']['md_tag']):
        heading_level = html_tag_map['heading_2']['heading_level']
      elif processed_line.startswith(html_tag_map['heading_3']['md_tag']):
        heading_level = html_tag_map['heading_3']['heading_level']
      elif processed_line.startswith(html_tag_map['heading_4']['md_tag']):
        heading_level = html_tag_map['heading_4']['heading_level']
      elif processed_line.startswith(html_tag_map['heading_5']['md_tag']):
        heading_level = html_tag_map['heading_5']['heading_level']
      elif processed_line.startswith(html_tag_map['heading_6']['md_tag']):
        heading_level = html_tag_map['heading_6']['heading_level']
      
      if heading_level > 0:
        html_tag = html_tag_map[f'heading_{heading_level}']['html_tag']
        # heading_level + 1 to include the space after the heading tag
        html_lines.append(f"<{html_tag}>{processed_line[heading_level+1:]}</{html_tag}>")
      else:
        html_lines.append(f"<p>{processed_line}</p>")
    # Last priority: otherwise, treat it as unformatted text: <p>...</p>
    else:
      processed_line = processed_line.strip()
      if processed_line:
        html_lines.append(f"<p>{processed_line}</p>")

  # concate html lines with newlines to main the intended line breaks
  return "\n".join(html_lines)
