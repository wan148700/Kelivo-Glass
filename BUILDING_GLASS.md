先下载完整源码附件 `Kelivo-Glass-1.3.2-glass13.3-source.zip` 并解压，在解压后的 Flutter 工程根目录执行以下步骤。

# 构建 Kelivo Glass13.3

源码根目录保留完整 Flutter 工程、锁文件、生成本地化及 vendored 依赖。所需工具：Flutter **3.47.6** / Dart **3.13**，Java **17**，Android SDK 36，NDK **29.0.14206865**，Python3、curl、tar。其他平台的源代码保留，但本发布只验证 Android ARM64。

```sh
flutter pub get
flutter gen-l10n
python3 tools/configure_glass_android.py
flutter build apk --release --target-platform android-arm64 --build-name 1.3.2-glass.13.3 --build-number 97
python3 tools/check_preferences_dex.py build/app/outputs/flutter-apk/app-release.apk --require --preferences-api pigeon
```

配置脚本只应用原构建使用的 Android 包名、NDK、应用标签和 R8 JNI 保留规则，可重复执行。若资源不足，可在 `android/gradle.properties` 中按本机容量配置 Gradle JVM 内存；原构建使用 `-Xmx4g -XX:MaxMetaspaceSize=1g`。

`shared_preferences_android` 锁定 2.4.28，使用 Pigeon；校验时需明确传入 `--preferences-api pigeon`。代码/工作流修改后按 AGENTS.md 运行受影响检查。完整严格分析命令为 `dart analyze --fatal-infos lib test integration_test`，测试使用工程现有 `flutter test`。

本仓库不提供维护者私有 keystore 或密码。自行构建时请用自己的签名配置或 Android SDK apksigner 签名；不同签名无法直接覆盖维护者已签名版本。发布 APK 的证书 SHA256 为 `ba2526b2a225cdee1d657ebbb9a1489800b0837afa19be7856986fb92eb4f64f`。签名导致的字节差异属于正常现象，本说明不宣称可逐字节复现签名 APK。
