# script to quickly create a URL list from a blog post

new_file = open("url_list.txt", "w+", encoding="utf-8")

url_base = "https://www.avforums.com/threads/hp-reverb-copper-vr-headset.2215289/page-"
pages = 4

for n in range(2, pages + 1):
	url_page = url_base + str(n)
	new_file.write("{}\n".format(url_page))
