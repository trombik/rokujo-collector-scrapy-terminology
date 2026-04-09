from datetime import datetime, timezone

import scrapy
from ..items import GlossaryJbitsItem


class JbitsSpider(scrapy.Spider):
    name = "jbits"
    allowed_domains = ["jbits.co.jp"]
    start_urls = ["https://www.jbits.co.jp/glossary.html"]

    def parse(self, response):
        hrefs = response.xpath("//div[contains(@class, 'about')]/a[1]/@href").getall()
        for href in hrefs:
            yield response.follow(href, callback=self.parse_terminology_page)

    def parse_terminology_page(self, res):
        page_title = res.xpath("//title/text()").get(default="").strip()
        obtained_at = datetime.now(timezone.utc).isoformat()

        for td in res.xpath("//tr/td"):
            term = td.xpath("./span[@class='term']/text()").get()

            full_text = "".join(td.xpath("./span[@class='desc']//text()").getall()).strip()
            if term and full_text:
                lines = [line.strip() for line in full_text.splitlines() if line.strip()]

                item = GlossaryJbitsItem()
                item["term"] = term.strip()
                item["translation"] = lines[0] if lines else ""
                item["description"] = " ".join(lines[1:]) if len(lines) > 1 else ""
                item["title"] = page_title
                item["obtained_at"] = obtained_at
                item["url"] = res.url
                yield item
