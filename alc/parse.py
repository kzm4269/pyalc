def _join_texts(e):
    return (e.text or '') + ''.join(map(_join_texts, e)) + (e.tail or '')


def extract_titles(dom):
    return map(_join_texts, dom.xpath('|'.join([
        '//div[@id="resultsList"]/ul/li/span[@class="midashi"]/h2',
        '//div[@id="resultsList"]/ul/li/span[@class="midashi_je"]/h2',
    ])))
