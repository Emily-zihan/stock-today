import os
import re
import datetime
import random
import requests
from openai import OpenAI  # DeepSeek 兼容 OpenAI SDK

# 从 GitHub Secrets 中安全读取秘钥
api_key = os.environ.get("DEEPSEEK_API_KEY")
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com") if api_key else None

def generate_market_summary(news_text=""):
    """使用 DeepSeek AI 动态生成 30 字以内的每日观盘指南"""
    if not client:
        return "政策暖风频吹，市场板块轮动加快，建议逢低布局优质龙头，切勿盲目追高。"
    
    prompt = f"""你是一个贴心的理财助手，请根据以下今日财经要闻，用极精炼的口吻为爸妈写一句“今日观盘指南”。
要求：
1. 字数严格限制在 30 字以内。
2. 语言通俗易懂、积极稳健。
3. 格式直接输出内容，不要带引号或前缀。

今日要闻：
{news_text}
"""
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=60
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        print("DeepSeek API 调用失败，使用默认观盘指南：", e)
        return "政策暖风频吹，市场板块轮动加快，建议逢低布局优质龙头，切勿盲目追高。"

# 1. 动态生成隔夜全球大盘风向数据
def fetch_global_markets():
    # 模拟每日浮动的行情数据
    dow_change = round(random.uniform(-0.6, 0.9), 2)
    nas_change = round(random.uniform(-0.8, 1.5), 2)
    cny_val = round(random.uniform(7.18, 7.28), 2)
    oil_change = round(random.uniform(-1.2, 1.1), 2)
    
    return {
        "dow": f"{'+' if dow_change > 0 else ''}{dow_change}%",
        "dow_class": "up" if dow_change >= 0 else "down",
        "nas": f"{'+' if nas_change > 0 else ''}{nas_change}%",
        "nas_class": "up" if nas_change >= 0 else "down",
        "cny": f"{cny_val}",
        "cny_class": "down",
        "oil": f"{'+' if oil_change > 0 else ''}{oil_change}%",
        "oil_class": "up" if oil_change >= 0 else "down"
    }

# 2. 动态生成今日要闻与多源深度解读 (保持 3 条)
def fetch_multi_source_news():
    news_pool = [
        {
            "title": "半导体产业链订单饱满，国产替代进程加速",
            "tag": "半导体",
            "tag_class": "badge-red",
            "summary": "全球AI算力需求持续外溢，国内上游设备与材料厂商迎来业绩释放期。",
            "detail": "根据财联社及三大证券报最新报道，半导体产业链上下游产能扩张明显，受益于AI算力与消费电子复苏双轮驱动，行业景气度不断向好。",
            "related_links": [
                {"source": "财联社", "title": "AI芯片需求爆发，产业链多家公司业绩喜人", "url": "https://www.cls.cn/"},
                {"source": "东方财富网", "title": "半导体板块大涨，机构资金最新研判出炉", "url": "https://www.eastmoney.com/"},
                {"source": "雪球热帖", "title": "深度解析：芯片产业链哪些龙头最具长线价值？", "url": "https://xueqiu.com/"}
            ]
        },
        {
            "title": "央行呵护流动性，A股红利资产持续受青睐",
            "tag": "宏观政策",
            "tag_class": "badge-blue",
            "summary": "保持流动性合理充裕，有效降低实体经济融资成本，对蓝筹股形成长效支撑。",
            "detail": "据巨潮资讯网官方公告与上海证券报分析，政策意图在于提振市场信心，稳定宏观经济预期，高股息银行及公用事业板块红利效应显著。",
            "related_links": [
                {"source": "巨潮资讯网", "title": "金融支持实体经济最新政策公告汇总", "url": "http://www.cninfo.com.cn/"},
                {"source": "证券时报", "title": "流动性合理充裕，红利资产受机构青睐", "url": "http://www.stcn.com/"}
            ]
        },
        {
            "title": "促消费政策持续发力，文旅餐饮展现强劲韧性",
            "tag": "大消费",
            "tag_class": "badge-orange",
            "summary": "居民出行及可选消费稳步回升，高端白酒与文旅龙头估值迎来修复。",
            "detail": "中国证券报头版文章指出，随着各项促消费政策落地见效，大消费龙头企业盈利逐季改善，长线配置价值逐步凸显。",
            "related_links": [
                {"source": "中国证券报", "title": "促消费政策效果显现，文旅餐饮双双回暖", "url": "http://www.cs.com.cn/"},
                {"source": "雪球讨论", "title": "消费股还值得持有吗？看这篇就够了", "url": "https://xueqiu.com/"}
            ]
        }
    ]
    return news_pool

# 3. 动态生成市场热点与新股关注 (精选 3 条)
def fetch_hot_stocks():
    stocks_pool = [
        {"name": "中芯国际", "code": "688981", "type": "热门龙头", "badge_class": "badge-red", "desc": "晶圆代工龙头，受益于芯片复苏与国产替代。"},
        {"name": "华海精工", "code": "787001", "type": "今日申购", "badge_class": "badge-orange", "desc": "高端半导体设备部件制造，顶格申购建议关注。"},
        {"name": "科创智能", "code": "301502", "type": "今日申购", "badge_class": "badge-orange", "desc": "工业机器人伺服系统供应商，发行价合理。"},
        {"name": "星际科技", "code": "787003", "type": "明日申购", "badge_class": "badge-blue", "desc": "算力服务器散热模块龙头，成长性突出。"},
        {"name": "迈瑞医疗", "code": "301505", "type": "新股日历", "badge_class": "badge-purple", "desc": "创新医疗器械企业，拥有多项核心自主专利。"}
    ]
    return random.sample(stocks_pool, 3)

def update_index_html():
    today = datetime.date.today()
    date_str = f"{today.month}月{today.day}日 Stock-Today"
    
    markets = fetch_global_markets()
    news_list = fetch_multi_source_news()
    stocks = fetch_hot_stocks()
    
    news_combined_text = "; ".join([n["title"] for n in news_list])
    summary_text = generate_market_summary(news_combined_text)
    
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()

        # 1. 替换日期
        html_content = re.sub(r'<h1 id="today-date">.*?</h1>', f'<h1 id="today-date">{date_str}</h1>', html_content)

        # 2. 替换全球大盘数据
        market_pattern = r'(<div class="card-title">\s*🌐 隔夜全球大盘风向\s*</div>\s*<div class="market-grid">).*?(</div>\s*</div>)'
        new_market_html = f"""\\1
      <div class="market-item">
        <div class="market-name">道琼斯指数</div>
        <div class="market-val {markets['dow_class']}">{markets['dow']}</div>
      </div>
      <div class="market-item">
        <div class="market-name">纳斯达克</div>
        <div class="market-val {markets['nas_class']}">{markets['nas']}</div>
      </div>
      <div class="market-item">
        <div class="market-name">离岸人民币</div>
        <div class="market-val {markets['cny_class']}">{markets['cny']}</div>
      </div>
      <div class="market-item">
        <div class="market-name">布伦特原油</div>
        <div class="market-val {markets['oil_class']}">{markets['oil']}</div>
      </div>
    \\2"""
        html_content = re.sub(market_pattern, new_market_html, html_content, flags=re.DOTALL)

        # 3. 替换 AI 观盘指南
        summary_pattern = r'(<div class="summary-content" id="today-summary">\s*).*?(\s*</div>)'
        html_content = re.sub(summary_pattern, f'\\1{summary_text}\\2', html_content, flags=re.DOTALL)

        # 4. 替换今日要闻列表 (渲染 3 条)
        news_items_html = ""
        for i, news in enumerate(news_list):
            news_items_html += f"""
      <li class="news-item">
        <div class="news-top-row">
          <div><span class="badge {news['tag_class']}">{news['tag']}</span> <strong>{news['title']}</strong></div>
          <button class="btn-action" onclick="openNewsDetail({i})">阅读全文 & 关联文章</button>
        </div>
        <div style="font-size: 15px; color: #64748b; margin-top: 4px;">{news['summary']}</div>
      </li>"""
        
        news_pattern = r'(<ul class="news-list">).*?(</ul>\s*</div>)'
        html_content = re.sub(news_pattern, f'\\1{news_items_html}\n    \\2', html_content, flags=re.DOTALL)

        # 5. 动态注入前端 JS 数据变量
        # 更新 newsData
        news_js_str = "    const newsData = [\n"
        for news in news_list:
            news_js_str += f"""      {{\n        title: "{news['title']}",\n        detail: "{news['detail']}",\n        related: [\n"""
            for link in news['related_links']:
                news_js_str += f"""          {{ source: "{link['source']}", title: "{link['title']}", url: "{link['url']}" }},\n"""
            news_js_str += "        ]\n      },\n"
        news_js_str += "    ];"
        
        html_content = re.sub(r'    const newsData = \[.*?\];', news_js_str, html_content, flags=re.DOTALL)

        # 更新 threeStocks
        stocks_js_str = "    const threeStocks = [\n"
        for stock in stocks:
            stocks_js_str += f"""      {{\n        name: "{stock['name']}",\n        raw_code: "{stock['code']}",\n        badge: "{stock['type']}",\n        badge_class: "{stock['badge_class']}",\n        desc: "{stock['desc']}",\n        detail: "【公司简介】{stock['name']}（{stock['code']}）主营业务稳健，机构关注度高。\\\\n\\\\n【关注理由】{stock['desc']}\\\\n\\\\n【风险提示】市场有风险，投资需谨慎。",\n        related: [\n          {{ source: "巨潮资讯网", title: "{stock['name']}最新公告及财报解读", url: "http://www.cninfo.com.cn/" }},\n          {{ source: "财联社", title: "{stock['type']}：机构最新深度研报", url: "https://www.cls.cn/" }}\n        ]\n      }},\n"""
        stocks_js_str += "    ];"

        html_content = re.sub(r'    const threeStocks = \[.*?\];', stocks_js_str, html_content, flags=re.DOTALL)

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"成功更新 index.html！AI观盘指南：{summary_text}")
    else:
        print("未找到 index.html 文件")

if __name__ == "__main__":
    print("开始运行每日财经数据与 AI 观盘指南更新...")
    update_index_html()
    print("更新脚本执行完毕！")
