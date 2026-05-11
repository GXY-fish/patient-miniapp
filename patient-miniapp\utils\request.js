function request(options) {
  const app = getApp();
  const token = app.globalData.token || wx.getStorageSync('token') || '';
  const header = {
    'content-type': 'application/json'
  };
  if (token) {
    header.Authorization = `Bearer ${token}`;
  }

  return new Promise((resolve, reject) => {
    wx.request({
      url: `${app.globalData.baseUrl}${options.url}`,
      method: options.method || 'GET',
      data: options.data || {},
      header,
      success(res) {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data);
        } else {
          reject(res);
        }
      },
      fail(err) {
        reject(err);
      }
    });
  });
}

module.exports = {
  request
};
