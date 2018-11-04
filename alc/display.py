import sys


def _e(font, text):
    text = text or ''
    if not text or not sys.stdout.isatty():
        return text
    return '\x1b[0;{}m{}\x1b[0m'.format(font, text)


def _format_title(e):
    if e.attrib.get('class') == 'redtext':
        text = _e('1;31', e.text)
    else:
        text = _e('1;34', e.text)
    text += ''.join(map(_format_title, e))
    text += _e('1;34', e.tail)
    return text


def _format_desc(e):
    class_ = e.attrib.get('class')

    if class_ == 'wordclass':
        lines = ['', _e('33', e.text)]
    elif class_ in ['kana', 'attr', 'ex_sentence']:
        return e.tail or ''
    else:
        lines = [e.text or '']

    for i, c in enumerate(e):
        if c.tag == 'li':
            index = e.attrib.get('start') or str(i + 1)
            lines.append(_e('33', index + '. '))
        elif c.tag == 'br':
            lines.append('')

        lines[-1] += _format_desc(c)

    if e.tail:
        lines[-1] += e.tail

    return '\n'.join(map(str.strip, lines))


def _format_result(e):
    title, = e.xpath('|'.join([
        './span[@class="midashi"]/h2',
        './span[@class="midashi_je"]/h2']))
    desc, = e.xpath('./div')

    title = _format_title(title)
    desc = _format_desc(desc)

    return title + '\n' + desc


def display(dom, n=None):
    results = list(dom.xpath('//div[@id="resultsList"]/ul/li'))
    if n is None:
        n = len(results)
    for li in results[:n]:
        try:
            print(_format_result(li), end='\n' * 2)
        except ValueError:
            pass

    info = 'total {} results'.format(len(results))
    print(_e('1;30', '{:-^79s}'.format(info)))
