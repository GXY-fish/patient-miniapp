const { request } = require('../../utils/request');

Page({
  data: {
    messages: []
  },
  onShow() {
    this.loadMessages();
  },
  loadMessages() {
    request({ url: '/messages' })
      .then((data) => {
        this.setData({ messages: Array.isArray(data) ? data : [] });
      })
      .catch(() => {
        wx.showToast({ title: '消息加载失败', icon: 'none' });
      });
  }
});
