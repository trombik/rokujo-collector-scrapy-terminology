## rokujo-collector-scrapy-terminology

A collection of spiders to scrape terminology and glossaries.

## Requirements

* Python 3
* [git](https://git-scm.com/)
* [uv](https://docs.astral.sh/uv/) (not necessarily a requirement, but strongly recommended)
* [jq](https://jqlang.org/) (optional)

## Install

```console
git clone https://github.com/trombik/rokujo-collector-scrapy-terminology.git
cd rokujo-collector-scrapy-terminology
uv sync
```

## Usage

The following command runs a spider and writes collected JSON items to `output.jsonl`.
See Available Spiders below for the list of spiders.

```console
uv run scrapy crawl -O output.jsonl $SPIDER_NAME
```

For details about the options, see [the official documentation of Scrapy](https://docs.scrapy.org/en/latest/).

### Export to CSV

You can filter by title (or any other attributes) and convert the JSONL output to a CSV file using jq:

```console
jq -r 'select(.title == "MY TITLE") | [.term, .translation, .description, .title, .url, .obtained_at] | @csv' < output.jsonl
```

## Available Spiders

* [jbits](terminology/spiders/jbits.py) ([用語集](https://www.jbits.co.jp/glossary.html) by [翻訳会社ジェイビット](https://www.jbits.co.jp/))

## License

MIT License. See [LICENSE](LICENSE) for details.
