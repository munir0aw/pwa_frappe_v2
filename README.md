# 🌐 PWA Frappe

A **Progressive Web App (PWA)** implementation for the **Frappe Framework**, enabling your applications to be installed and run as native-like apps on both desktop and mobile devices. 🚀

---

## ✨ Features

- ⚡ **Progressive Web App Support** — Turn your Frappe site into an installable PWA
- 📱 **Cross-Platform Installation** — Works on iOS, Android, and Chrome Desktop
- 🔔 **Push Notifications** — VAPID-based notifications (📦 Coming Soon!)
- 💾 **Offline-First Architecture** — Smart caching via Service Worker
- 🎨 **Customizable Manifest** — Icons, colors, display modes & screenshots
- 🧩 **Easy Configuration** — Manage everything from simple Frappe DocTypes

---

## 🧰 Installation

Use [bench](https://github.com/frappe/bench) to install the app:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/omfsakib/pwa_frappe --branch main
bench install-app pwa_frappe
```

---

## ⚙️ Configuration

### 1️⃣ Web App Manifest Setup

Go to **Web App Manifest** in your Frappe Desk and configure:

- 🏷️ **App Name** — Full name of your app
- 🔤 **Short Name** — Short display name
- 🎨 **Theme & Background Colors**
- 🧭 **Display Mode** — `fullscreen`, `standalone`, `minimal-ui`, or `browser`
- 🖼️ **Icons** — Upload in multiple sizes (192x192, 512x512 recommended)
- 📸 **Screenshots & Categories** — For app store appearance

### 2️⃣ Auto PWA Configuration

Click **"Automatically configure PWA"** to:
- ✅ Add manifest link to Website Settings
- ✅ Enable PWA features automatically
- ✅ Optionally enable Desk Mode support

### 3️⃣ Service Worker Setup (Optional)

Visit **Service Worker** doctype to:
- 🔑 Generate VAPID keys *(coming soon)*
- ⚙️ Configure caching and update policies

---

## 💡 Usage

### 🖥️ Desktop (Chrome/Edge)
1. Visit your site
2. Click the **Install icon** in the address bar or select **Install [App Name]**

### 📱 Android
1. Open your site in Chrome
2. Tap **Add to Home Screen** when prompted

### 🍎 iOS (Safari)
1. Open your site in Safari
2. Tap **Share → Add to Home Screen → Add**

Visit `/install` for a full installation guide.

---

## 🧱 Technical Details

### 📁 Directory Structure

```
pwa_frappe/
├── pwa_frappe/
│   ├── doctype/
│   │   ├── service_worker/           # Service Worker config
│   │   └── web_app_manifest/         # Manifest settings
│   └── www/
│       ├── app.html                  # PWA-enabled Desk template
│       ├── manifest.json             # Dynamic manifest endpoint
│       ├── sw.js                     # Service Worker script
│       ├── pwa.js                    # Client-side PWA logic
│       └── install.html              # Installation instructions
```

### 🧠 Service Worker Caching

Caches:
- Static assets (CSS, JS, images)
- Frappe core resources
- Custom app assets defined in hooks

Old caches are auto-cleared upon activation 🔁

### 📄 DocTypes

1. **Web App Manifest** — Main configuration
2. **Manifest Icon / Screenshot / Category / Related App** — Child tables
3. **Service Worker** — Caching & notifications config

---

## 🧑‍💻 Development

### 🔧 Prerequisites

```bash
cd apps/pwa_frappe
pre-commit install
```

### 🧹 Code Quality

- 🐍 **Ruff** — Python linting
- 💅 **Prettier** — Code formatting
- 🧭 **ESLint** — JavaScript linting

### 🧪 Testing

```bash
bench --site [site-name] run-tests --app pwa_frappe
```

---

## 🧩 Customization

### 🔗 Hooks Integration

In your `hooks.py`:

```python
app_include_js = ["/assets/pwa_frappe/js/pwa.js"]
web_include_js = ["/assets/pwa_frappe/js/pwa.js"]
```

### 🧠 Service Worker Extensions

Extend to include custom routes or caching strategies.

---

## 🌍 Browser Support

✅ Chrome (Desktop & Mobile)
✅ Safari (iOS 11.3+)

---

## ⚠️ Limitations

- 🚧 Push notifications not yet implemented
- 🔒 HTTPS required for PWA features
- 🍎 Limited iOS PWA support

---

## 🧰 Troubleshooting

**❌ PWA not installing?**
- Ensure HTTPS is enabled
- Verify `/manifest.json` is reachable
- Check Service Worker registration in DevTools

**🔁 Service Worker not updating?**
- Hard refresh (**Ctrl+Shift+R**)
- Clear site data
- Update cache version

---

## 🤝 Contributing

1. Fork this repo
2. Create a feature branch
3. Run pre-commit checks
4. Submit a PR 🧡

---

## 📜 License

MIT License — see [license.txt](license.txt)

---

## 🙌 Credits

Originally developed by **Md Omar Faruk**
Maintained by the **Frappe Community**

---

## 🧭 Support

- 📚 [Frappe Documentation](https://frappeframework.com)
- 💬 [Frappe Forum](https://discuss.frappe.io)
- 🐛 [Issue Tracker](https://github.com/omfsakib/pwa_frappe/issues)
