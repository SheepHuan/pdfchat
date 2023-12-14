#!/usr/bin/env python3
from datetime import datetime
from typing import List, Tuple
from uuid import uuid4
from nicegui import Client, ui
import hashlib
import os
from nougat_api import predict
SAVE_PATH = "tmp/"

cached_pdf = None
cached_mmd = None
def upload_pdf(e):
    global cached_pdf
    os.makedirs(SAVE_PATH,exist_ok=True)
    uploaded_pdf_path = os.path.join(SAVE_PATH, e.name)
    # 将内容写入文件
    with open(uploaded_pdf_path, 'wb') as f:
        f.write(e.content.read())
    # 计算MD5缓存PDF
    ui.notify(f'Uploaded {e.name}')
    cached_pdf = uploaded_pdf_path

def split_pdf():
    if cached_pdf!=None:
        cached_mmd,md5=predict(cached_pdf)
        ui.markdown(cached_mmd)
        # with ui.tab("Markdown"):
        #     ui.html(cached_mmd)
    else:
        ui.notify("no pdf cached!",type="negative")
    pass

@ui.page('/')
async def main(client: Client):
    anchor_style = r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}'
    ui.add_head_html(f'<style>{anchor_style}</style>')

    # the queries below are used to expand the contend down to the footer (content can then use flex-grow to expand)
    # ui.query('.q-page').classes('flex')
    # ui.query('.nicegui-content').classes('w-full')
    with ui.header():
        ui.upload(multiple=False,on_upload=lambda e: upload_pdf(e)).classes('max-w-full')
        ui.button('nougat', on_click=split_pdf)
        ui.button('translation', on_click=lambda: ui.notify('Translation now'))
        ui.button('clear', on_click=lambda: ui.notify('clear now'))
    with ui.tabs().classes('w-full') as tabs:
        chat_tab = ui.tab('Markdown')
        logs_tab = ui.tab('Translation')
        
ui.run(
    title='Chat with ChatGLM3',
    host="0.0.0.0",
    port = 8101
)