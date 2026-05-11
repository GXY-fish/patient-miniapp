const app = getApp();
const { request } = require('../../utils/request');

Page({
  data: {
    stomaTypeOptions: ['结肠造口', '回肠造口', '泌尿造口'],
    stomaTypeIndex: 0,
    profile: {
      name: '',
      phone: '',
      medicalNo: '',
      stomaType: '结肠造口',
      surgeryDate: '',
      privacyAuthorized: true,
      id: ''
    },
    loginPhone: ''
  },
  onShow() {
    wx.setStorageSync('loginRole', 'patient');
    app.globalData.role = 'patient';

    const storedProfile = wx.getStorageSync('patientProfile');
    const loginPhone = wx.getStorageSync('loginPhone') || '';
    if (storedProfile) {
      const stomaTypeIndex = this.data.stomaTypeOptions.indexOf(storedProfile.stomaType);
      this.setData({ profile: Object.assign({}, this.data.profile, storedProfile) });
      app.globalData.patientId = storedProfile.id || '';
      if (stomaTypeIndex >= 0) {
        this.setData({ stomaTypeIndex });
      }
    }
    this.setData({ loginPhone });
  },
  onNameInput(e) {
    this.setData({ 'profile.name': e.detail.value });
  },
  onPhoneInput(e) {
    this.setData({ 'profile.phone': e.detail.value });
  },
  onMedicalNoInput(e) {
    this.setData({ 'profile.medicalNo': e.detail.value });
  },
  onStomaTypeChange(e) {
    const index = Number(e.detail.value);
    this.setData({
      stomaTypeIndex: index,
      'profile.stomaType': this.data.stomaTypeOptions[index]
    });
  },
  onSurgeryDateInput(e) {
    this.setData({ 'profile.surgeryDate': e.detail.value });
  },
  login() {
    if (!this.data.profile.phone) {
      wx.showToast({ title: '请输入手机号', icon: 'none' });
      return;
    }
    request({
      url: '/auth/login',
      method: 'POST',
      data: {
        phone: this.data.profile.phone,
        code: '000000',
        role: 'patient'
      }
    })
      .then((data) => {
        wx.setStorageSync('token', data.access_token);
        wx.setStorageSync('loginPhone', this.data.profile.phone);
        wx.setStorageSync('loginRole', 'patient');
        app.globalData.token = data.access_token;
        app.globalData.role = 'patient';
        this.setData({ loginPhone: this.data.profile.phone });
        wx.showToast({ title: '登录成功', icon: 'success' });
        setTimeout(() => {
          wx.switchTab({ url: '/pages/home/home' });
        }, 150);
      })
      .catch(() => {
        wx.showToast({ title: '登录失败', icon: 'none' });
      });
  },
  saveProfile() {
    if (!this.data.profile.name || !this.data.profile.phone || !this.data.profile.surgeryDate) {
      wx.showToast({ title: '请填写完整档案', icon: 'none' });
      return;
    }
      const isUpdating = !!this.data.profile.id || !!wx.getStorageSync('patientId');
    request({
      url: '/patients',
      method: 'POST',
      data: {
        name: this.data.profile.name,
        phone: this.data.profile.phone,
        medical_no: this.data.profile.medicalNo ? this.data.profile.medicalNo.trim() : null,
        stoma_type: this.data.profile.stomaType,
        surgery_date: this.data.profile.surgeryDate,
        privacy_authorized: this.data.profile.privacyAuthorized
      }
    })
      .then((data) => {
        const profile = Object.assign({}, this.data.profile, { id: data.id });
        wx.setStorageSync('patientProfile', profile);
        wx.setStorageSync('patientId', data.id);
        app.globalData.patientId = data.id;
        this.setData({ profile });
          wx.showToast({ title: isUpdating ? '档案已更新' : '档案已保存', icon: 'success' });
      })
      .catch((err) => {
        const detail = err && err.data && err.data.detail ? err.data.detail : '保存失败';
        wx.showToast({ title: detail.length > 12 ? '保存失败' : detail, icon: 'none' });
      });
  }
});