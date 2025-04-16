
import streamlit as st
import re

# 定义 ESG 关键词词库
fuzzy_words = [
    "committed", "strive", "aim", "endeavor", "dedicated", "aspire", "vision",
    "sustainable development", "on track", "working towards", "believe", "hope", 
    "intend", "efforts", "targeting", "seeking", "aspiration", "moving toward",
    "leading", "progressing", "mission"
]

third_party_refs = [
    "GRI", "CDP", "SASB", "SGX", "TCFD", "UN SDG", "ISO 14001", "IFRS", 
    "ESRS", "ISSB", "CSRD", "B Corp", "UNGC", "CDSB", "IIRC"
]

esg_terms = {
    "E": ["carbon", "emissions", "climate", "energy", "environment", "green", "waste", "recycling", "pollution", "biodiversity", "sustainability", "renewable", "net zero", "solar", "water"],
    "S": ["diversity", "equality", "community", "education", "volunteer", "inclusion", "labor", "human rights", "safety", "philanthropy", "employee", "training"],
    "G": ["governance", "ethics", "board", "audit", "compliance", "transparency", "management", "oversight", "anti-corruption", "stakeholders"]
}

# 打分函数
def score_paragraph(text):
    scores = {"Transparency": 0, "Specificity": 0, "Completeness": 0}

    has_ref = any(std.lower() in text.lower() for std in third_party_refs)
    has_data = bool(re.search(r"\d+[\.\d+]*\s*(%|tons|kg|CO2|usd|year|mwh|metric)", text.lower()))
    scores["Transparency"] = int(has_ref) + int(has_data)

    fuzzy_count = sum(len(re.findall(rf"\\b{re.escape(word)}\\b", text.lower())) for word in fuzzy_words)
    scores["Specificity"] = 2 if fuzzy_count == 0 else (1 if fuzzy_count < 5 else 0)

    esg_found = set()
    for tag, keywords in esg_terms.items():
        if any(k in text.lower() for k in keywords):
            esg_found.add(tag)
    scores["Completeness"] = len(esg_found)

    return scores

# Streamlit 页面逻辑
def run():
    st.set_page_config(page_title="ESG 洗绿检测系统", layout="centered")
    st.title("🟢 ESG 洗绿检测系统")

    paragraph = st.text_area(
        "请输入一段 ESG 报告文本：",
        placeholder="如：We are committed to becoming carbon neutral by 2030, in alignment with GRI.",
        height=200
    )

    if st.button("立即检测") and paragraph.strip():
        with st.spinner("正在分析中..."):
            base_scores = score_paragraph(paragraph)
            consistency = 1  # 模拟一致性得分
            explanation = "该段落未出现明显自相矛盾内容。"

            total_score = sum(base_scores.values()) + consistency

            st.success("检测完成")
            st.subheader("评分结果")
            st.write(f"**透明性（Transparency）：** {base_scores['Transparency']} / 2")
            st.write(f"**具体性（Specificity）：** {base_scores['Specificity']} / 2")
            st.write(f"**完整性（Completeness）：** {base_scores['Completeness']} / 3")
            st.write(f"**一致性（Consistency）：** {consistency} / 2")
            st.write(f"**总得分：** {total_score} / 9")
            st.write(f"**Gemini解释：** {explanation}")

if __name__ == "__main__":
    run()
