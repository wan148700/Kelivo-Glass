# Kelivo Glass · 非官方玻璃改版

基于 [Chevey339/Kelivo](https://github.com/Chevey339/kelivo) 的个人修改版。原项目版权归原作者及贡献者；不代表原作者发布、维护或背书。此仓库用于独立保存已签名 APK 和完整对应源码，不包含原私人仓库历史或其他项目。

当前版本：**1.3.2-glass.13.3 / code97**，Android ARM64，包名 `com.psyche.kelivo.ashglass`。

- [下载 APK](https://github.com/wan148700/Kelivo-Glass/releases/download/glass13.3/Kelivo-Glass-1.3.2-glass13.3-arm64.apk)
- [下载完整对应源码 ZIP](https://github.com/wan148700/Kelivo-Glass/releases/download/glass13.3/Kelivo-Glass-1.3.2-glass13.3-source.zip)
- [全部发布附件与校验信息](https://github.com/wan148700/Kelivo-Glass/releases/tag/glass13.3)

**源码请下载上面专门命名的 source.zip 附件。GitHub 自动生成的 Source code (zip/tar.gz) 只包含本仓库的说明文件，不是完整 Flutter 工程。** 完整附件含 Flutter 源码、锁文件、vendored 依赖、生成本地化、许可证与构建配置脚本；不需要访问其他私人仓库。

## 修改与使用

修改整理日期：2026-11-03。上游稳定版 1.3.2，commit `b1702b3a9ff35656c682a0818a9b44d8a8b72454`。本版包含可调玻璃界面、渠道/模型两行显示、工作流/QQ组件和可选自动云归档。自动云归档默认关闭，默认 500MB 或30天任一达到、可调整，使用现有 WebDAV 配置；真实云盘与设备效果仍需配置验证。首次测试 WebDAV 时需确认备份文件夹存在。

这是已验证版本的归档，没有重编译或混入尚未完成的新修复。295项相关测试、ARM64构建、Pigeon/Kotlin检查、维护证书v2/v3签名及原发布回下载验证通过；具体范围见 [VALIDATION_GLASS.md](VALIDATION_GLASS.md)。构建见 [BUILDING_GLASS.md](BUILDING_GLASS.md)。不同签名的自行构建包不能直接覆盖维护者签名包。

## 许可

继续采用 **[GNU AGPL-3.0](LICENSE)**。保留原有版权和第三方声明，分发修改版时提供对应源码并注明修改。各第三方组件的许可证和 NOTICE 保存在完整源码 ZIP 内。源码和APK不含用户聊天、API密钥、云盘密码或维护者私有签名密钥。安装包不提供额外担保。

自动 Actions 已关闭，此仓库不自动跟随上游更新。
