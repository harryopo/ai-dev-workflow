# App 开发全流程指南（iOS / Android / 跨端）

> 来源：第二轮调研 R2
> 用途：阶段 5 编码实施时的 App 开发参考

## 1. 三大路线对比

| 维度 | iOS 原生 (SwiftUI) | Android 原生 (Compose) | 跨端 (RN/Flutter/MAUI) |
|------|------|------|------|
| 开发语言 | Swift | Kotlin | JS/TS、Dart、C# |
| 开发成本 | 单平台无复用 | 单平台无复用 | 一套代码双端 |
| 体验/性能 | 最佳 | 最佳 | Flutter≈原生；RN≈桥接 |
| 学习曲线 | 中（声明式） | 中（声明式） | 低-中 |
| 适用 | iOS 重体验 | Android 重体验 | 双端 MVP / 业务型 |

---

## 2. iOS 开发从 0 到上架

### 前置准备
- [ ] **Mac 电脑**（必需，Apple Silicon 推荐）
- [ ] **Apple Developer Program**：$99/年（https://developer.apple.com/programs/）

### 开发环境
- [ ] **Xcode**（Mac App Store，含 iOS SDK 与模拟器）
- [ ] 包管理：Swift Package Manager（官方首选）/ CocoaPods（旧项目）

### 真机调试
- [ ] 开发证书（Development Certificate）
- [ ] App ID + Provisioning Profile（绑定 Bundle ID）
- [ ] 设备 UDID 注册（免费账号限 3 台/周，付费不限）
- [ ] Xcode → Signing & Capabilities 自动管理签名

### 上架
- [ ] App Store Connect 建 App 记录
- [ ] 必备：1024 图标、截图、隐私政策 URL
- [ ] **隐私清单 PrivacyInfo.xcprivacy**（2024 春起强制）
- [ ] **ATT**（App Tracking Transparency）：广告标识必须弹窗
- [ ] 审核周期：通常 24-48 小时，复杂 3-7 天

文档：https://developer.apple.com/app-store/submissions/

---

## 3. Android 开发从 0 到上架

### 前置准备
- [ ] 任意 OS（Win/Mac/Linux）
- [ ] **Google Play 账号**：$25 一次性（https://play.google.com/console）

### 开发环境
- [ ] **Android Studio**（含 SDK、Gradle、ADB、模拟器）
- [ ] JDK 17+（Studio 内置）

### 真机调试
- [ ] 「设置 → 关于手机 → 连续点击版本号」开启开发者模式
- [ ] 「开发者选项 → USB 调试」
- [ ] 发布 keystore：`keytool -genkey`
- [ ] build.gradle 配置 signingConfigs

### 上架（Google Play）
- [ ] 上传 **AAB**（2021 起强制，非 APK）
- [ ] 内容分级问卷、目标受众、隐私政策、数据安全表
- [ ] 内测/封闭/公开分轨道发布
- [ ] 审核通常 1-3 天

### 上架（国内商店）
- 华为 AppGallery、小米、OPPO、vivo、腾讯应用宝
- 各需独立账号 + **软件著作权（软著）** + 部分需企业资质
- 审核通常 2-5 天

---

## 4. 跨端框架选型（2024-2026）

| 框架 | 语言 | 何时选 | 备注 |
|------|------|------|------|
| **React Native (Expo)** | JS/TS | React 团队、快速 MVP、需热更 | EAS 简化构建上架 |
| **Flutter** | Dart | 重 UI 一致性、动画密集、设计驱动 | 单引擎渲染，接近原生 |
| **.NET MAUI** | C# | 企业内部、Xamarin 迁移 | 生态较小，适合 .NET 团队 |
| **Kotlin Multiplatform** | Kotlin | 共享业务逻辑、UI 走原生 | 体验最佳，适合长期演进 |

文档：
- Expo：https://docs.expo.dev
- Flutter：https://flutter.dev
- MAUI：https://learn.microsoft.com/maui
- KMP：https://kotlinlang.org/lp/multiplatform

---

## 5. 关键坑

### iOS 审核被拒 Top 原因
- 崩溃/Bug
- 坏链接、占位内容
- 隐私清单缺失
- ATT 未弹窗
- 未走 IAP 内购
- 未成年人保护
- 诱导评分

### Android 碎片化
- 覆盖 Android 8+ 可达约 95% 设备
- 国产 ROM（EMUI/MIUI/ColorOS）权限策略差异大

### 热更新
- **iOS 禁止**动态下发可执行代码（JSPatch 已封）
- 仅允许 OTA 静态资源，需符合 App Review Guideline 4.7
- RN CodePush 在 iOS 受限

### 包体优化
- R8/ProGuard 混淆
- 只打 `arm64-v8a`（覆盖约 95%）
- Flutter 用 `--split-per-abi`
- 图标转 WebP
- 动态特性模块（Dynamic Feature）

---

## 6. 后端与云服务

| 服务 | 定位 | 适合 |
|------|------|------|
| **Firebase** | Google 全家桶（Firestore/Auth/Functions/推送） | 海外、实时应用 |
| **Supabase** | 开源 Postgres BaaS | 通用、低锁定 |
| **AWS Amplify** | AWS 生态 | 企业级 |
| **腾讯云开发** | 国内一体化 | 国内合规 |
| **Sentry/Firebase Crashlytics** | 崩溃收集 | 必备 |

---

## 7. 成本与时间估算

| 项目 | 单端 MVP（原生） | 跨端 MVP（RN/Flutter） |
|------|------|------|
| 人天（1 人） | 20-40 天 | 30-50 天（含双端调优） |
| 年费 | iOS $99 或 Android $25 | 两个商店均需付费账号 |
| 审核周期 | iOS 1-2 天，Android 1-3 天 | 各端独立审核 |
| 后期迭代 | 双端各一份代码 | 单份代码维护 |

---

## 官方文档速查
- Apple Developer：https://developer.apple.com/
- App Store 提交：https://developer.apple.com/app-store/submissions/
- Google Play Console：https://play.google.com/console
- Android 开发：https://developer.android.com/
- Expo：https://docs.expo.dev
- Flutter：https://flutter.dev
