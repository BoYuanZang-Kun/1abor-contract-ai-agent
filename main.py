"""
劳务合同合规审查AI智能体 - 基础框架
功能：OCR解析纸质合同 + 基础劳动法合规检查
"""
import cv2
import pytesseract
import re

# ---------------------- 1. 纸质合同OCR扫描模块 ----------------------
def scan_contract(image_path: str) -> str:
    """
    扫描纸质合同图片，提取文本内容
    :param image_path: 合同图片路径
    :return: 提取到的合同文本
    """
    # 读取图片
    img = cv2.imread(image_path)
    # 预处理（降噪、二值化，提升识别准确率）
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 调用OCR识别中文文本（需要提前安装Tesseract）
    text = pytesseract.image_to_string(gray, lang='chi_sim')
    return text

# ---------------------- 2. 劳动法合规检查模块 ----------------------
def check_compliance(contract_text: str) -> list:
    """
    检查合同是否存在违反劳动法的条款
    :param contract_text: 合同文本
    :return: 违规条款列表
    """
    violations = []

    # 规则1：试用期超过6个月（《劳动合同法》第19条）
    probation_pattern = r'试用期(\d+)个月'
    match = re.search(probation_pattern, contract_text)
    if match:
        months = int(match.group(1))
        if months > 6:
            violations.append(
                f"⚠️ 违规：试用期约定{months}个月，违反《劳动合同法》第19条，劳动合同期限3年以上的，试用期不得超过6个月。"
            )

    # 规则2：约定“自愿放弃社保”
    if "自愿放弃社保" in contract_text or "不缴纳社保" in contract_text:
        violations.append(
            "⚠️ 违规：约定不缴纳社保，违反《社会保险法》第58条，用人单位和劳动者必须依法参加社会保险，缴纳社会保险费。"
        )

    # 规则3：低于当地最低工资标准
    min_wage_pattern = r'工资(\d+)元'
    match = re.search(min_wage_pattern, contract_text)
    if match:
        wage = int(match.group(1))
        # 这里可以替换成你当地的最低工资标准，比如北京2026年是2790元
        if wage < 2000:  # 示例阈值，可修改
            violations.append(
                "⚠️ 违规：约定工资低于当地最低工资标准，违反《劳动法》第48条。"
            )

    return violations

# ---------------------- 3. 主函数：执行审查 ----------------------
def main():
    print("=== 劳务合同AI审查智能体 ===")
    # 示例：读取合同图片（后续替换成你的图片路径）
    image_path = "contract.jpg"
    print(f"正在扫描合同：{image_path}")
    
    # 步骤1：提取合同文本
    contract_text = scan_contract(image_path)
    print("✅ 文本提取完成")
    
    # 步骤2：合规检查
    violations = check_compliance(contract_text)
    print("🔍 合规检查完成，发现以下违规：")
    if violations:
        for v in violations:
            print(v)
    else:
        print("✅ 未发现明显违规条款（请人工复核）")

if __name__ == "__main__":
    main()
