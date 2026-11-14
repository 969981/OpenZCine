# OpenZCine localization (Simplified / Traditional Chinese)

This is the first localization pass on `feat/zh-hans-zh-hant-localization`. It does not
modify the Nikon camera wire protocol, transport enum identifiers, stored pairing
records, or the separately versioned OpenCine dependency.

## Language picker

Open **Operator Setup → System → Language**. Choose **Follow System**, **English**,
**简体中文** or **繁體中文**.

- Android: `AppLanguagePreferences` persists the selected BCP-47 language tag in
  private SharedPreferences. `MainActivity.attachBaseContext` applies its locale
  before view creation. Selecting another language recreates only the Activity.
- Apple: `@AppStorage("openzcine.appLanguage")` persists the selection and
  injects the new SwiftUI `Locale` into `NativeAppRoot` without a relaunch.
  Apple system permission dialogs use the **device's** language instead.

The default `system` choice follows system changes; English is also available
explicitly. Both variants preserve English fallback for untranslated strings.

## Resources

| Platform | Simplified | Traditional |
| --- | --- | --- |
| Android | `Apps/Android/app/src/main/res/values-b+zh+Hans/strings.xml` | `values-b+zh+Hant/strings.xml` |
| iPhone / iPad | `ios/Runner/zh-Hans.lproj/Localizable.strings` | `ios/Runner/zh-Hant.lproj/Localizable.strings` |
| Apple permission prompts | `zh-Hans.lproj/InfoPlist.strings` | `zh-Hant.lproj/InfoPlist.strings` |

The first pass covers the language picker, common buttons, much of pairing,
camera transport, monitoring controls, local operator settings, and support and
legal links. **This is not yet a fully translated app**: OpenCine shared
presentation components and other unconverted source literals may remain
English. A later pass should expand extraction and provide localization
resources for the pinned shared UI package rather than changing protocol
identifiers or pretending unsupported strings are translated.

## Development checks

Run `python3 scripts/check-localizations.py` to parse resources, catch
duplicates, validate required keys and formatting placeholders, and check Xcode
localization registration.

For visual checks, test a small phone in portrait and landscape, switch
languages while the System tab is open, restart the app, choose Follow System,
and verify that saved camera profiles, recorded assets, and display layouts
remain unchanged. Also check permission prompts in the device language.

Debug-signed Android APKs and unsigned simulator builds are for development.
They do not replace the original developer's signed Store / TestFlight builds.
