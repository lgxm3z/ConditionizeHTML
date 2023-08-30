# ConditionizeHTML
Dynamically process HTML files based on conditional statements embedded within comments

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Webpage</title>
</head>
<body>
    <!-- @if DEBUG -->
    <script>
        console.log('Debug mode');
    </script>
    <!-- @endif -->

    <!-- @if RELEASE -->
    <script>
        console.log('Release mode');
    </script>
    <!-- @endif -->
</body>
</html>
```
