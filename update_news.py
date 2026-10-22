import os
import requests
import re

# 1. 模拟或获取最新的财经新闻与新股数据（后续可替换为专业财经 API）
def fetch_financial_news():
    return [
        "美股芯片股昨夜大涨，AI应用加速落地，预计今日A股半导体与算力板块走势较强。",
        "央行持续释放流动性，支持消费与实体经济发展，对高股息蓝筹与消费板块形成支撑。",
        "国际油价近期回调，避险情绪缓和，整体宏观经济环境偏向稳健。"
    ]

def fetch_stock_hot():
    return [
        {
            "name": "中芯国际", "code": "688981", "badge": "热门龙头", "badge_class": "badge-red",
            "desc": "受益于国产替代加速与芯片行业复苏，近期机构关注度较高。"
        },
        {
            "name": "XX科技", "code": "今日申购", "badge": "新股日历", "badge_class": "badge-orange",
            "desc": "今日A股新股申购，主营智能制造领域，建议关注打新机会。"
        }
    ]

# 2. 调用 DeepSeek AI 生成通俗易懂的早报内容
def generate_ai_content(news_list, stock_list):
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("未检测到 API Key，使用默认优质排版")
        return None

    prompt = f"""
    你是一个贴心的老年理财助手。请根据以下新闻，生成两部分 HTML 代码：
    第一部分：3条新闻列表，每条格式为：<li class="news-item"><span class="badge badge-red">利好科技</span> 新闻内容...</li>
    第二部分：2条股票关注列表，每条格式为：
    <div class="stock-item"><div class="stock-header"><div><span class="stock-name">股票名</span><span class="stock-code">(代码)</span></div><span class="badge 标签类名">标签名</span></div><div class="stock-desc"><strong>关注理由：</strong>理由描述...</div></div>

    原始新闻：{news_list}
    原始股票：{stock_list}
    请直接返回生成好的 HTML 片段，不要包含 markdown 标记。
    """

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        res = requests.post("https://api.deepseek.com/v1/chat/completions", json=data, headers=headers)
        result = res.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        print("AI 生成失败:", e)
        return None

# 3. 自动更新 index.html
def update_html():
    if not os.path.exists("index.html"):
        print("未找到 index.html")
        return

    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    # 这里可以接入 AI 动态生成，或者使用默认的高级排版更新日期
    print("正在更新网页...")
    
    # 保存文件
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("index.html 更新成功！")

if __name__ == "__main__":
    update_html()
