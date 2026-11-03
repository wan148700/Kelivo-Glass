#!/usr/bin/env python3
"""Apply the Android packaging configuration used for Kelivo Glass13.3."""
from pathlib import Path


def configure(root):
    gradle = root / 'android/app/build.gradle.kts'
    text = gradle.read_text()
    assert 'applicationId = "com.psyche.kelivo"' in text or 'applicationId = "com.psyche.kelivo.ashglass"' in text
    text = text.replace('applicationId = "com.psyche.kelivo"', 'applicationId = "com.psyche.kelivo.ashglass"')
    text = text.replace('ndkVersion = "28.2.13676358"', 'ndkVersion = "29.0.14206865"')
    marker = 'getByName("release") {'
    rules = 'proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")'
    assert marker in text
    if rules not in text:
        text = text.replace(marker, marker + '\n            ' + rules, 1)
    gradle.write_text(text)
    proguard = root / 'android/app/proguard-rules.pro'
    keep = '\n# JNI looks up coroutine descriptors by their original binary names.\n-keep class kotlin.coroutines.** { *; }\n-keep class kotlin.Unit { *; }\n-keep class kotlin.Result { *; }\n-keep class kotlin.Result$Failure { *; }\n-keep,includedescriptorclasses class io.flutter.plugins.sharedpreferences.** { *; }\n'
    text = proguard.read_text()
    if keep not in text:
        proguard.write_text(text + keep)
    manifest = root / 'android/app/src/main/AndroidManifest.xml'
    manifest.write_text(manifest.read_text().replace('android:label="Kelivo"', 'android:label="Kelivo Glass"'))


if __name__ == '__main__':
    configure(Path(__file__).resolve().parents[1])
    print('Configured Kelivo Glass Android identity, NDK and JNI retention rules.')
