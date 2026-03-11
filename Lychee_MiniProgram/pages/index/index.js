// pages/index/index.js
Page({
  data: {
    imagePath: '',
    aiMode: 'idle', // 'idle', 'safe', 'direct', 'confirm'
    aiCandidates: [] 
  },

  // 触发相机拍照特大按钮
  chooseCamera: function () {
    this.handleChooseImage(['camera']);
  },

  // 触发相册选择特大按钮
  chooseAlbum: function () {
    this.handleChooseImage(['album']);
  },

  handleChooseImage: function (sourceType) {
    const that = this;
    wx.chooseMedia({
      count: 1,
      mediaType: ['image'],
      sourceType: sourceType,
      success(res) {
        const tempFilePath = res.tempFiles[0].tempFilePath;
        that.setData({ 
          imagePath: tempFilePath,
          aiMode: 'loading',
          aiCandidates: []
        });
        
        wx.showLoading({ title: 'AI 极速分析中', mask: true });

        wx.uploadFile({
          url: 'http://127.0.0.1:5000/predict', 
          filePath: tempFilePath,
          name: 'file', 
          success(uploadRes) {
            wx.hideLoading();
            // ── 爬爬哨兵：先检查 HTTP 状态码，防止 4xx/5xx HTML 污染 JSON.parse ──
            if (uploadRes.statusCode !== 200) {
              that.setData({
                aiMode: 'error',
                aiCandidates: [{name: '服务器波动', conf: null, advice: `⚠️ 服务器返回异常状态 (${uploadRes.statusCode})，请稍后重试。`}]
              });
              return;
            }
            let data = {};
            try {
              // 契约修复：防止后端意外爆栈导致前端 JSON 解析雪崩崩溃
              data = JSON.parse(uploadRes.data);
            } catch (e) {
              console.error('JSON Error', e, uploadRes.data.substring(0, 100));
              that.setData({ 
                aiMode: 'error',
                aiCandidates: [{name: '服务开小差', conf: null, advice: '⚠️ 后端数据格式异常，请检查 Flask 是否正常运行。'}] 
              });
              return;
            }

            if(data.status === 'success' && data.candidates) {
              that.setData({ 
                aiMode: data.mode || 'direct', 
                aiCandidates: data.candidates 
              });
            } else {
              that.setData({ 
                aiMode: 'error',
                aiCandidates: [{name: '识别失败', conf: null, advice: data.advice || '❌ 引擎处理失败，未能返回有效方案。'}] 
              });
            }
          },
          fail(err) {
            wx.hideLoading();
            that.setData({ 
              aiMode: 'error',
              aiCandidates: [{name: '网络掉线', conf: 0, advice: '⚠️ 无法连接到联想小新本地服务器，请检查 PM2 状态。'}] 
            });
            console.error('上传失败：', err);
          }
        })
      }
    })
  }
})