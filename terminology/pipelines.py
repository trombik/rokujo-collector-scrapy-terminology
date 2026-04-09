# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import re
import unicodedata

from scrapy.exceptions import DropItem

from .items import GlossaryJbitsItem


class TerminologyPipeline:
    def process_item(self, item, spider):
        return item


class GlossaryJbitsItemPipeline:
    def process_item(self, item, spider):
        if not isinstance(item, GlossaryJbitsItem):
            return item

        for field in ["translation", "description"]:
            val = item.get(field, "")
            if val:
                normalized = unicodedata.normalize('NFKC', val)
                item[field] = normalized

        translation = item.get("translation", "")
        description = item.get("description", "")

        # XXX some page have broken HTML, creating invalid items
        if len(description) >= 1024 or len(translation) >= 1024:
            raise DropItem(f"Dropped oversized item: {item.get('term')}")

        # XXX the glossary is not well-structured. perform some guess-work
        # here
        split_pattern = r"[:：]|\*\s+"
        if re.search(split_pattern, translation):
            parts = re.split(split_pattern, translation, maxsplit=1)
            item["translation"] = parts[0].strip()
            extra_desc = parts[1].strip()
            if extra_desc:
                item["description"] = f"{extra_desc} {description}".strip()
        else:
            item["translation"] = translation.strip()

        # normalize separaters
        norm_pattern = r"[;；/／／]\s*"
        item["translation"] = re.sub(norm_pattern, ";", item["translation"])
        item["translation"] = item["translation"].rstrip("*,:").strip()

        return item
