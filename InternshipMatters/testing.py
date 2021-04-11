import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re
s = "                SSSSSS                (DDDD)"
r = re.sub(r"\s+"," ", re.sub(r"^\s+|\s+$", "", s))  
print(r)