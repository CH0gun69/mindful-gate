// swift-tools-version: 5.9
import PackageDescription
import AppleProductTypes

let package = Package(
    name: "MindfulGate",
    defaultLocalization: "en",
    platforms: [.iOS("17.0")],
    products: [
        .iOSApplication(
            name: "MindfulGate",
            targets: ["AppModule"],
            bundleIdentifier: "com.mindfulgate.MindfulGate",
            teamIdentifier: nil,
            displayVersion: "1.0",
            bundleVersion: "1",
            appIcon: .asset("AppIcon"),
            accentColor: .asset("AccentColor"),
            supportedDeviceFamilies: [.pad, .phone],
            supportedInterfaceOrientations: [
                .portrait,
                .landscapeRight,
                .landscapeLeft,
                .portraitUpsideDown(.when(deviceFamilies: [.pad]))
            ]
        )
    ],
    targets: [
        .executableTarget(name: "AppModule")
    ]
)
