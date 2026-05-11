App({
  globalData: {
    userInfo: null,
    token: '',
    role: 'patient',
    patientId: '',
    baseUrl: 'http://127.0.0.1:8000/api/v1'
  },
  onLaunch() {
    const token = wx.getStorageSync('token') || '';
    const role = wx.getStorageSync('loginRole') || '';
    const patientId = wx.getStorageSync('patientId') || '';
    this.globalData.token = token;
    this.globalData.role = role;
    this.globalData.patientId = patientId;
    // 如果没有已选身份，启动时让小程序打开选择身份页（已配置为首页）
  }
});
