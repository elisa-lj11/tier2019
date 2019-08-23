# Created by Elisa Lupin-Jimenez
# script to quickly create a URL list from an AVForum blog post to input to HTTrack application

new_file = open("url_list.txt", "w+", encoding="utf-8")

# CONSTANT: change this for the URL base of the forum post that you would like to get all pages for
url_base = "https://www.avforums.com/threads/oculus-rift-vr-headset.1672862/page-"
pages = 122

for n in range(2, pages + 1):
	url_page = url_base + str(n)
	new_file.write("{}\n".format(url_page))
