// シンプル化したレンダラープロセス

// DOM要素
const elements = {
  urlInput: document.getElementById('url-input'),
  pasteBtn: document.getElementById('paste-btn'),
  controls: document.getElementById('controls'),
  formatBtns: document.querySelectorAll('.format-btn'),
  downloadBtn: document.getElementById('download-btn'),
  progressContainer: document.getElementById('progress-container'),
  progressFill: document.getElementById('progress-fill'),
  progressPercent: document.getElementById('progress-percent'),
  cancelBtn: document.getElementById('cancel-btn'),
  statusText: document.getElementById('status-text'),
  downloadPath: document.getElementById('download-path'),
  changePath: document.getElementById('change-path')
};

// 状態管理
let currentUrl = '';
let currentFormat = 'video';
let currentDownloadId = null;

// 初期化
document.addEventListener('DOMContentLoaded', async () => {
  await loadSettings();
  setupEventListeners();
  setupProgressListeners();
});

// 設定読み込み
async function loadSettings() {
  try {
    const settings = await window.electronAPI.getSettings();
    elements.downloadPath.textContent = formatPath(settings.downloadPath);
  } catch (error) {
    console.error('Settings error:', error);
  }
}

// イベントリスナー
function setupEventListeners() {
  // URL入力
  elements.urlInput.addEventListener('input', handleUrlInput);
  elements.urlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && currentUrl) startDownload();
  });

  // ペーストボタン
  elements.pasteBtn.addEventListener('click', async () => {
    const text = await navigator.clipboard.readText();
    elements.urlInput.value = text;
    handleUrlInput();
  });

  // フォーマット選択
  elements.formatBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      elements.formatBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentFormat = btn.dataset.format;
    });
  });

  // ダウンロード
  elements.downloadBtn.addEventListener('click', startDownload);
  elements.cancelBtn.addEventListener('click', cancelDownload);

  // パス変更
  elements.changePath.addEventListener('click', changeDownloadPath);
}

// 進捗リスナー
function setupProgressListeners() {
  window.electronAPI.onDownloadProgress((data) => {
    updateProgress(data.progress);
  });

  window.electronAPI.onImageDownloadProgress((data) => {
    updateProgress(data.percentage);
  });
}

// URL入力処理
function handleUrlInput() {
  const url = elements.urlInput.value.trim();

  if (isValidUrl(url)) {
    currentUrl = url;
    elements.controls.classList.remove('hidden');
    updateStatus('Ready');
  } else {
    currentUrl = '';
    elements.controls.classList.add('hidden');
    if (url) updateStatus('Invalid URL');
  }
}

// ダウンロード開始
async function startDownload() {
  if (!currentUrl) return;

  try {
    updateStatus('Analyzing...');
    elements.downloadBtn.disabled = true;

    // URL解析
    const analysis = await window.electronAPI.analyzeUrl(currentUrl);

    // プログレス表示
    elements.controls.classList.add('hidden');
    elements.progressContainer.classList.remove('hidden');
    updateStatus('Downloading...');

    if (analysis.type === 'video') {
      // 動画/音声ダウンロード
      const result = await window.electronAPI.downloadVideo({
        url: currentUrl,
        format: currentFormat === 'audio' ? 'audio' : 'best'
      });
      currentDownloadId = result.id;
    } else {
      // 画像ダウンロード
      const result = await window.electronAPI.downloadImages({
        images: analysis.images.slice(0, 50) // 最大50枚
      });

      updateStatus('Complete');
      resetUI();
    }

  } catch (error) {
    updateStatus('Error: ' + error.message);
    resetUI();
  }
}

// キャンセル
async function cancelDownload() {
  if (currentDownloadId) {
    await window.electronAPI.cancelDownload(currentDownloadId);
    currentDownloadId = null;
    updateStatus('Cancelled');
    resetUI();
  }
}

// 進捗更新
function updateProgress(percent) {
  elements.progressFill.style.width = `${percent}%`;
  elements.progressPercent.textContent = `${Math.round(percent)}%`;

  if (percent >= 100) {
    updateStatus('Complete');
    setTimeout(resetUI, 1000);
  }
}

// UI リセット
function resetUI() {
  elements.progressContainer.classList.add('hidden');
  elements.controls.classList.remove('hidden');
  elements.downloadBtn.disabled = false;
  elements.progressFill.style.width = '0%';
  elements.progressPercent.textContent = '0%';
  currentDownloadId = null;
}

// ステータス更新
function updateStatus(text) {
  elements.statusText.textContent = text;
}

// パス変更
async function changeDownloadPath() {
  const newPath = await window.electronAPI.setDownloadPath();
  if (newPath) {
    elements.downloadPath.textContent = formatPath(newPath);
  }
}

// ユーティリティ
function isValidUrl(string) {
  try {
    new URL(string);
    return true;
  } catch (_) {
    return false;
  }
}

function formatPath(path) {
  const parts = path.split('/');
  if (parts.length > 3) {
    return `.../${parts.slice(-2).join('/')}`;
  }
  return path;
}