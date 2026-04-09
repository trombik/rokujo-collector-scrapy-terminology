# The MIT License (MIT)
#
# Copyright © 2026 Tomoyuki Sakurai
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from datetime import datetime, timezone

import scrapy
from ..items import GlossaryJbitsItem


class JbitsSpider(scrapy.Spider):
    """
    A spider to scrape glossaries published on jbits.co.jp.

    Usage:
        uv run scrapy crawl -O output.jsonl jbits
    """
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
