import os
import re
import requests
from openai import OpenAI  # DeepSeek 兼容 OpenAI SDK

# 从 GitHub Secrets 中安全读取秘钥
api_key = os.environ.get("DEEPSEEK_API_KEY")
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com") if api_key else None

def generate_market_summary(news_text=""):
    """使用 DeepSeek API 生成 30 字以内的观盘指南"""
    if not client:
        return "外盘普涨利好开盘，半导体与大消费板块活跃，建议保持理性，多看少动。"
    
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
        return "外盘普涨利好开盘，半导体与大消费板块活跃，建议保持理性，多看少动。"

# 1. 模拟/对接多源财经资讯（财联社、东方财富、雪球、巨潮资讯等）
def fetch_multi_source_news():
    return [
        {
            "title": "芯片巨头业绩超预期，AI算力需求持续爆发",
            "tag": "半导体",
            "tag_class": "badge-red",
            "summary": "全球AI算力需求强劲，国内产业链设备与材料订单饱满。",
            "detail": "根据财联社及三大证券报最新报道，半导体产业链上下游产能扩张明显，国产替代进程加速。",
            "related_links": [
                {"source": "财联社", "title": "AI芯片需求爆发，产业链多家公司业绩喜人", "url": "https://www.cls.cn/"},
                {"source": "东方财富网", "title": "半导体板块大涨，机构资金最新研判出炉", "url": "https://www.eastmoney.com/"},
                {"source": "雪球热帖", "title": "深度解析：芯片产业链哪些龙头最具长线价值？", "url": "https://xueqiu.com/"}
            ]
        },
        {
            "title": "央行公开市场净投放，保持流动性合理充裕",
            "tag": "宏观政策",
            "tag_class": "badge-blue",
            "summary": "降低实体经济融资成本，对高股息蓝筹与银行板块形成长效支撑。",
            "detail": "据巨潮资讯网官方公告与上海证券报分析，政策意图在于提振市场信心，稳定宏观经济预期。",
            "related_links": [
                {"source": "巨潮资讯网", "title": "金融支持实体经济最新政策公告汇总", "url": "http://www.cninfo.com.cn/"},
                {"source": "证券时报", "title": "流动性合理充裕，红利资产受机构青睐", "url": "http://www.stcn.com/"}
            ]
        },
        {
            "title": "消费与文旅市场复苏，龙头业绩逐季向好",
            "tag": "大消费",
            "tag_class": "badge-orange",
            "summary": "居民出行及可选消费回升，餐饮、旅游及高端白酒稳健复苏。",
            "detail": "中国证券报头版文章指出，随着促消费政策落地见效，大消费龙头估值修复空间打开。",
            "related_links": [
                {"source": "中国证券报", "title": "促消费政策效果显现，文旅餐饮双双回暖", "url": "http://www.cs.com.cn/"},
                {"source": "雪球讨论", "title": "消费股还值得持有吗？看这篇就够了", "url": "https://xueqiu.com/"}
            ]
        }
    ]

# 2. 获取热门股票/新股日历数据
def fetch_ten_stocks():
    return [
        {"name": "中芯国际", "code": "688981", "type": "热门龙头", "badge_class": "badge-red", "desc": "晶圆代工龙头，受益于芯片复苏与国产替代。"},
        {"name": "XX精密", "code": "787001", "type": "今日申购", "badge_class": "badge-orange", "desc": "高端半导体设备部件制造，顶格申购建议关注。"},
        {"name": "YY智能", "code": "301502", "type": "今日申购", "badge_class": "badge-orange", "desc": "工业机器人伺服系统供应商，发行价合理。"},
        {"name": "ZZ科技", "code": "787003", "type": "明日申购", "badge_class": "badge-blue", "desc": "算力服务器散热模块龙头，成长性突出。"},
        {"name": "AA医疗", "code": "301505", "type": "新股日历", "badge_class": "badge-purple", "desc": "创新医疗器械企业，拥有多项核心自主专利。"},
        {"name": "BB材料", "code": "688006", "type": "新股日历", "badge_class": "badge-purple", "desc": "新能源电池关键材料突破者，关注打新机会。"},
        {"name": "CC光电", "code": "787007", "type": "待上市", "badge_class": "badge-blue", "desc": "光芯片封测领域专精特新“小巨人”企业。"},
        {"name": "DD软件", "code": "301508", "type": "待上市", "badge_class": "badge-blue", "desc": "工业软件国产化领军企业，机构关注度高。"},
        {"name": "EE数据", "code": "688009", "type": "热门龙头", "badge_class": "badge-red", "desc": "大数据基础设施建设者，高股息稳健资产。"},
        {"name": "FF装备", "code": "301510", "type": "新股日历", "badge_class": "badge-orange", "desc": "商业航天零部件核心供应商，科技属性强。"}
    ]

def update_index_html():
    # 提取新闻内容并让 DeepSeek 生成观盘指南
    news_list = fetch_multi_source_news()
    news_combined_text = "; ".join([n["title"] for n in news_list])
    
    summary_text = generate_market_summary(news_combined_text)
    
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()

        # 动态替换网页中的 today-summary 文本
        pattern = r'(<div class="summary-content" id="today-summary">\s*).*?(\s*</div>)'
        new_html = re.sub(pattern, f'\\1{summary_text}\\2', html_content, flags=re.DOTALL)

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(new_html)
        
        print(f"成功更新 index.html，AI观盘指南为：{summary_text}")
    else:
        print("未找到 index.html 文件")

if __name__ == "__main__":
    print("开始运行每日财经数据与 AI 观盘指南更新...")
    update_index_html()
    print("更新脚本执行完毕！")
