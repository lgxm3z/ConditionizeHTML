import argparse
import os
import re


def process_conditional_block(html_content, **kwargs):
    pattern = re.compile(
        r'(\s*)<!--\s*@if\s+(.*?)\s*-->\s*(.*?)\s*<!--\s*@endif\s*-->', re.IGNORECASE | re.DOTALL)

    def replacer(match):
        indentation = match.group(1)
        condition = match.group(2).upper()
        block = match.group(3).rstrip()
        if kwargs.get(condition, False):
            return f"{indentation}{block}"
        else:
            return ''

    return pattern.sub(replacer, html_content)


def minify_html(html_content):
    html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
    tag_pattern = re.compile(r'<(.*?)>(.*?)<\/.*?>', re.DOTALL)
    html_content = tag_pattern.sub(
        lambda m: "<" + m.group(1) + ">" + m.group(2).strip() + "</" + m.group(1) + ">", html_content)
    html_content = re.sub(r'\s+', ' ', html_content)
    html_content = re.sub(r'>\s+<', '><', html_content)
    return html_content.strip()


# Parse command line arguments
parser = argparse.ArgumentParser(
    description="Transform HTML based on conditions.")
parser.add_argument("--IN", type=str, required=True,
                    help="Input HTML file.", metavar="input_file")
parser.add_argument(
    "--OUT", type=str, help="Output HTML file. If not specified, will overwrite input.", metavar="output_file")
parser.add_argument("--MINIFY", action='store_true',
                    help="Flag to minify the HTML.")
parser.add_argument("--EXTRA", nargs=argparse.REMAINDER,
                    help="Extra arguments for conditional flags.")

args = parser.parse_args()

extra_args_dict = {}
if args.EXTRA:
    for extra_arg in args.EXTRA:
        key, value = extra_arg.split('=')
        extra_args_dict[key.upper()] = value.lower() == "true"

if args.IN and not os.path.exists(args.IN):
    raise FileNotFoundError(f"The input file {args.IN} does not exist.")

with open(args.IN, 'r') as file:
    html_content = file.read()

# Conditionally process the specific block
new_html_content = process_conditional_block(html_content, **extra_args_dict)

# Minify if the flag is set
if args.MINIFY:
    new_html_content = minify_html(new_html_content)

with open(args.OUT if args.OUT else args.IN, 'w') as file:
    file.write(new_html_content)
