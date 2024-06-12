import os
import subprocess

import typer
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider
from markdownify import markdownify as md
from rich.console import Console


class MySpider(Spider):
    name = "web2mark"

    def __init__(
        self,
        url=None,
        folder=None,
        threads=None,
        depth=None,
        prettify=False,
        verbose=False,
        *args,
        **kwargs,
    ):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]
        self.folder = folder
        self.threads = threads
        self.depth = depth
        self.prettify = prettify
        self.verbose = verbose

    def clean_markdown(self, content):
        content = content.replace("* ```", "```")
        return content

    def parse(self, response):
        content = md(response.css("body").get(), heading_style="ATX")

        content = self.clean_markdown(content)

        filename = f"{response.url.split('/')[-2]}.md"

        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

        with open(f"{self.folder}/{filename}", "w") as f:
            f.write(content)

        if self.prettify:
            try:
                subprocess.run(
                    ["prettier", "--write", f"{self.folder}/{filename}"],
                    check=True,
                    capture_output=not self.verbose,
                )
            except FileNotFoundError:
                typer.Abort(
                    "Prettier not found. Please install it using `npm install -g prettier`"
                )
            except subprocess.CalledProcessError:
                typer.echo("Prettier failed to format the markdown file")

        if self.depth > 0:
            for link in response.css("a::attr(href)").getall():
                if link.startswith("/") and self.depth > 1:
                    yield response.follow(link, self.parse)


def main(
    url: str,
    folder: str = "website",
    threads: int = 1,
    depth: int = 1,
    prettify: bool = False,
    verbose: bool = False,
):
    console = Console()
    with console.status(f"Crawling {url}") as status:
        status.update(f"Crawling {url}", spinner="dots")
        process = CrawlerProcess(
            settings={
                "LOG_LEVEL": "INFO" if verbose else "ERROR",
                "CONCURRENT_REQUESTS_PER_DOMAIN": threads,
                "DEPTH_LIMIT": depth,
            }
        )
        process.crawl(
            MySpider,
            url=url,
            folder=folder,
            threads=threads,
            depth=depth,
            prettify=prettify,
            verbose=verbose,
        )
        process.start()


if __name__ == "__main__":
    typer.run(main)
