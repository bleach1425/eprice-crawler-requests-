import requests
import jieba
from bs4 import BeautifulSoup
import csv
import io

# 總頁數
header_data = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    "Accept-Language": "zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3"
}
# 所有評論的CODE
def get_code(n):
    data_list = []
    r3 = requests.get(f"https://www.eprice.com.tw/mobile/talk/4568/0/{n}/",
                      headers=header_data,
                      params={
                      }
                      )
    r3.encoding = "utf-8"
    bs3 = BeautifulSoup(r3.text, "html.parser")
    title = bs3.find_all("a", {"class": "title"})
    title_first = ""
    for q in title:
        if len(q.get("href").split("/")[4]) == 7:
            code = q.get("href").split("/")[4]
            data_list.append(code)
    return data_list

# 拿BS的資料去抓標題
def get_title(bs):
    title1 = bs.find_all("h1", {"class": "title"})
    title_list = []
    for z in title1:
        title_list.append(z.text)
    return title_list

# 拿BS的資料去抓內文
def get_content(bs):
    content_list = []
    title2 = bs.find_all("div", {"class": "user-comment-block"})
    for n in title2:
        content_list.append(n.text)
    return content_list

# 拿到CODE之後找所有BeatifulSoup處理完的資料
def get_page_parser(code):
    r = requests.get(f"https://www.eprice.com.tw/mobile/talk/4568/{code}/1/",
                     headers=header_data,
                     params={
                     }
                     )
    r.encoding = "utf-8"
    bs = BeautifulSoup(r.text, "html.parser")
    return bs


# 找出最大頁數
def get_page(bs):
    all_page_list = []
    data_page = bs.find_all("a", {"data-name": "page"})
    for b in data_page:
        all_page = b.get("data-value")
        all_page_list.append(int(all_page))
    return all_page_list
    #     test = int(max(all_page_list))
    # if len(all_page_list) == 0:
    #     test = 1

# 用參數code,內文頁數，爬使用者評論
def get_user_comment(code,max_page):
    user_comment = []
    for page in range(1, max_page + 1):
        r1 = requests.get(f"https://www.eprice.com.tw/mobile/talk/4568/{code}/{page}/",
                          headers=header_data,
                          params={
                          }
                          )
        r1.encoding = "utf-8"
        bs1 = BeautifulSoup(r1.text, "html.parser")
        title = bs1.find_all("div", {"class": "comment"})
        for f in title:
            user_comment.append(f.text)
    return user_comment


def get_page_detail(page):
    code_list = get_code(page)

    data = []
    for code in code_list:
        result = dict()
        bs = get_page_parser(code)
        page_list = get_page(bs)
        if not page_list:
            page_list=[1]
        max_page = max(page_list)
        title = get_title(bs)
        result['title'] = title
        content = get_content(bs)
        result['content'] = content
        comments = get_user_comment(code,max_page)
        result['comments'] = comments
        print(comments, end="\n")
        data.append(result)
    return data

# 開始爬蟲
def main():
    data = []
    # title = get_title(bs)
    # content = get_content(bs)
    # with open("Apple_title_content.csv","r",encodeing="utf-8",newline="") as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["標題", "內容"])
    #     writer.writerow()

    # with open("Apple_User_Comment.csv", "r", encodeing="utf-8", newline="") as f1:
    for i in range(1, 66):
        ret = get_page_detail(i)
        # data.append(ret)
        print("[", i, "]", "=====", ret)
        with open("MIUserComment.csv", "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["標題", "內容", "使用者評論"])
            for item in ret:
                writer.writerow([item['title'], item['content'], item['comments']])


    #    for i in range(1, 66):
    #     ret = get_page_detail(i)
    #     data.append(ret)
    #     print("[", i, "]", "=====", ret)
if __name__ == "__main__":
    main()
