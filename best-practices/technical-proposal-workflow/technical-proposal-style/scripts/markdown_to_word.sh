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

    # 查找并排序文件
    mapfile -t FILES < <(find "$INPUT_SOURCE" -maxdepth 1 -name "$FILE_PATTERN" -type f | sort)
    if [ ${#FILES[@]} -eq 0 ]; then
        echo "错误: 未找到匹配的文件: $INPUT_SOURCE/$FILE_PATTERN"
        exit 1
    fi
    echo "  找到 ${#FILES[@]} 个文件"

    for file in "${FILES[@]}"; do
        echo "  合并: $(basename "$file")"
        echo -e "\n\n" >> "$TEMP_MERGED"
        cat "$file" >> "$TEMP_MERGED"
    done
fi

# ============================================================
# 步骤2: 预处理 Markdown
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

# 6. 【关键修复】确保表格头行和分隔行之间没有空行
#   Markdown表格格式：| xxx | xxx | 后面紧跟 |---|---|
content = re.sub(r'(\|[^\n]+\|)\n\n(\|[-:| ]+\|)', r'\1\n\2', content)

# 7. 确保表格前后有空行（但表格内部没有多余空行）
content = re.sub(r'([^\n])\n(\|[^\n]+\|\n\|[-:| ]+\|)', r'\1\n\n\2', content)

with open('_temp_cleaned.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("  格式清理完成")
PYTHON_SCRIPT

# ============================================================
# 步骤3: Pandoc 转换
# ============================================================
echo "=== 步骤3: Pandoc 转换 ==="
pandoc "$TEMP_CLEANED" \
    -o "$OUTPUT_FILE" \
    --from=markdown+pipe_tables+tex_math_dollars \
    --to=docx \
    --mathml \
    --wrap=none \
    --standalone \
    --metadata title="技术方案"

# ============================================================
# 步骤4: 后处理 Word 格式
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
    import sys
except ImportError:
    print("  警告: python-docx 未安装，跳过后处理")
    print("  提示: 运行 'pip3 install python-docx' 安装")
    sys.exit(0)

output_file = sys.argv[1] if len(sys.argv) > 1 else '技术方案_完整版.docx'
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
for i, para in enumerate(doc.paragraphs):
    text = para.text.strip()
    is_heading = para.style.name.startswith('Heading') if para.style else False

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
print("  Word 格式后处理完成")
PYTHON_SCRIPT "$OUTPUT_FILE"

# ============================================================
# 步骤5: 清理临时文件
# ============================================================
echo "=== 步骤5: 清理临时文件 ==="
rm -f "$TEMP_MERGED" "$TEMP_CLEANED"

echo ""
echo "=== 完成 ==="
echo "输出文件: $OUTPUT_FILE"
