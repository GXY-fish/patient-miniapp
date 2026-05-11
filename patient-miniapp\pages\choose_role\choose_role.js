Page({
  data: {},
  choosePatient() {
    wx.redirectTo({ url: '/pages/patient_login/patient_login' });
  },
  chooseDoctor() {
    wx.redirectTo({ url: '/pages/doctor_login/doctor_login' });
  }
});