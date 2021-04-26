import re
email = "dashka-klimovich@mail.ru"
pattern=r"^([a-z0-9_-]+\.)*[a-z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,6}$"
number_re=re.compile(pattern)
if number_re.findall(email):
    print("Email of correct:")
    print(email)
else:
    print("Error:")
    print(email)

print()
data = "2.2"
pattern=r"^[0-9]*[.,]?[0-9]+$"
number_re=re.compile(pattern)
if number_re.findall(data):
    print("data of correct:")
    print(data)
else:
    print("Error:")
    print(data)



print()
site = "http://www.my-site.com"
pattern=r"^((https?|ftp)\:\/\/)?([a-z0-9]{1})((\.[a-z0-9-])|([a-z0-9-]))*\.([a-z]{2,6})(\/?)$"
number_re=re.compile(pattern)
if number_re.findall(site):
    print("Site of correct:")
    print(site)
else:
    print("Error:")
    print(site)
