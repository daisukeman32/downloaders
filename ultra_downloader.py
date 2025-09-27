#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULTRA DOWNLOADER - 最強のメディアダウンローダー
あらゆるセキュリティ、広告、トラップを突破
"""

import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3
import threading
import os
import sys
import time
import random
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse, quote, unquote
import json
import hashlib
import subprocess
import tempfile
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import cloudscraper
import zipfile
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ssl
import socket

# SSL警告を無効化
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

class UltraSecurityBypass:
    """最強のセキュリティ突破システム"""

    def __init__(self):
        """初期化"""
        self.session = requests.Session()
        self.cloudscraper = cloudscraper.create_scraper()
        self.ua = UserAgent()
        self.driver = None
        self.setup_session()
        self.setup_retry_strategy()

    def setup_session(self):
        """最強のセッション設定"""
        # 実際のブラウザに近いヘッダー
        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '"Chromium";v="120", "Google Chrome";v="120", "Not_A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"'
        })
        self.rotate_user_agent()

    def setup_retry_strategy(self):
        """リトライ戦略"""
        retry_strategy = Retry(
            total=10,
            status_forcelist=[403, 429, 500, 502, 503, 504, 520, 521, 522, 523, 524],
            allowed_methods=["HEAD", "GET", "OPTIONS"],
            backoff_factor=2
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def rotate_user_agent(self):
        """User-Agent変更"""
        agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0'
        ]
        agent = random.choice(agents)
        self.session.headers['User-Agent'] = agent
        self.cloudscraper.headers['User-Agent'] = agent

    def add_delay(self, min_delay=1.0, max_delay=3.0):
        """ランダム遅延"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)

    def get_selenium_driver(self):
        """Seleniumドライバー取得"""
        if self.driver is None:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-web-security')
            options.add_argument('--allow-running-insecure-content')
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--ignore-ssl-errors')
            options.add_argument('--ignore-certificate-errors-spki-list')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-plugins')
            options.add_argument('--disable-images')
            options.add_argument(f'--user-agent={self.session.headers["User-Agent"]}')

            try:
                self.driver = webdriver.Chrome(options=options)
                self.driver.set_page_load_timeout(30)
            except:
                print("[!] Chrome WebDriverが見つかりません。通常のHTTPリクエストのみ使用します。")

        return self.driver

    def ultra_request(self, url, max_retries=10):
        """最強のリクエスト"""
        print(f"[*] アクセス開始: {url}")

        # 方法1: 通常のリクエスト
        for attempt in range(3):
            try:
                self.rotate_user_agent()
                if attempt > 0:
                    self.add_delay(2, 5)

                response = self.session.get(
                    url,
                    verify=False,
                    timeout=30,
                    allow_redirects=True
                )

                if response.status_code == 200:
                    print(f"[✓] 通常リクエスト成功")
                    return response

            except Exception as e:
                print(f"[!] 通常リクエスト失敗 {attempt+1}: {str(e)}")

        # 方法2: CloudScraper (Cloudflare突破)
        for attempt in range(3):
            try:
                print(f"[*] CloudScraper試行 {attempt+1}")
                self.add_delay(2, 4)

                response = self.cloudscraper.get(
                    url,
                    timeout=60
                )

                if response.status_code == 200:
                    print(f"[✓] CloudScraper成功")
                    return response

            except Exception as e:
                print(f"[!] CloudScraper失敗 {attempt+1}: {str(e)}")

        # 方法3: Selenium (JavaScript必須サイト)
        driver = self.get_selenium_driver()
        if driver:
            for attempt in range(2):
                try:
                    print(f"[*] Selenium試行 {attempt+1}")
                    self.add_delay(3, 6)

                    driver.get(url)
                    time.sleep(5)  # ページ読み込み待機

                    # JavaScriptの実行を待つ
                    WebDriverWait(driver, 15).until(
                        lambda d: d.execute_script("return document.readyState") == "complete"
                    )

                    html = driver.page_source
                    if html and len(html) > 1000:
                        print(f"[✓] Selenium成功")

                        # レスポンスオブジェクトを模擬
                        class MockResponse:
                            def __init__(self, text, url):
                                self.text = text
                                self.content = text.encode('utf-8')
                                self.status_code = 200
                                self.url = url

                        return MockResponse(html, url)

                except Exception as e:
                    print(f"[!] Selenium失敗 {attempt+1}: {str(e)}")

        print(f"[✗] 全ての方法で失敗: {url}")
        return None

    def download_file(self, url, filepath, callback=None):
        """ファイルダウンロード"""
        print(f"[*] ファイルダウンロード: {url}")

        try:
            self.rotate_user_agent()

            response = self.session.get(
                url,
                stream=True,
                verify=False,
                timeout=60
            )

            if response.status_code == 200:
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0

                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)

                            if callback and total_size > 0:
                                progress = (downloaded / total_size) * 100
                                callback(progress)

                print(f"[✓] ダウンロード完了: {filepath}")
                return True

        except Exception as e:
            print(f"[!] ダウンロードエラー: {str(e)}")

        return False

    def close(self):
        """リソース解放"""
        if self.driver:
            self.driver.quit()


class UltraDownloader:
    """メインアプリケーション"""

    def __init__(self, root):
        """初期化"""
        self.root = root
        self.security = UltraSecurityBypass()
        self.download_folder = str(Path.home() / "Downloads" / "UltraDownloader")
        self.create_download_folder()
        self.setup_window()
        self.create_widgets()
        self.is_downloading = False

    def create_download_folder(self):
        """ダウンロードフォルダ作成"""
        os.makedirs(self.download_folder, exist_ok=True)

    def setup_window(self):
        """ウィンドウ設定"""
        self.root.title("ULTRA DOWNLOADER - 最強版")
        self.root.geometry("800x600")
        self.root.configure(bg='#000000')

    def create_widgets(self):
        """UI作成"""
        # タイトル
        title = tk.Label(
            self.root,
            text="🔥 ULTRA DOWNLOADER 🔥",
            font=('Arial', 24, 'bold'),
            fg='#00ff00',
            bg='#000000'
        )
        title.pack(pady=20)

        # サブタイトル
        subtitle = tk.Label(
            self.root,
            text="あらゆるサイトを突破する最強ダウンローダー",
            font=('Arial', 12),
            fg='#ffffff',
            bg='#000000'
        )
        subtitle.pack(pady=5)

        # URL入力
        url_frame = tk.Frame(self.root, bg='#000000')
        url_frame.pack(pady=20, padx=20, fill='x')

        tk.Label(url_frame, text="URL:", font=('Arial', 14), fg='#ffffff', bg='#000000').pack(side='left')

        self.url_entry = tk.Entry(
            url_frame,
            font=('Arial', 12),
            bg='#333333',
            fg='#ffffff',
            insertbackground='#00ff00',
            relief='flat',
            bd=5
        )
        self.url_entry.pack(side='left', fill='x', expand=True, padx=10)

        # ダウンロードボタン
        download_btn = tk.Button(
            url_frame,
            text="🚀 突破開始",
            font=('Arial', 12, 'bold'),
            bg='#ff0000',
            fg='#ffffff',
            command=self.start_download,
            relief='raised',
            bd=3
        )
        download_btn.pack(side='right', padx=5)

        # 進捗バー
        self.progress_frame = tk.Frame(self.root, bg='#000000')
        self.progress_frame.pack(pady=10, padx=20, fill='x')

        self.progress_label = tk.Label(
            self.progress_frame,
            text="待機中...",
            font=('Arial', 12),
            fg='#00ff00',
            bg='#000000'
        )
        self.progress_label.pack()

        # ログエリア
        log_frame = tk.Frame(self.root, bg='#000000')
        log_frame.pack(pady=20, padx=20, fill='both', expand=True)

        tk.Label(log_frame, text="🔍 システムログ", font=('Arial', 14), fg='#00ff00', bg='#000000').pack(anchor='w')

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            font=('Consolas', 10),
            bg='#111111',
            fg='#00ff00',
            insertbackground='#00ff00',
            relief='flat',
            bd=2
        )
        self.log_text.pack(fill='both', expand=True, pady=5)

        # フッター
        footer_frame = tk.Frame(self.root, bg='#000000')
        footer_frame.pack(pady=10, padx=20, fill='x')

        self.folder_label = tk.Label(
            footer_frame,
            text=f"💾 保存先: {self.download_folder}",
            font=('Arial', 10),
            fg='#ffffff',
            bg='#000000'
        )
        self.folder_label.pack(side='left')

        change_btn = tk.Button(
            footer_frame,
            text="📁 変更",
            font=('Arial', 10),
            command=self.change_folder,
            bg='#333333',
            fg='#ffffff'
        )
        change_btn.pack(side='right')

        self.log("🔥 ULTRA DOWNLOADER 起動完了")
        self.log("💪 最強のセキュリティ突破システム待機中")

    def log(self, message):
        """ログ出力"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def change_folder(self):
        """保存先変更"""
        folder = filedialog.askdirectory(initialdir=self.download_folder)
        if folder:
            self.download_folder = folder
            self.folder_label.config(text=f"💾 保存先: {self.download_folder}")
            self.log(f"📁 保存先変更: {self.download_folder}")

    def start_download(self):
        """ダウンロード開始"""
        if self.is_downloading:
            messagebox.showwarning("警告", "既にダウンロード中です")
            return

        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("エラー", "URLを入力してください")
            return

        self.is_downloading = True
        thread = threading.Thread(target=self.download_worker, args=(url,), daemon=True)
        thread.start()

    def download_worker(self, url):
        """ダウンロードワーカー"""
        try:
            self.progress_label.config(text="🔍 サイト解析中...")
            self.log(f"🎯 ターゲット: {url}")

            # YouTube/動画サイトの場合
            if self.is_video_site(url):
                self.download_video(url)
            else:
                # 通常のWebサイト
                self.download_from_website(url)

        except Exception as e:
            self.log(f"❌ エラー: {str(e)}")
            messagebox.showerror("エラー", f"ダウンロード失敗: {str(e)}")
        finally:
            self.is_downloading = False
            self.progress_label.config(text="待機中...")

    def is_video_site(self, url):
        """動画サイト判定"""
        video_sites = [
            'youtube.com', 'youtu.be', 'vimeo.com', 'dailymotion.com',
            'twitch.tv', 'twitter.com', 'instagram.com', 'tiktok.com',
            'facebook.com', 'reddit.com'
        ]
        return any(site in url.lower() for site in video_sites)

    def download_video(self, url):
        """動画ダウンロード"""
        self.log("🎬 動画サイト検出 - yt-dlp使用")

        try:
            # yt-dlpでダウンロード
            output_template = os.path.join(self.download_folder, '%(title)s.%(ext)s')

            cmd = [
                'yt-dlp',
                '--no-check-certificate',
                '--user-agent', self.security.session.headers['User-Agent'],
                '--referer', url,
                '--extract-flat', 'false',
                '-f', 'best[height<=1080]/best',
                '-o', output_template,
                url
            ]

            self.progress_label.config(text="📥 動画ダウンロード中...")

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            for line in process.stdout:
                if line.strip():
                    self.log(f"📹 {line.strip()}")
                    if '%' in line:
                        # 進捗更新
                        self.root.update_idletasks()

            process.wait()

            if process.returncode == 0:
                self.log("✅ 動画ダウンロード完了")
                self.progress_label.config(text="✅ 完了")
            else:
                error = process.stderr.read()
                raise Exception(f"yt-dlp error: {error}")

        except Exception as e:
            self.log(f"❌ 動画ダウンロードエラー: {str(e)}")
            raise

    def download_from_website(self, url):
        """Webサイトからダウンロード"""
        self.log("🌐 Webサイト解析開始")

        # サイトアクセス
        response = self.security.ultra_request(url)
        if not response:
            raise Exception("サイトにアクセスできませんでした")

        self.log("✅ サイトアクセス成功")
        self.progress_label.config(text="🔍 メディア検索中...")

        # HTML解析
        soup = BeautifulSoup(response.content, 'html.parser')

        # メディアファイル収集
        media_urls = set()

        # 画像
        for img in soup.find_all('img'):
            for attr in ['src', 'data-src', 'data-lazy-src', 'data-original']:
                src = img.get(attr)
                if src:
                    media_urls.add(urljoin(url, src))

        # 動画
        for video in soup.find_all('video'):
            src = video.get('src')
            if src:
                media_urls.add(urljoin(url, src))
            for source in video.find_all('source'):
                src = source.get('src')
                if src:
                    media_urls.add(urljoin(url, src))

        # 音声
        for audio in soup.find_all('audio'):
            src = audio.get('src')
            if src:
                media_urls.add(urljoin(url, src))

        # リンク内のメディアファイル
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and self.is_media_file(href):
                media_urls.add(urljoin(url, href))

        # CSS背景画像
        for element in soup.find_all(style=True):
            style = element['style']
            urls = re.findall(r'url\(["\']?([^"\']+)["\']?\)', style)
            for img_url in urls:
                media_urls.add(urljoin(url, img_url))

        self.log(f"🎯 {len(media_urls)}個のメディアファイルを発見")

        if not media_urls:
            raise Exception("メディアファイルが見つかりませんでした")

        # ダウンロード実行
        self.download_media_files(list(media_urls))

    def is_media_file(self, url):
        """メディアファイル判定"""
        media_extensions = [
            '.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg', '.ico',
            '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv',
            '.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a',
            '.pdf', '.zip', '.rar', '.7z', '.exe', '.dmg'
        ]
        return any(url.lower().endswith(ext) for ext in media_extensions)

    def download_media_files(self, urls):
        """メディアファイル一括ダウンロード"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_folder = os.path.join(self.download_folder, f"media_{timestamp}")
        os.makedirs(save_folder, exist_ok=True)

        total = len(urls)
        success_count = 0

        for i, media_url in enumerate(urls, 1):
            try:
                self.progress_label.config(text=f"📥 {i}/{total} ダウンロード中...")

                # ファイル名生成
                parsed = urlparse(media_url)
                filename = os.path.basename(parsed.path)
                if not filename or filename == '/':
                    ext = media_url.split('.')[-1].split('?')[0][:5]
                    filename = f"file_{i:04d}.{ext}" if ext else f"file_{i:04d}"

                filepath = os.path.join(save_folder, filename)

                # 重複回避
                counter = 1
                original_filepath = filepath
                while os.path.exists(filepath):
                    name, ext = os.path.splitext(original_filepath)
                    filepath = f"{name}_{counter}{ext}"
                    counter += 1

                # ダウンロード実行
                if self.security.download_file(media_url, filepath):
                    success_count += 1
                    self.log(f"✅ {filename}")
                else:
                    self.log(f"❌ {filename}")

                # 遅延
                if i < total:
                    self.security.add_delay(0.5, 1.5)

            except Exception as e:
                self.log(f"❌ {media_url[:50]}... エラー: {str(e)}")

        self.log(f"🎉 ダウンロード完了: {success_count}/{total} 成功")
        self.log(f"📁 保存場所: {save_folder}")
        self.progress_label.config(text=f"✅ 完了 ({success_count}/{total})")

        messagebox.showinfo("完了", f"{success_count}/{total} ファイルのダウンロードが完了しました。")


def main():
    """メイン関数"""
    root = tk.Tk()
    app = UltraDownloader(root)

    def on_closing():
        """終了処理"""
        app.security.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()