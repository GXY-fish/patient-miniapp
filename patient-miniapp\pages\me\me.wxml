const { request } = require('../../utils/request');

Page({
  data: {
    dashboard: {
      pending_total: 0,
      high_risk_total: 0,
      timeout_total: 0,
      done_today: 0
    },
    cases: [],
    filteredCases: [],
    activeFilter: 'all'
  },
  onShow() {
    this.loadDashboard();
    this.loadCases();
  },
  loadDashboard() {
    request({ url: '/doctor/dashboard' })
      .then((data) => {
        this.setData({
          dashboard: {
            pending_total: data.pending_total || 0,
            high_risk_total: data.high_risk_total || 0,
            timeout_total: data.timeout_total || 0,
            done_today: data.done_today || 0
          }
        });
      })
      .catch(() => {
        wx.showToast({ title: '医生首页加载失败', icon: 'none' });
      });
  },
  loadCases() {
    request({ url: '/doctor/cases' })
      .then((data) => {
        const cases = Array.isArray(data) ? data.slice(0, 50) : [];
        this.setData({
          cases
        });
        this.applyFilter(this.data.activeFilter);
      })
      .catch(() => {
        wx.showToast({ title: '病例列表加载失败', icon: 'none' });
      });
  },
  onStatTap(e) {
    const type = e.currentTarget.dataset.type || 'all';
    this.applyFilter(type);
  },
  onFilterTap(e) {
    const type = e.currentTarget.dataset.type || 'all';
    this.applyFilter(type);
  },
  applyFilter(type) {
    const all = this.data.cases || [];
    let filtered = all;
    if (type === 'pending') {
      filtered = all.filter((item) => item.case_status === 'pending_doctor_review');
    } else if (type === 'high') {
      filtered = all.filter((item) => item.ai_risk_level === '高');
    } else if (type === 'done') {
      filtered = all.filter((item) => item.case_status === 'completed');
    } else if (type === 'timeout') {
      filtered = all.filter((item) => item.case_status === 'timeout');
    }
    this.setData({
      activeFilter: type,
      filteredCases: filtered
    });
    if (type !== 'all') {
      wx.showToast({
        title: `已筛选 ${filtered.length} 条`,
        icon: 'none'
      });
    }
  },
  openCase(e) {
    const caseId = e.currentTarget.dataset.caseid;
    if (!caseId) {
      wx.showToast({ title: '病例编号无效', icon: 'none' });
      return;
    }
    wx.navigateTo({
      url: `/pages/doctor/case_detail?case_id=${caseId}`,
      fail: () => {
        wx.showToast({ title: '打开病例失败', icon: 'none' });
      }
    });
  }
});