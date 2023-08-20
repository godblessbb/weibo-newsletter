import openai
import os
import pandas as pd
from datetime import datetime


def read_and_concat_weibo_texts(folder_path):
    # 获取今天的日期，格式为YYYY-MM-DD
    today_date = datetime.now().strftime('%Y-%m-%d')

    # 构建文件路径
    file_path = os.path.join(folder_path, f'{today_date}.csv')

    # 检查文件是否存在
    if os.path.exists(file_path):
        # 读取CSV文件
        df = pd.read_csv(file_path)

        # 获取正文列的内容
        text_content = df['正文'].tolist()

        # 将内容拼接成一个长文本，每一列的内容独自成为一段
        long_text = '\n'.join(text_content)

        return long_text
    else:
        return f"文件 {file_path} 不存在"

def generate_ai_report(long_text):
    openai.api_key = 'YOUR KEY'
    # 通过 `系统(system)` 角色给 `助手(assistant)` 角色赋予一个人设
    messages = [{'role': 'system', 'content': '你是一个专业的财经分析师。你主要关注人工智能技术的发展和遇到的伦理和监管挑战。'}]
    # 在 messages 中加入 `用户(user)` 角色提出第 1 个问题
    messages.append({'role': 'user', 'content': long_text + '以上是过去24小时的新闻汇总，请首先为我筛选出过去一天人工智能领域最值得关注的10条新闻，然后对这10条新闻做出概要。要求：1.请将新闻按顺序编好排列，每行一条新闻，行与行之间不留空行，2.新闻必须出自上面给出的新闻汇总，不得产生与给出文本无关的内容。3.新闻内容包括不限于新产品和新技术、行业动态等'})
    # 调用 API 接口
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-16k-0613',
        messages=messages,
    )
    # 在 messages 中加入 `助手(assistant)` 的回答
    messages.append({
        'role': response['choices'][0]['message']['role'],
        'content': response['choices'][0]['message']['content'],
    })

    # 查看整个对话
    res = messages[2]['content']
    return res

def ai_newsletter():
    # 调用函数并传递文件夹路径
    folder_path = 'weibo_event'
    result = read_and_concat_weibo_texts(folder_path)
    newsletter = generate_ai_report(result)

    return newsletter


if __name__ == "__main__":
    pass
