"""
pip install markdown
pip install pdfkit
pip install python-markdown-math

"""

from markdown import markdown


def convert_html(input,output):
    with open(input, encoding='utf-8') as f:
        text = f.read()

    html = """  
<!DOCTYPE html><body><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex/dist/katex.min.css" crossorigin="anonymous"><script src="https://cdn.jsdelivr.net/npm/katex/dist/katex.min.js" crossorigin="anonymous"></script><script src="https://cdn.jsdelivr.net/npm/katex/dist/contrib/mathtex-script-type.min.js" defer></script>{}</html>
    """

    text = markdown(text, output_format='html', extensions=['mdx_math'])  # MarkDown转HTML
    html = html.format(text)
    with open("test.html", "w", encoding='utf-8') as f:
        f.write(html)
    # HTML(string=html).write_pdf(output)
    # options = {
    # 'page-size':'Letter',
    # 'margin-top':'0.75in',
    # 'margin-right':'0.75in',
    # 'margin-bottom':'0.75in',
    # 'margin-left':'0.75in',
    # 'encoding':"UTF-8",
    # 'no-outline':None
    # }
    # pdfkit.from_string(html, output_path=output,options=options)  # HTML转PDF


if __name__=="__main__":
    convert_html("doc.mmd","doc.html")