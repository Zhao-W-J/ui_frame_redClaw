---
alwaysApply: false
---
# Figma URL 需求解析规则

## 规则描述
当用户提供 Figma URL 时，自动解析设计需求并生成文档。

## 触发条件
- 用户输入包含 Figma URL（格式：`https://www.figma.com/file/` 或 `https://www.figma.com/design/`）

## 处理流程

### 1. 解析 Figma URL
- 从 URL 中提取 `fileKey`
- 如果 URL 包含 `node-id` 参数，提取 `nodeId`

### 2. 获取 Figma 数据
使用 Figma MCP 服务获取设计文件数据：
```
工具：get_figma_data
参数：
- fileKey: 从URL提取的文件键
- nodeId: 从URL提取的节点ID（如果存在）
```

### 3. 整理需求文档
- 根据获取的 Figma 数据生成需求文档
- 文档保存路径：`doc/{需求名称}.md`
- 需求名称基于 Figma 文件名或页面名称生成

### 4. 文档内容要求
- **一比一还原需求**：严格按照设计稿内容描述
- **不添加过多理解**：避免主观解释和扩展
- 包含以下内容：
  - 页面/组件名称
  - 布局结构
  - 视觉元素描述
  - 文本内容
  - 交互元素（按钮、链接等）
  - 颜色和样式信息

### 5. 文档格式模板
```markdown
# {需求名称}

## 来源
- Figma 文件：{文件名}
- URL：{原始URL}
- 解析时间：{时间戳}

## 页面结构
{基于Figma数据的结构描述}

## 视觉元素
{颜色、字体、图标等描述}

## 内容清单
{所有文本内容的列表}

## 交互元素
{按钮、链接、表单等交互组件}

## 布局信息
{尺寸、间距、对齐等布局细节}
```

## 执行示例
当用户输入：
```
请解析这个Figma设计：https://www.figma.com/file/abc123/MyDesign?node-id=1%3A2
```

系统将：
1. 提取 fileKey: `abc123`
2. 提取 nodeId: `1:2`
3. 调用 Figma MCP 获取数据
4. 生成文档 `doc/MyDesign.md`
5. 按模板格式整理需求内容

## 注意事项
- 确保 Figma MCP 服务可用
- 处理 URL 解析错误的情况
- 文档名称避免特殊字符
- 保持原始设计意图，不做主观修改