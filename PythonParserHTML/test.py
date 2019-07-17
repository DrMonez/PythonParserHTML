import urllib.request
import re
import os


class HtmlParser:

    def __init__(self, html):
        self.html_address = html

    def __get_html(self):
        with urllib.request.urlopen(self.html_address) as html:
            self.content = str(html.read().decode('utf-8'))

    def __references_substitution(self, content):
        search_ref = True
        while search_ref:

            ref = re.search(r'<a.*?href=".*?"', content)

            try:
                ref = re.sub(r'<a.*?href="', r'', ref[0], count=0)
                ref = re.sub(r'"', r'', ref, count=0)
                content = re.sub(r'<a.*?href=".*?>', r'', content, count=1)
                content = re.sub(r'</a>', "[" + ref + "]", content, count=1)

            except:
                search_ref = False

        return content

    def __get_content(self, tag, count, start_index):
        search = True
        content = ''
        iteration = 0

        while search:
            if int(count) != 0:
                if iteration < int(count):
                    try:
                        search_result = re.search(r'<' + tag + r'.*?</' + tag + r'>', self.content)

                        if not iteration < int(start_index):
                            content = self.__get_content_subpass(tag, content, search_result[0])

                        self.content = re.sub(r'<' + tag + r'.*?</' + tag + r'>', r'', self.content, count=1)
                    except:
                        search = False
                else:
                    search = False
            else:
                try:
                    search_result = re.search(r'<' + tag + r'.*?</' + tag + r'>', self.content)

                    if not iteration < int(start_index):
                        content = self.__get_content_subpass(tag, content, search_result[0])

                    self.content = re.sub(r'<' + tag + r'.*?</' + tag + r'>', r'', self.content, count=1)
                except:
                    search = False
            iteration += 1

        return content

    def __get_content_subpass(self, tag, content, search_result):


        content += re.sub(r'<' + tag + r'.*?>', r'', search_result, count=0)
        content = re.sub(r'</' + tag + r'>', '\n\n', content, count=0)
        content = re.sub(r'&\S*;', r' ', content, count=0)

        content = self.__references_substitution(content)

        content = re.sub(r'<.*>', r'', content, count=0)

        return content

    def __read_settings(self):
        try:
            file = open("parser_settings.txt", 'r')
            tags = file.read()
            file.close()
            self.tags = tags.split('\n')
        except:
            pass

    def save_in_file(self):
        filename = self.html_address.strip("https://")
        filename = filename.strip("https://")
        new_path = filename.rstrip('/')
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        filename += r"\content.txt"
        filename = re.sub(r'/', r'\\', filename, count=0)
        file = open(filename, 'w', encoding='utf-8')
        file.write(self.content)
        file.close()

    def __formatting_string(self, content):
        is_formatted = False
        res = ''
        while not is_formatted:
            try:

                a = re.search(r'.{,80}\s', content)
                res += a[0] + '\n'
                content = re.sub(r'.{,80}\s', '', content, count=1)
            except:
                is_formatted = True

        res = re.sub(r'\s{3,}', '\n\n', res, count=0)
        return res

    def parse(self):
        self.__read_settings()
        self.__get_html()
        content = ''
        for tag in self.tags:
            info = re.split(r'\s', tag)
            try:
                content += self.__get_content(info[0], info[1], info[2])
            except:
                pass
        content = self.__formatting_string(content)
        self.content = content
        return content


def main():
    parser1 = HtmlParser('https://novosibirsk.hh.ru/vacancy/30036210')
    print(parser1.parse())
    parser1.save_in_file()


if __name__ == '__main__':
    main()
