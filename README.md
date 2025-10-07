# Static Site Generator

A custom-built static site generator written in Python that converts Markdown content into a complete HTML website.

## Features

- **Markdown to HTML conversion** - Converts Markdown files to semantic HTML
- **Multiple block types** - Supports headings, paragraphs, code blocks, quotes, ordered/unordered lists
- **Inline formatting** - Handles bold, italic, code, links, and images
- **Recursive directory processing** - Automatically processes nested content directories
- **Static asset copying** - Copies static files (images, CSS, etc.) to output directory
- **Template system** - Uses a simple template with title and content placeholders
- **Configurable base path** - Supports deployment to subdirectories

## Project Structure

```
├── content/             # Markdown source files
├── static/              # Static assets (images, CSS)
│   └── images/
│   └── index.css
├── src/                 # Python source code
│   ├── main.py          # Entry point and page generation
│   ├── block.py         # Block-level Markdown parsing
│   ├── inline.py        # Inline Markdown parsing
│   ├── htmlnode.py      # Base HTML node class
│   ├── leafnode.py      # Leaf HTML nodes
│   ├── parentnode.py    # Parent HTML nodes
│   └── textnode.py      # Text nodes with formatting
├── template.html        # HTML template
└── docs/                # Generated site output
```

## Installation

This project requires Python 3.10+.

## Usage

### Generate the site

```bash
./build.sh
```

### Run tests

```bash
./test.sh
```

### Local development server

```bash
./main.sh
```

This generates the site and starts a local server on port 8888.

## Supported Markdown Syntax

### Block-level elements

- **Headings**: `# H1` through `###### H6`
- **Paragraphs**: Regular text separated by blank lines
- **Code blocks**: Fenced with triple backticks
- **Quotes**: Lines starting with `>`
- **Unordered lists**: Lines starting with `- `
- **Ordered lists**: Lines starting with `1. `, `2. `, etc.

### Inline elements

- **Bold**: `**text**`
- **Italic**: `_text_`
- **Code**: `` `text` ``
- **Links**: `[text](url)`
- **Images**: `![alt](url)`

## How It Works

1. **Content processing**: The generator recursively scans the `content/` directory for Markdown files
2. **Markdown parsing**: Each file is parsed into block-level elements (headings, paragraphs, lists, etc.)
3. **Inline processing**: Within each block, inline formatting (bold, italic, links, etc.) is processed
4. **HTML generation**: The parsed content is converted to HTML nodes and rendered
5. **Template injection**: The generated HTML is injected into the template with the extracted title
6. **Asset copying**: Static assets from `static/` are copied to the output directory
7. **Output**: Complete HTML files are written to the `docs/` directory

## License

This project is part of the Boot.dev curriculum.
