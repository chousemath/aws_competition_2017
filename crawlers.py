import urllib2


OUTPUT_FILE_NAME = 'output.txt'

URL = 'http://sports.news.naver.com/lol/news/index.nhn'


def get_text(URL):
    temp = urllib2.urlopen(URL)
    return temp.read()


def main():
    open_output_file = open(OUTPUT_FILE_NAME, 'w')
    result_text = get_text(URL)
    open_output_file.write(result_text)
    open_output_file.close()


if __name__ == '__main__':
    main()
