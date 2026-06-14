// Spoof process.platform to "linux" so hyperframes' isLinuxArm() takes the
// system-Chromium path instead of the @puppeteer/browsers download path that
// rejects android-arm64. arch stays arm64.
try {
  Object.defineProperty(process, 'platform', { value: 'linux', configurable: true });
} catch (e) {
  process.platform = 'linux';
}
