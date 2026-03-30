# Mermaid CLI 参考指南

## 工具信息

**工具**：`@mermaid-js/mermaid-cli`（官方 CLI）

## 首次使用准备

如果 puppeteer 未下载，运行一次即可（下载约200MB）：

```bash
npx -y @mermaid-js/mermaid-cli mmdc -i /dev/null -o /dev/null
```

## 单图转换命令

```bash
# 将 mermaid 代码写入临时文件
cat > /tmp/diagram.mmd << 'EOF'
flowchart TD
    A[开始] --> B[步骤1]
    B --> C[结束]
EOF

# 转换为 PNG（白色背景）
npx -y @mermaid-js/mermaid-cli mmdc \
  -i /tmp/diagram.mmd \
  -o output.png \
  -b white \
  -w 1600 -H 1200
```

## 批量转换脚本

```bash
#!/bin/bash
# mmdc-batch.sh - 批量转换 mermaid 为 PNG

IMAGES_DIR="sections/images"
mkdir -p "$IMAGES_DIR"

# 从 markdown 中提取 mermaid 代码块并转换
for md_file in sections/*.md; do
    # 检查是否包含 mermaid 代码块
    if grep -q '```mermaid' "$md_file"; then
        echo "处理: $md_file"

        # 提取 mermaid 代码块（第一个）
        sed -n '/```mermaid/,/```/p' "$md_file" | sed '1d;$d' > /tmp/extracted.mmd

        # 生成输出文件名
        base_name=$(basename "$md_file" .md)
        output_file="$IMAGES_DIR/${base_name}-diagram.png"

        # 转换
        npx -y @mermaid-js/mermaid-cli mmdc \
          -i /tmp/extracted.mmd \
          -o "$output_file" \
          -b white \
          -w 1600 -H 1200

        echo "  -> $output_file"
    fi
done
```

## CLI 参数说明

| 参数 | 说明 |
|------|------|
| `-i <file>` | 输入的 .mmd 文件 |
| `-o <file>` | 输出的图片文件（.png/.svg） |
| `-b <bg>` | 背景颜色（white/transparent） |
| `-w <px>` | 输出宽度（像素） |
| `-H <px>` | 输出高度（像素） |
| `-t <theme>` | 主题（default/mermaid/neutral/dark） |

## 适合 Mermaid 的场景

- 工作流程（步骤1 → 步骤2 → 步骤3）
- 状态机（状态A ↔ 状态B）
- 时序图（用户 → 系统 → 数据库）
- 类图、ER 图
- 甘特图

## 语法注意事项

- 节点标签用中文可以直接写，无需引号：`A[开始]`
- 中文字体需要确保系统有中文字体支持
- 复杂中文字符串可用引号包裹：`A["中文节点"]`

## 常见问题

### 问题1：首次运行卡住（下载 puppeteer）

**现象**：命令执行后长时间无输出

**解决**：
```bash
# 先手动下载 puppeteer（约200MB，只需一次）
npx -y @mermaid-js/mermaid-cli mmdc -i /dev/null -o /dev/null
```

### 问题2：中文显示为方块

**原因**：系统缺少中文字体

**解决**：
```bash
# macOS 安装中文字体
brew install --cask adobe-source-han-sans-cn-fonts
# 或使用系统字体
```

### 问题3：图片尺寸不合适

**解决**：调整 `-w`（宽度）和 `-H`（高度）参数
```bash
npx -y @mermaid-js/mermaid-cli mmdc -i diagram.mmd -o diagram.png -w 1920 -H 1080
```
