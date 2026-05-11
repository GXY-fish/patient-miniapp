const { request } = require('../../utils/request');

Page({
  data: {
    case: {},
    finalRisk: '低',
    complicationTags: '',
    careAdvice: '',
    disposition: ''
  },
  onLoad(options) {
    const caseId = options.case_id;
    if (!caseId) {
      wx.showToast({ title: '缺少 case_id', icon: 'none' });
      return;
    }
    this.setData({ caseId });
    request({ url: `/doctor/cases/${caseId}` })
      .then((data) => {
        this.setData({ case: data });
      })
      .catch(() => {
        wx.showToast({ title: '病例详情加载失败', icon: 'none' });
      });
  },
  onRiskChange(e) {
    const idx = Number(e.detail.value);
    const v = ['低', '中', '高'][idx] || '低';
    this.setData({ finalRisk: v });
  },
  onCompInput(e) {
    this.setData({ complicationTags: e.detail.value });
  },
  onAdviceInput(e) {
    this.setData({ careAdvice: e.detail.value });
  },
  onDispositionInput(e) {
    this.setData({ disposition: e.detail.value });
  },
  submitReview() {
    const caseId = this.data.caseId;
    if (!caseId) return;
    const payload = {
      final_risk_level: this.data.finalRisk,
      complication_tags: this.data.complicationTags ? this.data.complicationTags.split(/\s*,\s*/) : [],
      revision_flag: false,
      revision_reason: null,
      care_advice: this.data.careAdvice || '无',
      disposition: this.data.disposition || '门诊随访',
      urgent_level: null,
      followup_days: 7
    };
    request({ url: `/doctor/cases/${caseId}/review`, method: 'POST', data: payload })
      .then((data) => {
        wx.showToast({ title: '审核已保存', icon: 'success' });
        setTimeout(() => {
          const pages = getCurrentPages();
          const prevPage = pages.length >= 2 ? pages[pages.length - 2] : null;
          if (prevPage && typeof prevPage.loadDashboard === 'function') {
            prevPage.loadDashboard();
          }
          if (prevPage && typeof prevPage.loadCases === 'function') {
            prevPage.loadCases();
          }
          if (prevPage && typeof prevPage.applyFilter === 'function') {
            prevPage.applyFilter(prevPage.data && prevPage.data.activeFilter ? prevPage.data.activeFilter : 'all');
          }
          wx.navigateBack();
        }, 300);
      })
      .catch((err) => {
        wx.showToast({ title: '提交失败', icon: 'none' });
      });
  }
});