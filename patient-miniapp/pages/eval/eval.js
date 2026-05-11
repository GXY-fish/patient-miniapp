const app = getApp();
const { request } = require('../../utils/request');

Page({
  data: {
    photos: [],
    uploadedPhotos: [],
    bindingNeeded: false,
    symptom: {
      painScore: 0,
      oozeLevel: '无',
      bleeding: false,
      odor: false,
      fever: false,
      prolapseSuspect: false,
      note: ''
    },
    submitting: false
  },
  getPatientId() {
    return app.globalData.patientId || wx.getStorageSync('patientId') || '';
  },
  refreshBindingState() {
    const patientId = this.getPatientId();
    this.setData({ bindingNeeded: !patientId });
    return patientId;
  },
  goPatientLogin() {
    wx.navigateTo({ url: '/pages/patient_login/patient_login' });
  },
  onShow() {
    this.refreshBindingState();
  },
  choosePhoto() {
    wx.chooseMedia({
      count: 3,
      mediaType: ['image'],
      sourceType: ['camera', 'album'],
      success: (res) => {
        const files = res.tempFiles.map((item) => item.tempFilePath);
        this.uploadPhotos(files);
      }
    });
  },
  uploadPhotos(files) {
    const remaining = 3 - this.data.photos.length;
    const targets = files.slice(0, remaining);
    targets.forEach((filePath) => {
      wx.uploadFile({
        url: `${app.globalData.baseUrl}/uploads`,
        filePath,
        name: 'file',
        success: (res) => {
          try {
            const data = JSON.parse(res.data);
            const photos = this.data.photos.concat([filePath]);
            const uploadedPhotos = this.data.uploadedPhotos.concat([data.path]);
            this.setData({
              photos,
              uploadedPhotos
            });
          } catch (error) {
            wx.showToast({ title: '图片解析失败', icon: 'none' });
          }
        },
        fail: () => {
          wx.showToast({ title: '图片上传失败', icon: 'none' });
        }
      });
    });
  },
  onPainChange(e) {
    this.setData({ 'symptom.painScore': Number(e.detail.value) });
  },
  onOozeChange(e) {
    this.setData({ 'symptom.oozeLevel': e.detail.value });
  },
  toggleFlag(e) {
    const key = e.currentTarget.dataset.key;
    this.setData({ [`symptom.${key}`]: !this.data.symptom[key] });
  },
  onNoteInput(e) {
    this.setData({ 'symptom.note': e.detail.value });
  },
  submit() {
    const patientId = this.refreshBindingState();
    if (!patientId) {
      wx.showModal({
        title: '需要绑定患者档案',
        content: '请先完成患者登录并绑定档案，再返回提交评估。',
        confirmText: '去登录',
        cancelText: '取消',
        success: (res) => {
          if (res.confirm) {
            this.goPatientLogin();
          }
        }
      });
      return;
    }
    if (this.data.photos.length < 1) {
      wx.showToast({ title: '请至少上传1张照片', icon: 'none' });
      return;
    }
    this.setData({ submitting: true });
    request({
      url: '/evaluations',
      method: 'POST',
      data: {
        patient_id: Number(patientId),
        photos: this.data.uploadedPhotos,
        symptoms: this.data.symptom
      }
    })
      .then((data) => {
        wx.showModal({
          title: '提交成功',
          content: `已生成评估单，编号：${data.id}`,
          showCancel: false
        });
        this.setData({ photos: [], uploadedPhotos: [] });
      })
      .catch(() => {
        wx.showToast({ title: '提交失败', icon: 'none' });
      })
      .finally(() => {
        this.setData({ submitting: false });
      });
  }
});
