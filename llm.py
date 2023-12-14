from transformers import AutoTokenizer, AutoModel
import requests
import json
prompt = f"""
你现在是一个markdown文本翻译工具,将文本的英文翻译成中文.我希望你遵循以下规则:
1. 不要翻译标题(例如, ### Abstract),只需要翻译正文部分.
2. 不要翻译latex公式,表格以及代码块。例如: $\alpha$; ```c++ ....```.
3. 仍然保留原本的文章结构.
请按照上面的规则，翻译文本.
"""

base_url = "http://127.0.0.1:8101"

def create_chat_completion(model, messages, functions, use_stream=False):
    data = {
        "functions": functions,  # 函数定义
        "model": model,  # 模型名称
        "messages": messages,  # 会话历史
        "stream": use_stream,  # 是否流式响应
        "max_tokens": 12000,  # 最多生成字数
        "temperature": 0.5,  # 温度
        "top_p": 0.7,  # 采样概率
    }

    response = requests.post(f"{base_url}/v1/chat/completions", json=data, stream=use_stream)
    if response.status_code == 200:
        if use_stream:
            # 处理流式响应
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')[6:]
                    try:
                        response_json = json.loads(decoded_line)
                        content = response_json.get("choices", [{}])[0].get("delta", {}).get("content", "")
                        print(content)
                    except:
                        print("Special Token:", decoded_line)
        else:
            # 处理非流式响应
            decoded_line = response.json()
            content = decoded_line.get("choices", [{}])[0].get("message", "").get("content", "")
            # print(content)
            return content
    else:
        print("Error:", response.status_code)
        return None

def simple_chat(input,use_stream=True):
    functions = None
    chat_messages = [
        {
            "role": "system",
            "content": "You are ChatGLM3, a large language model trained by Zhipu.AI. Follow the user's instructions carefully. Respond using markdown.",
        },
        {
            "role": "user",
            "content": f"{prompt}\n请帮我翻译以下文本:{input}"
        }
    ]
    
    
    
    create_chat_completion("chatglm3-6b", messages=chat_messages, functions=functions, use_stream=use_stream)


import re

def split_sections(markdown_text,out):
    sections = re.split(r'\n(?=# )|\n(?=## )', markdown_text)
    sections = [section.strip() for section in sections if section.strip()]
    contents = []
    for section in sections:
        content = simple_chat(section,use_stream=False)
        contents.append(content)
    
    open(out,"w").write("\n".join(contents))



if __name__=="__main__":
    text = open("tmp/doc.mmd","r").read()
    sections = split_sections(text,"tmp/doc.html")
    # 