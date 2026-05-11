const { request } = require('../../utils/request');

Page({
  data: {
    dashboard: {
      riskLevel: '--',
      lastReportTime: '--',
      nextFollowupDate: '--',
      pendingCount: 0
    }
  },
  onShow() {
    this.loadDashboard();
    this.loadLatestReport();
  },
  loadDashboard() {
    request({ url: '/doctor/dashboard' })
      .then((data) => {
        this.setData({
          dashboard: {
            riskLevel: data.high_risk_total > 0 ? '高' : '低',
            lastReportTime: this.data.dashboard.lastReportTime,
            nextFollowupDate: '待医生设置',
            pendingCount: data.pending_total
          }
        });
      })
      .catch(() => {
        wx.showToast({ title: '首页数据加载失败', icon: 'none' });
      });
  },
  loadLatestReport() {
    request({ url: '/reports' })
      .then((data) => {
        const latest = Array.isArray(data) && data.length > 0 ? data[0] : null;
        if (!latest) {
          return;
        }
        const dashboard = Object.assign({}, this.data.dashboard, {
          lastReportTime: latest.created_at || latest.time || '--'
        });
        this.setData({
          dashboard
        });
      })
      .catch(() => {});
  },
  goEval() {
    wx.switchTab({ url: '/pages/eval/eval' });
  },
  goReports() {
    wx.switchTab({ url: '/pages/report/report' });
  },
  goMessages() {
    wx.switchTab({ url: '/pages/message/message' });
  }
});
