const { request } = require('../../utils/request');

Page({
  data: {
    reports: []
  },
  onShow() {
    this.loadReports();
  },
  loadReports() {
    request({ url: '/reports' })
      .then((data) => {
        const toRisk = (item) => {
          if (item.disposition && item.disposition.indexOf('就诊') >= 0) {
            return { riskLevel: '高', riskClass: 'high' };
          }
          return { riskLevel: '中', riskClass: 'medium' };
        };

        const reports = Array.isArray(data) ? data.map((item) => {
          const risk = toRisk(item);
          return {
            riskLevel: risk.riskLevel,
            riskClass: risk.riskClass,
            id: `RPT-${item.id}`,
            time: item.created_at || '--',
            status: item.disposition || '已完成',
            summary: item.final_conclusion || item.care_advice || ''
          };
        }) : [];
        this.setData({ reports });
      })
      .catch(() => {
        wx.showToast({ title: '报告加载失败', icon: 'none' });
      });
  }
});
