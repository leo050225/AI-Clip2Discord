```markdown
# Clipboard AI Image Analyzer (剪貼簿 AI 圖片分析工具)

[English Version](#english-version) | [中文版](#中文版)

---

# 中文版

這是一個常駐在背景運行的自動化工具。它會持續監控您的系統剪貼簿，當偵測到您複製了新的圖片時，會自動將圖片傳送給 AI 模型進行視覺分析，並將分析結果直接推送到您指定的 Discord 頻道中。

## 💡 結構說明
```
SCREENSHOT_TO_AI/
├── dist/                  # 編譯或打包後的輸出目錄
├── src/                   # 核心原始程式碼
│   ├── discord_notifier.py # Discord 通知傳送邏輯
│   ├── main.py            # 程式啟動入口
│   └── model_factory.py    # AI 模型實例化與管理工廠
├── .env.example           # 環境變數範例檔 (請複製並更名為 .env)
├── README.md              # 專案說明文件
└── requirements.txt       # Python 依賴套件清單
```

src/: 存放主要的邏輯程式碼。

main.py: 負責執行主要的流程控制。

model_factory.py: 封裝了模型的建立過程，方便抽換或擴充不同的 AI 模型。

discord_notifier.py: 專門處理與 Discord Webhook 或 Bot 的對接。

.env.example: 為了安全性，敏感資訊（如 API Keys）不會上傳到版本控制。請根據此範本建立 .env 檔案。

requirements.txt: 使用 pip install -r requirements.txt 即可快速安裝專案環境。

## 🌟 功能特色

* **自動化監控**：自動偵測剪貼簿中的圖片，無需手動上傳。
* **AI 視覺分析**：使用強大的大型語言模型（LLM）來分析圖片內容。
* **Discord 整合**：分析完成後自動將文字結果發送至 Discord Webhook。
* **智慧防呆**：自動計算圖片的 MD5 Hash，避免重複分析同一張圖片。
* **開箱即用的執行檔**：提供打包好的 `.exe` 檔案，免安裝 Python 環境即可直接使用。


**執行檔的 AI 模型預設行為 (Fallback 機制)：**
此執行檔已經預設配置了**容錯機制**。它會先嘗試使用 **Gemini 2.0 Flash** 分析圖片；如果 Gemini 發生錯誤或配額耗盡，系統會自動切換使用 **GitHub Models 的 GPT-4o**；若再次失敗，則會使用 **GPT-4o-mini** 進行最後嘗試。這確保了服務的高度穩定性。

## ⚙️ 安裝與環境設定 (開發者/原始碼模式)

如果您想從原始碼執行，請按照以下步驟操作：

1. 安裝所需套件：
   ```bash
   pip install -r requirements.txt
   ```
2. 複製 `.env.example` 並重新命名為 `.env`，然後填寫以下資訊：
   ```env
   # Google AI Studio (Gemini)
   GOOGLE_API_KEY=您的_GOOGLE_API_KEY

   # GitHub Models
   GITHUB_TOKEN=您的_GITHUB_TOKEN

   # Discord Webhook
   DISCORD_WEBHOOK_URL=您的_DISCORD_WEBHOOK_URL

   # Custom Prompt(自訂提示詞)
   AI_PROMPT="請描述這張圖片的內容"
   ```
3. 啟動服務：
   ```bash
   python main.py
   ```

## 🛠️ 進階：如何只使用單一 AI 模型？

如果您不想使用預設的容錯機制 (Gemini -> GPT)，只想單獨使用 Gemini 或 GPT，請開啟 `model_factory.py` 檔案並修改 `get_vision_chain` 函式的回傳值：

### 選項 A：只使用 Gemini 
找到 `model_factory.py` 底部的 `return fallback_chain`，將其修改為：
```python
        # return fallback_chain (註解掉或刪除這行)
        return google_llm # 只回傳 Gemini 模型
```

### 選項 B：只使用 GPT-4o
找到 `model_factory.py` 底部的 `return fallback_chain`，將其修改為：
```python
        # return fallback_chain (註解掉或刪除這行)
        return github_4o # 只回傳 GitHub GPT-4o 模型
```

---

# English Version

This is a background automation tool that monitors your system clipboard. Whenever you copy an image, it automatically sends the image to an AI model for visual analysis and pushes the results directly to your specified Discord channel.

## 💡 Component Overview
```
SCREENSHOT_TO_AI/
├── dist/                  # Directory for compiled or bundled output
├── src/                   # Core source code
│   ├── discord_notifier.py # Logic for sending Discord notifications
│   ├── main.py            # Main entry point of the application
│   └── model_factory.py    # Factory for AI model instantiation and management
├── .env.example           # Template for environment variables
├── README.md              # Project documentation
└── requirements.txt       # List of Python dependencies
```

src/: Contains the primary application logic.

main.py: Handles the main workflow and execution control.

model_factory.py: Encapsulates the model creation process, allowing for easy swapping or expansion of different AI models.

discord_notifier.py: Dedicated module for Discord Webhook or Bot integration.

.env.example: For security purposes, sensitive information (like API Keys) is not tracked by version control. Please copy this file and rename it to .env to configure your settings.

requirements.txt: Run pip install -r requirements.txt to quickly set up the project environment

## 🌟 Features

* **Automated Monitoring**: Automatically detects images in the clipboard, eliminating manual uploads.
* **AI Vision Analysis**: Utilizes powerful Large Language Models (LLMs) to analyze image content.
* **Discord Integration**: Automatically sends the text analysis results to a Discord Webhook.
* **Smart Duplication Prevention**: Calculates the MD5 hash of images to avoid processing the same image twice.
* **Ready-to-use Executable**: Comes with a pre-packaged `.exe` file so you can use it without setting up a Python environment.

**Default AI Behavior of the Executable (Fallback Mechanism):**
This executable is pre-configured with a **fallback sequence**. It will first attempt to analyze the image using **Gemini 2.0 Flash**. If Gemini encounters an error or runs out of quota, it will automatically switch to **GitHub Models' GPT-4o**. If that fails as well, it will make a final attempt using **GPT-4o-mini**. This guarantees high reliability.

## ⚙️ Installation & Setup (Developer / Source Code Mode)

If you wish to run the tool from the source code, please follow these steps:

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` and rename it to `.env`, then fill in your credentials:
   ```env
   # Google AI Studio (Gemini)
   GOOGLE_API_KEY=your_google_api_key

   # GitHub Models
   GITHUB_TOKEN=your_github_token

   # Discord Webhook
   DISCORD_WEBHOOK_URL=your_discord_webhook_url

   # Custom Prompt
   AI_PROMPT="Please describe this image."
   ```
3. Start the service:
   ```bash
   python main.py
   ```

## 🛠️ Advanced: How to use ONLY Gemini or ONLY GPT?

If you want to bypass the default fallback sequence (Gemini -> GPT) and strictly use only Gemini or only GPT, open the `model_factory.py` file and modify the return value of the `get_vision_chain` method:

### Option A: Use ONLY Gemini
Locate `return fallback_chain` at the bottom of `model_factory.py` and change it to:
```python
        # return fallback_chain (Comment out or delete this line)
        return google_llm # Return only the Gemini model
```

### Option B: Use ONLY GPT-4o
Locate `return fallback_chain` at the bottom of `model_factory.py` and change it to:
```python
        # return fallback_chain (Comment out or delete this line)
        return github_4o # Return only the GitHub GPT-4o model
```
```