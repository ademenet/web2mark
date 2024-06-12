# web2mark

A CLI tool to crawl web pages and convert them to markdown.

## Installation

We recommend using `pipx`:

```bash
pipx install web2mark
```

## Usage

```bash
web2mark https://example.com
```

### Options

- `--folder`: Folder to save the markdown files. Default: `website`.
- `--threads`: Number of threads to use for crawling. Default: 1.
- `--depth`: Depth of the crawl. Default: 1.
- `--prettify`: Prettify the markdown output using Prettier (you need Prettier to be installed locally). Default: False.
- `--verbose`: Show verbose output. Default: False.
