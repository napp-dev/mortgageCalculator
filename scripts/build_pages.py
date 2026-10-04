from pathlib import Path
import html
import json
import re
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
CONFIG = json.loads((ROOT / 'site.json').read_text(encoding='utf-8'))
BASE = CONFIG['base_path'].rstrip('/')
CONTACT_EMAIL = CONFIG['contact_email']
DOCUMENT_KINDS = ['privacy', 'terms', 'support']
EXTERNAL_SCHEMES = {'https', 'mailto'}
LOCALES = {locale['code']: locale for locale in CONFIG['locales']}


def page_url(source):
    relative = source.relative_to(ROOT)
    if relative == Path('index.md'):
        return BASE + '/'
    return BASE + '/' + relative.with_suffix('').as_posix() + '/'


def link(label, target, source):
    parsed = urlparse(target)
    if parsed.scheme:
        if parsed.scheme not in EXTERNAL_SCHEMES:
            raise ValueError(f'Only HTTPS and mailto external links are supported: {source}: {target}')
        href = target
    else:
        destination = (source.parent / target).resolve()
        if not destination.is_relative_to(ROOT) or not destination.is_file():
            raise ValueError(f'Missing local link: {source}: {target}')
        href = page_url(destination)
    return f'<a href="{html.escape(href, quote=True)}">{emphasis(label)}</a>'


def emphasis(text):
    parts = text.split('**')
    if len(parts) % 2 == 0:
        raise ValueError(f'Unbalanced bold marker: {text}')
    return ''.join(
        f'<strong>{html.escape(part)}</strong>' if index % 2 else html.escape(part)
        for index, part in enumerate(parts)
    )


def inline(text, source):
    output = []
    cursor = 0
    for match in re.finditer(r'\[([^\]\n]+)\]\(([^)\n]+)\)', text):
        output.append(emphasis(text[cursor:match.start()]))
        output.append(link(match[1], match[2], source))
        cursor = match.end()
    output.append(emphasis(text[cursor:]))
    return ''.join(output)


def render_markdown(source):
    blocks = []
    paragraph = []
    items = []
    headings = []

    def flush():
        if paragraph:
            blocks.append('<p>' + inline(' '.join(paragraph), source) + '</p>')
            paragraph.clear()
        if items:
            blocks.append('<ul>' + ''.join('<li>' + inline(item, source) + '</li>' for item in items) + '</ul>')
            items.clear()

    lines = source.read_text(encoding='utf-8').splitlines()
    if lines and lines[0] == '---':
        raise ValueError(f'Front matter is not supported: {source}')
    for line in lines:
        if not line.strip():
            flush()
            continue
        heading = re.fullmatch(r'(#{1,3}) (.+)', line)
        if heading:
            flush()
            level, title = len(heading[1]), heading[2]
            slug = re.sub(r'[^\w]+', '-', title.casefold()).strip('-')
            blocks.append(f'<h{level} id="{html.escape(slug, quote=True)}">{html.escape(title)}</h{level}>')
            headings.append((level, title))
        elif line.startswith('- '):
            if paragraph:
                flush()
            items.append(line[2:])
        elif line.startswith('  ') and items:
            items[-1] += ' ' + line.strip()
        else:
            if items:
                flush()
            paragraph.append(line)
    flush()
    if [level for level, _ in headings].count(1) != 1 or headings[0][0] != 1:
        raise ValueError(f'Exactly one leading title is required: {source}')
    return '\n'.join(blocks), headings[0][1]


def document_page(locale, kind):
    source = ROOT / locale['code'] / f'{kind}.md'
    article, title = render_markdown(source)
    language_links = []
    for item in CONFIG['locales']:
        address = f'{BASE}/{item["code"]}/{kind}/'
        current = ' aria-current="page"' if item['code'] == locale['code'] else ''
        language_links.append(
            f'<a href="{address}" lang="{item["language"]}" hreflang="{item["language"]}"{current}>'
            f'{html.escape(item["label"])}</a>'
        )
    nav = (
        f'<details class="languages"><summary>{html.escape(locale["home"])}</summary>'
        f'<nav aria-label="{html.escape(locale["home"], quote=True)}">{"".join(language_links)}</nav></details>'
    )
    alternates = ''.join(
        f'<link rel="alternate" hreflang="{item["language"]}" href="{CONFIG["origin"]}{BASE}/{item["code"]}/{kind}/">'
        for item in CONFIG['locales']
    )
    return template(locale['language'], locale['app_name'], title, page_url(source), nav, article, alternates)


def template(language, brand, title, canonical, navigation, content, alternates=''):
    return f'''<!doctype html>
<html lang="{language}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(title, quote=True)}">
<link rel="canonical" href="{CONFIG['origin']}{canonical}">
{alternates}
<link rel="stylesheet" href="{BASE}/assets/style.css">
</head>
<body>
<header class="site-header"><a class="brand" href="{BASE}/">{html.escape(brand)}</a>{navigation}</header>
<main>{content}</main>
<footer><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a><span>{html.escape(brand)} · {CONFIG['updated']}</span></footer>
</body>
</html>
'''


def write(destination, page):
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(page, encoding='utf-8')


def build():
    count = 0
    for locale in CONFIG['locales']:
        for kind in DOCUMENT_KINDS:
            write(ROOT / locale['code'] / kind / 'index.html', document_page(locale, kind))
            count += 1
    for alias, target in CONFIG.get('aliases', {}).items():
        if alias in LOCALES or target not in LOCALES:
            raise ValueError(f'Alias must point from a free path to a locale: {alias} -> {target}')
        for kind in DOCUMENT_KINDS:
            write(ROOT / alias / kind / 'index.html', document_page(LOCALES[target], kind))
            count += 1
    index_content, title = render_markdown(ROOT / 'index.md')
    write(ROOT / 'index.html', template('en', CONFIG['title'], title, BASE + '/', '', index_content))
    print(f'Built {count + 1} HTML pages.')


if __name__ == '__main__':
    build()
