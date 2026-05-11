const app = getApp();

Page({
  data: {
    loginPhone: '',
    loginRole: '',
    roleText: '未选择',
    patientName: '',
    medicalNo: ''
  },
  onShow() {
    const storedProfile = wx.getStorageSync('patientProfile');
    const loginPhone = wx.getStorageSync('loginPhone') || '';
    const loginRole = wx.getStorageSync('loginRole') || '';
    const roleText = loginRole === 'doctor' ? '医生' : (loginRole === 'patient' ? '患者' : '未选择');
    this.setData({
      loginPhone,
      loginRole,
      roleText,
      patientName: storedProfile?.name || '',
      medicalNo: storedProfile?.medicalNo || ''
    });
    app.globalData.role = loginRole;
  },
  goRoleLogin() {
    if (this.data.loginRole === 'doctor') {
      wx.navigateTo({ url: '/pages/doctor_login/doctor_login' });
      return;
    }
    wx.navigateTo({ url: '/pages/patient_login/patient_login' });
  },
  switchIdentity() {
    wx.removeStorageSync('loginRole');
    app.globalData.role = '';
    wx.reLaunch({ url: '/pages/choose_role/choose_role' });
  },
  logout() {
    wx.removeStorageSync('token');
    wx.removeStorageSync('loginPhone');
    app.globalData.token = '';
    wx.showToast({ title: '已退出登录', icon: 'success' });
    setTimeout(() => {
      wx.reLaunch({ url: '/pages/choose_role/choose_role' });
    }, 150);
  }
});
