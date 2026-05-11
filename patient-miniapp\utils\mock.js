const recentReports = [
  {
    id: 'RPT-20260420-001',
    time: '2026-04-20 10:30',
    status: '已完成',
    riskLevel: '中',
    summary: '造口周围皮肤轻度发红，建议加强清洁与观察。'
  },
  {
    id: 'RPT-20260418-002',
    time: '2026-04-18 09:15',
    status: '待审核',
    riskLevel: '高',
    summary: '疑似造口旁疝风险，请尽快等待医生确认。'
  }
];

const messages = [
  {
    id: 'MSG-001',
    title: '医生已回复',
    content: '您的最新评估报告已完成，请查看护理建议。',
    time: '10:45',
    unread: true
  },
  {
    id: 'MSG-002',
    title: '随访提醒',
    content: '请于本周内重新上传造口图片进行复查。',
    time: '昨天',
    unread: false
  }
];

const dashboard = {
  riskLevel: '中',
  lastReportTime: '2026-04-20 10:30',
  nextFollowupDate: '2026-04-27',
  pendingCount: 2
};

module.exports = {
  recentReports,
  messages,
  dashboard
};
