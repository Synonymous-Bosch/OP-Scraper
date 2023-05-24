#! python3
import requests, os, bs4, re, lxml

with open("new_chapter.txt", "r") as file:
    newChapterNum = int(file.read())

newChapter = "https://read-onepiece.one/comic/one-piece-chapter-" + str(newChapterNum)

url_main = "https://read-onepiece.one/"


print(url_main)

os.makedirs('OnePiece', exist_ok=True)

print("Downloading ")
res_main = requests.get(url_main)
res_main.raise_for_status()
soup_main = bs4.BeautifulSoup(res_main.text, "html.parser")
result = soup_main.body.find_all("a", href=re.compile(newChapter))

if newChapter in str(result):
    print("New chapter found")
    # 
    res = requests.get(newChapter)
    res.raise_for_status()
    soup_new = bs4.BeautifulSoup(res.content, 'lxml')
    images = soup_new.select('img')

    for image in images:
            
        url = image['data-src']
        comic = requests.get(url)
        comic.raise_for_status()
        comic_file = open(os.path.join('OnePiece', os.path.basename(url)), 'wb')
        for chunk in comic.iter_content(100000):
             comic_file.write(chunk)
        comic_file.close()

    newChapterNum += 1
    file = open("new_chapter.txt", "w")
    stored_variable = repr(newChapterNum)
    file.write(stored_variable)
    file.close()


else:
    print("No new chapter today")