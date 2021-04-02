import re

match = re.match(r"-?\d*.?\d+", "-133.559")

print(match.group())
print()

match = re.match(r"(?P<name>.+)@(.+\.com)", "user@domain.com")

print(match.group('name'))
print()

match = re.match(r"^(?P<scheme>.+)://(?P<host>.+):(?P<port>\d+)/(?P<path>.+)\?(?P<query>.+)", 
                 "http://www:80/something/something.html/2.html?query")

print(match.group('scheme'))
print(match.group('host'))
print(match.group('port'))
print(match.group('path'))
print(match.group('query'))