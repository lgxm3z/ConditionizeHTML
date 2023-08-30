import re

DEBUG = False  # Change this to test the behavior


def process_conditional_block(html_content):
    pattern = re.compile(
        r'(\s*)<!--\s*@if\s+(DEBUG|RELEASE)\s*-->\s*(.*?)\s*<!--\s*@endif\s*-->', re.IGNORECASE | re.DOTALL)

    def replacer(match):
        indentation = match.group(1)
        condition = match.group(2).upper()
        block = match.group(3).rstrip()
        if (condition == 'DEBUG' and DEBUG) or (condition == 'RELEASE' and not DEBUG):
            return f"{indentation}{block}"
        else:
            return ''

    return pattern.sub(replacer, html_content)


def minify_html(html_content):
    # Remove comments
    html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)

    # Remove whitespaces
    html_content = re.sub(r'\s+', ' ', html_content)

    # Remove whitespaces between tags
    html_content = re.sub(r'>\s+<', '><', html_content)

    # make code on one line
    html_content = re.sub(r'\n', '', html_content)

    # replace "<script> " to "<script>" and " </script>" to "</script>"
    html_content = re.sub(r'<script>\s+', '<script>', html_content)
    html_content = re.sub(r'\s+</script>', '</script>', html_content)

    return html_content


# Sample HTML content
html_content = '''
<!DOCTYPE html>
<html>
<head>
    <title>My Webpage</title>
</head>
<body>
    <!-- @If DEBUG -->
    <script>
        console.log('Debug mode');
    </script>
    <!-- @endif -->

    <!-- @If RELEASE -->
    <script>
        console.log('Release mode');
    </script>
    <!-- @endif -->
</body>
</html>
'''

# Conditionally process the specific block
new_html_content = process_conditional_block(html_content)

if (not DEBUG):
    new_html_content = minify_html(new_html_content)

print(new_html_content)
