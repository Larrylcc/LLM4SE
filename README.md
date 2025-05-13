# LLM4SE

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-370/) [![OpenAI](https://img.shields.io/badge/OpenAI-API-lightgrey)](https://openai.com/)

---

## 简介

本项目为软件工程课程设计，基于阿里云通义千问大模型（Qwen）和 OpenAI 兼容 API，结合 Chroma 向量数据库，实现了一个面向文档的智能问答系统。用户可通过命令行与系统交互，系统会自动检索本地知识库并生成简洁、准确的答案。

---

## 功能特性

- 支持本地 TXT 文档批量加载与分块
- 自动生成文本向量嵌入并存储于 Chroma 向量数据库
- 基于语义检索的相关片段召回
- 利用阿里云 Qwen 大模型进行上下文增强问答（RAG）
- 支持原始大模型直接问答与带检索增强的问答对比
- 命令行交互，实时返回答案

---

## 目录结构

```
.
├── app_aliyun.py           # 主程序，问答系统核心逻辑
├── environment.yml         # Python 环境
├── README.md               # 项目说明文档
├── TXT2025/                # 存放知识库 TXT 文档
└── chroma_persistent_storage/ # Chroma 持久化存储
```

---

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/Larrylcc/LLM4SE.git
cd LLM4SE
```

### 2. 一键配置 Conda 环境

推荐使用 Conda 管理依赖环境，确保兼容性。

```bash
conda env create -f environment.yml
conda activate LLM4SE
```

### 3. 配置阿里云 API Key

在项目根目录下创建 `.env` 文件，内容如下：

```
ALIYUN_API_KEY=你的阿里云通义API密钥
```

### 4. 准备知识库文档

将你的 TXT 文档放入 `TXT2025/` 文件夹。

### 5. 运行问答系统

```bash
python app_aliyun.py
```

系统会自动加载文档、生成向量、初始化数据库，并进入交互式问答模式。

---

## 使用示例

```
====数据库初始化完成，请输入您的问题（输入'exit'退出）====
用户: 面向对象设计分为哪些阶段？
AI: 面向对象设计分为系统设计和对象设计阶段。
```

---

## 依赖环境

- Python 3.12+
- openai
- numpy
- python-dotenv
- chromadb

---

## 贡献

欢迎提交 Issue 或 PR 改进本项目！

---

# English Version

## Introduction

This project implements a document-based Q&A system for Software Engineering course, using Alibaba Cloud Qwen LLM (OpenAI-compatible API) and Chroma vector database. It loads local TXT documents, splits and embeds them, stores in Chroma, and enables semantic retrieval-augmented generation (RAG) for accurate answers.

## Features

- Batch load and split local TXT documents
- Generate text embeddings and store in Chroma vector DB
- Semantic retrieval of relevant document chunks
- RAG-based Q&A using Aliyun Qwen LLM
- Compare vanilla LLM answers and RAG answers
- Command-line interactive interface

## Directory Structure

```
.
├── app_aliyun.py           # Main program
├── requirements.txt        # Python dependencies
├── README.md               # Documentation
├── TXT2025/                # Knowledge base TXT files
└── chroma_persistent_storage/ # Chroma storage
```

## Getting Started

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd <project-folder>
   ```
2. **One-click Conda Environment Setup**

   ```bash
   conda env create -f environment.yml
   conda activate LLM4SE
   ```
3. **Set up Aliyun API Key**

   Create a `.env` file in the root directory:

   ```
   ALIYUN_API_KEY=your_aliyun_api_key
   ```
4. **Prepare TXT documents**

   Put your TXT files in the `TXT2025/` folder.
5. **Run the Q&A system**

   ```bash
   python app_aliyun.py
   ```

---

## Example

```
====数据库初始化完成，请输入您的问题（输入'exit'退出）====
用户: 面向对象设计分为哪些阶段？
AI: 面向对象设计分为系统设计和对象设计阶段。
```

---

## Dependencies

- Python 3.7+
- openai
- numpy
- python-dotenv
- chromadb

---

## Contributing

Pull requests and issues are welcome!
