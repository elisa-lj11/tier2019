# script to quickly create a URL list from a blog post

new_file = open("url_list.txt", "w+", encoding="utf-8")

url_base = "https://www.avforums.com/threads/oculus-rift-vr-headset.1672862/page-"
pages = 122

for n in range(2, pages + 1):
	url_page = url_base + str(n)
	new_file.write("{}\n".format(url_page))
