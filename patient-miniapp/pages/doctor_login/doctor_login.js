const app = getApp();
const { request } = require('../../utils/request');

Page({
  data: {
    phone: '',
    loginPhone: ''
  },
  onShow() {
    wx.setStorageSync('loginRole', 'doctor');
    app.globalData.role = 'doctor';
    this.setData({
      loginPhone: wx.getStorageSync('loginPhone') || '',
      phone: wx.getStorageSync('loginPhone') || ''
    });
  },
  onPhoneInput(e) {
    this.setData({ phone: e.detail.value });
  },
  login() {
    if (!this.data.phone) {
      wx.showToast({ title: '请输入手机号', icon: 'none' });
      return;
    }
    request({
      url: '/auth/login',
      method: 'POST',
      data: {
        phone: this.data.phone,
        code: '000000',
        role: 'doctor'
      }
    })
      .then((data) => {
        wx.setStorageSync('token', data.access_token);
        wx.setStorageSync('loginPhone', this.data.phone);
        wx.setStorageSync('loginRole', 'doctor');
        app.globalData.token = data.access_token;
        app.globalData.role = 'doctor';
        this.setData({ loginPhone: this.data.phone });
        wx.showToast({ title: '登录成功', icon: 'success' });
        setTimeout(() => {
          wx.redirectTo({ url: '/pages/doctor/doctor' });
        }, 150);
      })
      .catch(() => {
        wx.showToast({ title: '登录失败', icon: 'none' });
      });
  }
});