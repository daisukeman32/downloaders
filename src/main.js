const { app, BrowserWindow, ipcMain, dialog, shell } = require('electron');
const path = require('path');
const fs = require('fs').promises;
const { spawn } = require('child_process');
const axios = require('axios');
const cheerio = require('cheerio');
// 設定ストア（簡易版）
const store = {
  get: (key) => {
    const defaults = {
      downloadPath: app.getPath('downloads'),
      theme: 'dark',
      quality: 'best'
    };
    return defaults[key];
  },
  set: () => {} // 設定保存は後で実装
};

let mainWindow;
let downloadQueue = [];
let activeDownloads = new Map();

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    titleBarStyle: 'hiddenInset',
    backgroundColor: '#1a1a1a',
    icon: path.join(__dirname, '..', 'assets', 'icon.png')
  });

  mainWindow.loadFile(path.join(__dirname, 'index.html'));

  // 開発モード時のみDevTools
  if (process.argv.includes('--dev')) {
    mainWindow.webContents.openDevTools();
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// IPC ハンドラー
ipcMain.handle('get-settings', () => {
  return {
    downloadPath: store.get('downloadPath'),
    theme: store.get('theme'),
    quality: store.get('quality')
  };
});

ipcMain.handle('set-download-path', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ['openDirectory', 'createDirectory'],
    defaultPath: store.get('downloadPath')
  });

  if (!result.canceled && result.filePaths.length > 0) {
    store.set('downloadPath', result.filePaths[0]);
    return result.filePaths[0];
  }
  return null;
});

ipcMain.handle('analyze-url', async (event, url) => {
  try {
    // URLの種類を判定
    const urlType = detectUrlType(url);

    if (urlType === 'video' || urlType === 'youtube') {
      // yt-dlpで動画情報を取得
      return new Promise((resolve, reject) => {
        const ytdlp = spawn('yt-dlp', ['--dump-json', url]);
        let output = '';
        let error = '';

        ytdlp.stdout.on('data', (data) => {
          output += data;
        });

        ytdlp.stderr.on('data', (data) => {
          error += data;
        });

        ytdlp.on('close', (code) => {
          if (code === 0) {
            try {
              const info = JSON.parse(output);
              resolve({
                type: 'video',
                title: info.title || 'Unknown Title',
                thumbnail: info.thumbnail,
                duration: info.duration
              });
            } catch (parseError) {
              reject(new Error('Failed to parse video info'));
            }
          } else {
            reject(new Error(`yt-dlp failed: ${error}`));
          }
        });
      });
    } else {
      // Webページとして解析
      const response = await axios.get(url, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        },
        timeout: 30000
      });

      const $ = cheerio.load(response.data);
      const images = [];

      // img タグから画像を収集
      $('img').each((i, elem) => {
        const src = $(elem).attr('src') || $(elem).attr('data-src');
        if (src) {
          images.push(new URL(src, url).href);
        }
      });

      return {
        type: 'webpage',
        title: $('title').text() || 'Untitled',
        images: [...new Set(images)].slice(0, 50) // 重複除去、最大50個
      };
    }
  } catch (error) {
    throw new Error(`URL解析エラー: ${error.message}`);
  }
});

ipcMain.handle('download-video', async (event, { url, format, outputPath }) => {
  const downloadId = Date.now().toString();

  try {
    const downloadPath = outputPath || store.get('downloadPath');

    // ダウンロードオプション
    const options = format === 'audio'
      ? [
          '-f', 'bestaudio/best',
          '-x',
          '--audio-format', 'mp3',
          '--audio-quality', '0',
          '-o', path.join(downloadPath, '%(title)s.%(ext)s'),
          url
        ]
      : [
          '-f', format || 'best[height<=1080]/best',
          '-o', path.join(downloadPath, '%(title)s.%(ext)s'),
          url
        ];

    return new Promise((resolve, reject) => {
      const ytdlp = spawn('yt-dlp', options);

      activeDownloads.set(downloadId, ytdlp);

      let progress = 0;

      ytdlp.stdout.on('data', (data) => {
        const output = data.toString();
        // 進捗の簡易パース
        const progressMatch = output.match(/(\d+\.?\d*)%/);
        if (progressMatch) {
          progress = parseFloat(progressMatch[1]);
          mainWindow.webContents.send('download-progress', {
            id: downloadId,
            progress: progress
          });
        }
      });

      ytdlp.stderr.on('data', (data) => {
        console.log('yt-dlp stderr:', data.toString());
      });

      ytdlp.on('close', (code) => {
        activeDownloads.delete(downloadId);
        if (code === 0) {
          mainWindow.webContents.send('download-progress', {
            id: downloadId,
            progress: 100
          });
          resolve({ success: true, id: downloadId });
        } else {
          reject(new Error(`Download failed with code ${code}`));
        }
      });

      ytdlp.on('error', (error) => {
        activeDownloads.delete(downloadId);
        reject(error);
      });
    });

  } catch (error) {
    activeDownloads.delete(downloadId);
    throw error;
  }
});

ipcMain.handle('download-images', async (event, { images, outputPath }) => {
  const downloadPath = outputPath || store.get('downloadPath');
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const folderPath = path.join(downloadPath, `images_${timestamp}`);

  // フォルダ作成
  await fs.mkdir(folderPath, { recursive: true });

  const results = [];

  for (let i = 0; i < images.length; i++) {
    try {
      const imageUrl = images[i];
      const response = await axios.get(imageUrl, {
        responseType: 'arraybuffer',
        timeout: 30000,
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
      });

      // ファイル名を生成
      const urlPath = new URL(imageUrl).pathname;
      const filename = path.basename(urlPath) || `image_${i + 1}.jpg`;
      const filepath = path.join(folderPath, filename);

      // 保存
      await fs.writeFile(filepath, response.data);

      results.push({ url: imageUrl, success: true, path: filepath });

      // 進捗を送信
      mainWindow.webContents.send('image-download-progress', {
        current: i + 1,
        total: images.length,
        percentage: ((i + 1) / images.length) * 100
      });

    } catch (error) {
      results.push({ url: images[i], success: false, error: error.message });
    }
  }

  return { folder: folderPath, results };
});

ipcMain.handle('cancel-download', async (event, downloadId) => {
  const process = activeDownloads.get(downloadId);
  if (process) {
    process.kill();
    activeDownloads.delete(downloadId);
    return true;
  }
  return false;
});

ipcMain.handle('open-folder', async (event, folderPath) => {
  shell.showItemInFolder(folderPath);
});

// ヘルパー関数
function detectUrlType(url) {
  // YouTube判定
  if (url.includes('youtube.com/watch') || url.includes('youtu.be/')) {
    return 'youtube';
  }

  // その他の動画サイト判定
  const videoSites = [
    'vimeo.com',
    'dailymotion.com',
    'twitch.tv',
    'twitter.com',
    'instagram.com',
    'tiktok.com'
  ];

  if (videoSites.some(site => url.includes(site))) {
    return 'video';
  }

  return 'webpage';
}