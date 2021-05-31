import webbrowser

message = """<html>
<head></head>
<body><p>Hello World!</p></body>
</html>"""

filepath = "solution.html"
# with open(filepath, 'w') as f:
#     f.write(message)
#     f.close()
webbrowser.open(filepath)