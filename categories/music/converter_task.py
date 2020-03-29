from pprint import pprint

from lxml import etree

from categories.basic_task import Task


class ConverterTask(Task):
    def run(self):
        url = 'https://vk.com/audios' + str(self.user_id)
        site = self.site_request(url)
        xpath = './/div[@class="audio_row_content _audio_row_content"]'
        document = etree.HTML(site.text)
        result = document.xpath(xpath)
        tracklist = []
        for item in result:
            artist = item.xpath('.//div[@class="audio_row__performers"]')[0].getchildren()[0].text
            name = item.xpath('.//span[@class="audio_row__title_inner _audio_row__title_inner"]')[0].text
            full = (artist + '   ' + name).lower()
            tracklist.append(full)
        pprint(tracklist)
        for track in tracklist:
            response = self.site_request('https://www.youtube.com/results', search_query=track)
            xpath = '//a[@id="video-title"]'
            document = etree.HTML(response.text)
            result = document.xpath(xpath)
            for item in result:
                title = item.attrib['title']
                href = item.attrib['href']
                video = title.lower() + ' //  ' + href
                print(video)
