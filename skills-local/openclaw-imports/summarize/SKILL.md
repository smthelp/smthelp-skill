# Summarize 📝

Summary of URLs, files, and media using the `summarize` CLI.

## Usage

Use the `summarize` command to summarize content from a URL, local file, or YouTube video.

### Basic Summary
```bash
summarize "https://example.com"
```

### Specify Model
```bash
summarize "https://example.com" --model google/gemini-2.0-flash-001
```

### YouTube Video
```bash
summarize "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Local File
```bash
summarize "./path/to/document.pdf"
```

### Custom Length
Options: `short`, `medium`, `long`, `xl`, `xxl`
```bash
summarize "https://example.com" --length long
```

### Language
```bash
summarize "https://example.com" --lang zh
```

## Configuration

The CLI uses environment variables for API keys if not using a local provider:
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GEMINI_API_KEY`
- `GROQ_API_KEY`

## Installation

This skill requires the `summarize` CLI:
```bash
brew install steipete/tap/summarize
```
