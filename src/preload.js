const { contextBridge, ipcRenderer } = require('electron');

// レンダラープロセスに公開するAPI
contextBridge.exposeInMainWorld('electronAPI', {
  // 設定関連
  getSettings: () => ipcRenderer.invoke('get-settings'),
  setDownloadPath: () => ipcRenderer.invoke('set-download-path'),

  // URL解析
  analyzeUrl: (url) => ipcRenderer.invoke('analyze-url', url),

  // ダウンロード関連
  downloadVideo: (options) => ipcRenderer.invoke('download-video', options),
  downloadImages: (options) => ipcRenderer.invoke('download-images', options),
  cancelDownload: (id) => ipcRenderer.invoke('cancel-download', id),

  // フォルダを開く
  openFolder: (path) => ipcRenderer.invoke('open-folder', path),

  // イベントリスナー
  onDownloadProgress: (callback) => {
    ipcRenderer.on('download-progress', (event, data) => callback(data));
  },
  onImageDownloadProgress: (callback) => {
    ipcRenderer.on('image-download-progress', (event, data) => callback(data));
  }
});