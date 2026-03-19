#!/bin/bash
# Markdown 转 Word 脚本（技术标书/方案专用版）
# 解决：公式、标题符号、段落空格、字体颜色、宋体、首行缩进、\newpage、表格问题
#
# 使用方法:
#   ./markdown_to_word.sh [选项] <输入文件或目录> [输出文件]
#
# 选项:
#   -o, --output FILE    输出文件名 (默认: 技术方案_完整版.docx)
#   -f, --files PATTERN  目录模式下的文件匹配模式 (默认: *.md)
#   -h, --help           显示帮助信息
#
# 示例:
#   # 单文件转换
#   ./markdown_to_word.sh 合并内容.md
#   ./markdown_to_word.sh -o 投标文件.docx 合并内容.md
#
#   # 目录模式：合并目录下所有 .md 文件（按文件名排序）
#   ./markdown_to_word.sh sections/
#   ./markdown_to_word.sh -o 投标文件.docx -f "*.md" 章节目录/
#
# 依赖:
#   - pandoc:  brew install pandoc
#   - python-docx: pip3 install python-docx

set -e

# 默认参数
OUTPUT_FILE="技术方案_完整版.docx"
FILE_PATTERN="*.md"
INPUT_SOURCE=""
TEMP_MERGED="_temp_merged.md"
TEMP_CLEANED="_temp_cleaned.md"
INPUT_MODE=""

# 帮助信息
show_help() {
    cat << 'EOF'
Markdown 转 Word 转换脚本（技术标书专用版）

使用方法:
  ./markdown_to_word.sh [选项] <输入文件或目录> [输出文件]

选项:
  -o, --output FILE    输出文件名 (默认: 技术方案_完整版.docx)
  -f, --files PATTERN  目录模式下的文件匹配模式 (默认: *.md)
  -h, --help           显示帮助信息

输入模式:
  1. 单文件模式: 第一个参数是 .md 文件
     ./markdown_to_word.sh 合并内容.md
     ./markdown_to_word.sh -o 输出.docx 合并内容.md

  2. 目录模式: 第一个参数是目录
     ./markdown_to_word.sh sections/
     ./markdown_to_word.sh -f "*.md" -o 输出.docx 章节目录/

示例:
  # 单文件转换
  ./markdown_to_word.sh 合并内容.md

  # 指定输出文件
  ./markdown_to_word.sh -o 投标文件.docx 合并内容.md

  # 合并章节目录中的所有文件
  ./markdown_to_word.sh 章节拆分/

依赖:
  pandoc:       brew install pandoc
  python-docx:  pip3 install python-docx
EOF
}

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -f|--files)
            FILE_PATTERN="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            if [ -z "$INPUT_SOURCE" ]; then
                INPUT_SOURCE="$1"
            elif [ -z "$OUTPUT_FILE" ] || [[ "$OUTPUT_FILE" != *.docx ]]; then
                # 如果第二个位置参数看起来像输出文件（以.docx结尾或未设置过）
                if [[ "$1" == *.docx ]] || [ -d "$1" ]; then
                    : # 可能是目录或其他参数，不作为输出文件处理
                else
                    OUTPUT_FILE="$1"
                fi
            fi
            shift
            ;;
    esac
done

# 检查输入
if [ -z "$INPUT_SOURCE" ]; then
    echo "错误: 请指定输入文件或目录"
    show_help
    exit 1
fi

if [ -f "$INPUT_SOURCE" ] && [[ "$INPUT_SOURCE" == *.md ]]; then
    # 单文件模式
    INPUT_MODE="single"
elif [ -d "$INPUT_SOURCE" ]; then
    # 目录模式
    INPUT_MODE="directory"
else
    echo "错误: 输入不存在或不是有效的 .md 文件/目录: $INPUT_SOURCE"
    exit 1
fi

# 检查依赖
if ! command -v pandoc &> /dev/null; then
    echo "错误: pandoc 未安装"
    echo "请运行: brew install pandoc"
    exit 1
fi

echo "=== Markdown 转 Word ==="
echo "输出文件: $OUTPUT_FILE"

# ============================================================
# 步骤1: 合并文件（单文件或目录）
# ============================================================
echo "=== 步骤1: 合并/读取文件 ==="
> "$TEMP_MERGED"

if [ "$INPUT_MODE" == "single" ]; then
    echo "  模式: 单文件"
    echo "  输入: $INPUT_SOURCE"
    cp "$INPUT_SOURCE" "$TEMP_MERGED"
else
    echo "  模式: 目录"
    echo "  目录: $INPUT_SOURCE"
    echo "  匹配: $FILE_PATTERN"

    # 查找并排序文件（Python实现，兼容macOS bash 3.2）
    PYTHON_FILES=$(python3 -c "
import glob, os
pattern = os.path.join('$INPUT_SOURCE', '${FILE_PATTERN}')
files = sorted(glob.glob(pattern))
if not files:
    exit(1)
for f in files:
    print(f)
")
    if [ -z "$PYTHON_FILES" ]; then
        echo "错误: 未找到匹配的文件: $INPUT_SOURCE/$FILE_PATTERN"
        exit 1
    fi
    FILE_COUNT=$(echo "$PYTHON_FILES" | grep -c .)
    echo "  找到 ${FILE_COUNT} 个文件"

    while IFS= read -r file; do
        echo "  合并: $(basename "$file")"
        echo -e "\n\n" >> "$TEMP_MERGED"
        cat "$file" >> "$TEMP_MERGED"
    done <<< "$PYTHON_FILES"
fi

# ============================================================
# 步骤2: 预处理格式（仅做格式规范化，数学公式由 pandoc 直接处理）
# ============================================================
echo "=== 步骤2: 预处理格式 ==="
python3 << 'PYTHON_SCRIPT'
import re

with open('_temp_merged.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 清理 \newpage 指令
content = re.sub(r'\\newpage', '', content)

# 1.1 清理水平分割线 (---)
content = re.sub(r'\n---+\n', '\n\n', content)

# 2. 确保标题前后有空行
content = re.sub(r'([^\n])\n(#{1,6} )', r'\1\n\n\2', content)
content = re.sub(r'(#{1,6} .+)\n([^\n])', r'\1\n\n\2', content)

# 3. 清理多余的连续空行
content = re.sub(r'\n{4,}', '\n\n', content)

# 4. 确保公式块前后有空行
content = re.sub(r'([^\n])\n(\$\$)', r'\1\n\n\2', content)
content = re.sub(r'(\$\$[^\$]+\$\$)\n([^\n])', r'\1\n\n\2', content)

# 5. 清理行尾空格
content = re.sub(r' +\n', '\n', content)

# 6. 确保表格头行和分隔行之间没有空行
content = re.sub(r'(\|[^\n]+\|)\n\n(\|[-:| ]+\|)', r'\1\n\2', content)

# 7. 确保表格前后有空行
content = re.sub(r'([^\n])\n(\|[^\n]+\|\n\|[-:| ]+\|)', r'\1\n\n\2', content)

with open('_temp_cleaned.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("  格式清理完成（数学公式由 pandoc 直接处理，不做预处理）")
PYTHON_SCRIPT

# ============================================================
# 步骤3: Pandoc 转换（直接输出 OMML，不再 --mathml）
# ============================================================
echo "=== 步骤3: Pandoc 转换 ==="
pandoc "$TEMP_CLEANED" \
    -o "$OUTPUT_FILE" \
    --from=markdown+pipe_tables+tex_math_dollars \
    --to=docx \
    --wrap=none \
    --standalone \
    --resource-path=".:sections:images" \
    --metadata title="技术方案"

# ============================================================
# 步骤4: 后处理 Word 格式 + 公式 fallback 处理
# ============================================================
echo "=== 步骤4: Word 格式后处理 ==="
python3 << 'PYTHON_SCRIPT'
try:
    from docx import Document
    from docx.shared import Pt, RGBColor, Twips
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    import re
    import sys
except ImportError:
    print("  警告: python-docx 未安装，跳过后处理")
    print("  提示: 运行 'pip3 install python-docx' 安装")
    sys.exit(0)

# LaTeX → Unicode 符号映射表（用于 fallback 处理 pandoc 无法转换的公式）
latex_map = [
    ('\\Alpha', 'Α'), ('\\Beta', 'Β'), ('\\Gamma', 'Γ'), ('\\Delta', 'Δ'),
    ('\\Theta', 'Θ'), ('\\Lambda', 'Λ'), ('\\Xi', 'Ξ'), ('\\Pi', 'Π'),
    ('\\Sigma', 'Σ'), ('\\Phi', 'Φ'), ('\\Psi', 'Ψ'), ('\\Omega', 'Ω'),
    ('\\alpha', 'α'), ('\\beta', 'β'), ('\\gamma', 'γ'), ('\\delta', 'δ'),
    ('\\theta', 'θ'), ('\\lambda', 'λ'), ('\\mu', 'μ'), ('\\nu', 'ν'),
    ('\\xi', 'ξ'), ('\\pi', 'π'), ('\\rho', 'ρ'), ('\\sigma', 'σ'),
    ('\\tau', 'τ'), ('\\phi', 'φ'), ('\\chi', 'χ'), ('\\psi', 'ψ'),
    ('\\omega', 'ω'), ('\\eta', 'η'), ('\\zeta', 'ζ'), ('\\iota', 'ι'),
    ('\\kappa', 'κ'), ('\\varepsilon', 'ε'), ('\\varpi', 'ϖ'),
    ('\\cdot', '·'), ('\\times', '×'), ('\\div', '÷'), ('\\pm', '±'), ('\\mp', '∓'),
    ('\\geq', '≥'), ('\\le', '≤'), ('\\neq', '≠'), ('\\approx', '≈'), ('\\equiv', '≡'),
    ('\\forall', '∀'), ('\\exists', '∃'), ('\\infty', '∞'),
    ('\\partial', '∂'), ('\\nabla', '∇'),
    ('\\in', '∈'), ('\\notin', '∉'), ('\\subset', '⊂'), ('\\subseteq', '⊆'),
    ('\\supset', '⊃'), ('\\supseteq', '⊇'), ('\\cup', '∪'), ('\\cap', '∩'),
    ('\\emptyset', '∅'), ('\\setminus', '∖'),
    ('\\land', '∧'), ('\\wedge', '∧'), ('\\lor', '∨'), ('\\vee', '∨'),
    ('\\neg', '¬'), ('\\lnot', '¬'), ('\\implies', '⟹'),
    ('\\rightarrow', '→'), ('\\leftarrow', '←'), ('\\leftrightarrow', '↔'),
    ('\\Rightarrow', '⇒'), ('\\Leftarrow', '⇐'), ('\\Leftrightarrow', '⟺'),
    ('\\to', '→'), ('\\gets', '←'), ('\\iff', '⟺'),
    ('\\ldots', '…'), ('\\cdots', '⋯'), ('\\vdots', '⋮'), ('\\ddots', '⋱'),
    ('\\prime', '′'), ('\\degree', '°'),
    ('\\mid', '|'), ('\\vert', '|'),
    ('\\quad', '  '), ('\\qquad', '    '),
    ('\\backslash', '∖'),
    ('\\text{', ''),
    ('\\mathbf{', ''), ('\\mathit{', ''), ('\\mathsf{', ''),
    ('\\mathtt{', ''), ('\\mathbb{', ''), ('\\mathcal{', ''),
    ('\\hat{', ''), ('\\tilde{', ''), ('\\bar{', ''),
    ('\\vec{', ''), ('\\dot{', ''), ('\\ddot{', ''),
    ('\\widehat{', ''), ('\\widetilde{', ''),
]

def apply_latex_map(text):
    for latex, unicode_sym in latex_map:
        text = text.replace(latex, unicode_sym)
    return text

def clean_latex(text):
    """清理残留 LaTeX 命令和多余括号"""
    text = apply_latex_map(text)
    # 清理 \left( → (  \right) → )
    text = re.sub(r'\\left\s*(\()', r'\1', text)
    text = re.sub(r'\\right\s*(\))', r'\1', text)
    text = re.sub(r'\\left\s*(\{)', r'\1', text)
    text = re.sub(r'\\right\s*(\})', r'\1', text)
    text = re.sub(r'\\left\s*(\[)', r'\1', text)
    text = re.sub(r'\\right\s*(\])', r'\1', text)
    text = re.sub(r'\\left\s*\.', '', text)
    text = re.sub(r'\\right\s*\.', '', text)
    text = re.sub(r'\\bigl\s*', '', text)
    text = re.sub(r'\\bigr\s*', '', text)
    text = re.sub(r'\\Bigl\s*', '', text)
    text = re.sub(r'\\Bigr\s*', '', text)
    text = re.sub(r'\\big\s*', '', text)
    text = re.sub(r'\\Big\s*', '', text)
    # 清理 \\, \; \: 等间距命令
    text = re.sub(r'\\[;,:\!]', ' ', text)
    # 清理 \\, \\, 等换行命令
    text = re.sub(r'\\\\', ' ', text)
    # 清理 \\\\drule 等残留
    text = re.sub(r'\\+\w+', '', text)
    # 清理多余空格
    text = re.sub(r'  +', ' ', text)
    text = re.sub(r' *([{}|]) *', r'\1', text)
    return text.strip()

def laatex_to_unicode(text):
    """将 LaTeX 数学符号转为 Unicode（用于 fallback）"""
    text = clean_latex(text)
    # 保留 $$ 包裹的显示公式，去除外层 $$
    m = re.match(r'^\$\$(.+)\$\$$', text.strip(), re.DOTALL)
    if m:
        return m.group(1).strip()
    # 保留 $ 包裹的行内公式
    m = re.match(r'^\$(.+)\$$', text.strip())
    if m:
        return m.group(1).strip()
    return text.strip()

# 检测段落是否包含 pandoc fallback 的原始 LaTeX（而非 OMML 公式）
# 如果段落以 $$ 开头/结尾，或包含未转换的 begin/end，则认为需要 fallback
def looks_like_unconverted_math(text):
    if not text.strip():
        return False
    # 如果文本包含典型的 LaTeX 数学命令但不是 OMML，则需要 fallback
    has_latex = bool(re.search(r'\\frac|\\begin|\\left|\\right|\\tau|\\gamma|\\sigma', text))
    # 检查是否已经是纯 Unicode（无反斜杠）
    is_clean = '\\' not in text
    return has_latex and not is_clean

output_file = '最终方案.docx'
doc = Document(output_file)

def set_run_font(run, font_name='宋体', font_size=12):
    """设置文字格式：字体、大小、颜色"""
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.font.color.rgb = RGBColor(0, 0, 0)
    r = run._element
    rPr = r.get_or_add_rPr()
    for child in list(rPr):
        if child.tag == qn('w:rFonts'):
            rPr.remove(child)
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    rFonts.set(qn('w:eastAsia'), font_name)
    rPr.insert(0, rFonts)

# 处理段落
fallback_count = 0
for i, para in enumerate(doc.paragraphs):
    text = para.text.strip()
    is_heading = para.style.name.startswith('Heading') if para.style else False

    # 检查是否是 pandoc fallback 的 LaTeX 公式段落
    if looks_like_unconverted_math(text) and not is_heading:
        # 将 LaTeX 转为 Unicode text
        unicode_text = laatex_to_unicode(text)
        # 清空段落内容并重新设置文本
        for run in para.runs:
            run._element.getparent().remove(run._element)
        # 添加新的 Unicode 文本
        new_run = para.add_run(unicode_text)
        new_run.font.name = 'Cambria Math'
        new_run.font.size = Pt(12)
        set_run_font(new_run, 'Cambria Math', 12)
        fallback_count += 1

    if not is_heading and text:
        # 正文格式：首行缩进、1.5倍行距、无段前段后间距
        para.paragraph_format.first_line_indent = Twips(420)  # 2字符
        para.paragraph_format.line_spacing = 1.5
        para.paragraph_format.space_before = Pt(0)
        para.paragraph_format.space_after = Pt(0)

    for run in para.runs:
        if is_heading:
            # 标题用黑体，取消斜体
            if 'Heading 1' in para.style.name:
                set_run_font(run, '黑体', 16)
            elif 'Heading 2' in para.style.name:
                set_run_font(run, '黑体', 14)
            else:
                set_run_font(run, '黑体', 12)
            run.italic = False
        else:
            # 正文用宋体，小四（12pt）
            set_run_font(run, '宋体', 12)

    if text:
        para.paragraph_format.line_spacing = 1.5
        para.paragraph_format.space_before = Pt(0)
        para.paragraph_format.space_after = Pt(0)

    # 一级标题前插入分页符（除了第一个）
    if para.style.name == 'Heading 1' and i > 0:
        pPr = para._p.get_or_add_pPr()
        pageBreak = OxmlElement('w:pageBreakBefore')
        pPr.append(pageBreak)

# 处理图片段落居中
for para in doc.paragraphs:
    # 判断段落是否包含图片（Drawing元素）
    has_image = False
    for run in para.runs:
        drawing = run._element.find('.//' + qn('w:drawing'))
        if drawing is not None:
            has_image = True
            break
        # mc:AlternateContent 使用原始命名空间避免 KeyError
        mc_ns = '{http://schemas.openxmlformats.org/markup-compatibility/2006}AlternateContent'
        inline_drawing = run._element.find('.//' + mc_ns)
        if inline_drawing is not None:
            has_image = True
            break
    if has_image:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        # 图片段落不加首行缩进
        para.paragraph_format.first_line_indent = None

# 处理题注居中（图 X-Y、表 X-Y）
caption_pattern = re.compile(r'^(图\s*\d+[-\s]\d+|表\s*\d+[-\s]\d+)\s*[：:].*')
for para in doc.paragraphs:
    text = para.text.strip()
    if caption_pattern.match(text):
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER

# 处理表格
for table in doc.tables:
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for row in table.rows:
        is_header = (row == table.rows[0])
        for cell in row.cells:
            for para in cell.paragraphs:
                para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in para.runs:
                    set_run_font(run, '宋体', 10.5)
                    if is_header:
                        run.font.bold = True  # 表头加粗

doc.save(output_file)
print(f"  Word 格式后处理完成（公式 fallback 处理: {fallback_count} 个段落）")
PYTHON_SCRIPT

# ============================================================
# 步骤5: 清理临时文件
# ============================================================
echo "=== 步骤5: 清理临时文件 ==="
rm -f "$TEMP_MERGED" "$TEMP_CLEANED"

echo ""
echo "=== 完成 ==="
echo "输出文件: $OUTPUT_FILE"
