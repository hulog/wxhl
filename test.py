import requests
import re
douban_url = 'https://movie.douban.com/'
douban_html = requests.get(douban_url).text
c = re.compile(r' <a onclick="moreurl.*?href="(.*?)"[\s\S]*?src="(.*?)" alt="(.*?)" [\s\S]*?class="subject-rate">(.*?)</span>', re.S)
DOUBAN = re.findall(c,douban_html)

print DOUBAN[:5]
