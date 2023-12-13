"""
pip install markdown
pip install pdfkit
pip install python-markdown-math

"""

import pdfkit
from markdown import markdown



def convert(input,output):
    with open(input, encoding='utf-8') as f:
        text = f.read()

    html = '<!DOCTYPE html><body><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex/dist/katex.min.css" crossorigin="anonymous"><script src="https://cdn.jsdelivr.net/npm/katex/dist/katex.min.js" crossorigin="anonymous"></script><script src="https://cdn.jsdelivr.net/npm/katex/dist/contrib/mathtex-script-type.min.js" defer></script>{}</body></html>'
    # text = '$$E=mc^2$$'
    text = markdown(text, output_format='html', extensions=['mdx_math'])  # MarkDown转HTML
    html = html.format(text)
    print(html)

    with open(output,'w', encoding='utf-8') as f:
        f.write(html)
    # htmltopdf = fr'D:\htmltopdf\wkhtmltopdf\bin\wkhtmltopdf.exe'
    # configuration = pdfkit.configuration(wkhtmltopdf=htmltopdf)
    # pdfkit.from_string(html, output_path=output, configuration=configuration, options={'encoding': 'utf-8'})  # HTML转PDF


if __name__=="__main__":
    convert("doc.mmd","doc.html")