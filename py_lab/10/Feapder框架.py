import feapder


def writer(filename, name, intro):
    """记录一位院士(包括姓名和介绍)"""
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(name + '\n')
        f.writelines(intro)
        f.write('\n*******************************\n')


class SpiderTest(feapder.AirSpider):
    def start_requests(self):
        yield feapder.Request('http://www.cae.cn/cae/html/main/col48/column_48_1.html')

    def parse(self, request, response):
        li_lst = response.xpath('//li[@class="name_list"]')
        for li in li_lst:
            name = li.xpath("./a/text()").extract_first()
            url = li.xpath("./a/@href").extract_first()
            # 产生新任务
            yield feapder.Request(
                url, callback=self.parse_detail, name=name
            )  # callback 为回调函数

    def parse_detail(self, request, response):
        """处理新任务"""
        # 解析正文
        intro = response.xpath(
            'string(//div[@class="intro"])'
        ).extract_first().strip()  # string 表达式是取某个标签下的文本，包括子标签文本
        writer('工程院士信息feapder.txt', request.name, intro)


if __name__ == "__main__":
    SpiderTest(thread_count=32).start()
