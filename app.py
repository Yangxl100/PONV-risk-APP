
import streamlit as st

# 标准化函数
def standardize_gdf15(raw_value, mean=800, std=50):
    return (raw_value - mean) / std

# Apfel评分计算
def calculate_apfel(gender, smoking_history, previous_ponv, postop_opioids):
    score = 0
    if gender == '女':
        score += 1
    if not smoking_history:
        score += 1
    if previous_ponv:
        score += 1
    if postop_opioids:
        score += 1
    return score

# 风险决策树
def risk_decision_tree(apfel_score, gdf15_value, gdf15_threshold=0):
    if apfel_score < 3:
        return "中低风险"
    else:
        if gdf15_value < gdf15_threshold:
            return "极高风险"
        else:
            return "高风险"

# 干预建议输出
def output_recommendation(risk_level):
    templates = {
        "极高风险": "建议加强止吐药物联合应用，增加术后监测频率。",
        "高风险": "建议常规止吐药物预防，术后注意观察。",
        "中低风险": "建议常规护理及定期随访。"
    }
    return templates.get(risk_level, "暂无建议")

# Streamlit UI
st.set_page_config(page_title="PONV风险评估系统", layout="centered")
st.title("🎯 手术后恶心呕吐（PONV）风险评估系统")

st.subheader("📋 请输入患者信息")

with st.form("risk_form"):
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("性别", ["女", "男"])
        smoking_history = st.checkbox("有吸烟史")
    with col2:
        previous_ponv = st.checkbox("既往有PONV或晕动病史")
        postop_opioids = st.checkbox("术后计划使用阿片类药物")

    gdf15_raw = st.number_input("GDF-15检测值（pg/ml）", min_value=0.0, step=0.1)

    submitted = st.form_submit_button("点击评估")

if submitted:
    apfel_score = calculate_apfel(gender, smoking_history, previous_ponv, postop_opioids)
    gdf15_standard = standardize_gdf15(gdf15_raw, mean=800, std=50)
    risk_level = risk_decision_tree(apfel_score, gdf15_standard)
    recommendation = output_recommendation(risk_level)

    st.success(f"🌡 Apfel评分：{apfel_score} 分")
    st.info(f"🧠 GDF-15标准化值：{gdf15_standard:.2f}")
    st.warning(f"📊 综合风险等级：{risk_level}")
    st.write("💡 干预建议：")
    st.markdown(f"> {recommendation}")
