import argparse
import struct
import zipfile


def symbols(data):
    def u32(offset):
        return struct.unpack_from('<I', data, offset)[0]

    def text(offset):
        while data[offset] & 128:
            offset += 1
        offset += 1
        return data[offset:data.index(b'\0', offset)].decode('utf-8', errors='replace')

    count, offset = u32(56), u32(60)
    strings = [text(u32(offset + i * 4)) for i in range(count)]
    count, offset = u32(64), u32(68)
    types = [strings[u32(offset + i * 4)] for i in range(count)]
    count, offset = u32(72), u32(76)
    protos = []
    for i in range(count):
        _, ret, params = struct.unpack_from('<III', data, offset + i * 12)
        args = [] if not params else struct.unpack_from('<' + 'H' * u32(params), data, params + 4)
        protos.append('(' + ''.join(types[a] for a in args) + ')' + types[ret])
    count, offset = u32(88), u32(92)
    method_ids = []
    for i in range(count):
        cls, proto, name = struct.unpack_from('<HHI', data, offset + i * 8)
        method_ids.append((types[cls], strings[name], protos[proto]))
    count, offset = u32(80), u32(84)
    fields = []
    for i in range(count):
        cls, type_id, name = struct.unpack_from('<HHI', data, offset + i * 8)
        fields.append((types[cls], strings[name], types[type_id]))
    count, offset = u32(96), u32(100)
    classes = {types[u32(offset + i * 32)] for i in range(count)}
    return classes, set(method_ids), set(fields)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('apk')
    parser.add_argument('--require', action='store_true')
    parser.add_argument('--preferences-api', choices=['jni', 'pigeon'], default='jni',
                        help='Expected API from the resolved, reviewed plugin source; never infer it from missing classes')
    args = parser.parse_args()
    classes, methods, fields = set(), set(), set()
    with zipfile.ZipFile(args.apk) as apk:
        for name in apk.namelist():
            if name.startswith('classes') and name.endswith('.dex'):
                c, m, f = symbols(apk.read(name))
                classes.update(c)
                methods.update(m)
                fields.update(f)
    required_classes = {
        'Lkotlin/Unit;', 'Lkotlin/Result;', 'Lkotlin/Result$Failure;',
        'Lkotlin/coroutines/Continuation;',
        'Lkotlin/coroutines/intrinsics/CoroutineSingletons;',
        'Lkotlin/coroutines/intrinsics/IntrinsicsKt;',
    }
    required_methods = {
        ('Lkotlin/coroutines/Continuation;', 'resumeWith', '(Ljava/lang/Object;)V'),
        ('Lkotlin/Result$Failure;', '<init>', '(Ljava/lang/Throwable;)V'),
    }
    required_fields = {
        ('Lkotlin/Result;', 'value', 'Ljava/lang/Object;'),
        ('Lkotlin/Result$Failure;', 'exception', 'Ljava/lang/Throwable;'),
        ('Lkotlin/Unit;', 'INSTANCE', 'Lkotlin/Unit;'),
    }
    if args.preferences_api == 'jni':
        required_classes.add('Lio/flutter/plugins/sharedpreferences/SharedPreferencesApiRegistrar;')
        required_methods.add(('Lio/flutter/plugins/sharedpreferences/SharedPreferencesApiRegistrar;', 'getAll', '(Ljava/lang/String;Ljava/util/List;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;'))
    else:
        # Reviewed shared_preferences_android 2.4.28 uses Pigeon, not the
        # 2.5.0 JNI registrar. Keep both actual read paths and their descriptors.
        required_classes.update({
            'Lio/flutter/plugins/sharedpreferences/SharedPreferencesPlugin;',
            'Lio/flutter/plugins/sharedpreferences/LegacySharedPreferencesPlugin;',
            'Lio/flutter/plugins/sharedpreferences/SharedPreferencesPigeonOptions;',
        })
        required_methods.update({
            ('Lio/flutter/plugins/sharedpreferences/LegacySharedPreferencesPlugin;', 'getAll', '(Ljava/lang/String;Ljava/util/List;)Ljava/util/Map;'),
            ('Lio/flutter/plugins/sharedpreferences/SharedPreferencesPlugin;', 'getAll', '(Ljava/util/List;Lio/flutter/plugins/sharedpreferences/SharedPreferencesPigeonOptions;)Ljava/util/Map;'),
        })
    missing = list(required_classes - classes) + list(required_methods - methods) + list(required_fields - fields)
    if not any(name == 'getCOROUTINE_SUSPENDED' and proto == '()Ljava/lang/Object;' and cls.startswith('Lkotlin/coroutines/intrinsics/IntrinsicsKt') for cls, name, proto in methods):
        missing.append('IntrinsicsKt.getCOROUTINE_SUSPENDED()Ljava/lang/Object;')
    print('Expected preferences API:', args.preferences_api)
    print('Missing JNI symbols:', sorted(map(str, missing)))
    if args.require and missing:
        raise SystemExit('Packaged JNI runtime contract is incomplete')
    print('Full Kotlin JNI runtime contract present:', not missing)


if __name__ == '__main__':
    main()
