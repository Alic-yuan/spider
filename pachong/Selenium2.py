from selenium import webdriver

class Item():
    ip = None  # ip地址
    port = None  # 端口
    anonymous = None  # 是否匿名
    type = None  # http or https
    local = None  # 物理地址
    speed = None  # 速度

class GetProxy():
    def __init__(self):
        self.starturl = 'http://www.kuaidaili.com/free/inha/'
        self.urls = self.get_urls()
        self.proxies = self.get_proxies(self.urls)
        self.filename = 'proxies.txt'
        self.save_file(self.filename,self.proxies)

    def get_urls(self):
        urls = []
        for i in range(1,3):
            url = self.starturl + str(i)
            urls.append(url)
        return urls

    def get_proxies(self,urls):
        brower = webdriver.PhantomJS()
        proxy_list=[]
        for url in urls:
            brower.get(url)
            brower.implicitly_wait(3)
            results = brower.find_elements_by_xpath('//*[@id="list"]/table/tbody/tr')
            for result in results:
                item = Item()
                item.ip = result.find_element_by_xpath('./td[1]').text
                item.port = result.find_element_by_xpath('./td[2]').text
                item.anonymous = result.find_element_by_xpath('./td[3]').text
                item.type = result.find_element_by_xpath('./td[4]').text
                item.local = result.find_element_by_xpath('./td[5]').text
                item.speed = result.find_element_by_xpath('./td[6]').text
                print(item.ip)
                proxy_list.append(item)
        brower.quit()
        return proxy_list


    def save_file(self, filename, proxies):
        with open(filename,'w') as f:
            for item in proxies:
                f.write(item.ip +'\t')
                f.write(item.port + '\t')
                f.write(item.anonymous + '\t')
                f.write(item.type + '\t')
                f.write(item.local + '\t')
                f.write(item.speed + '\n\n')

if __name__ == '__main__':
    proxy = GetProxy()