// swift-tools-version: 5.9
import PackageDescription
import AppleProductTypes

let package = Package(
    name: "MindfulGate",
    defaultLocalization: "en",
    platforms: [.iOS("17.0")],
    dependencies: [
        // Add AppleProductTypes package to provide .iOSApplication and related helpers
        .package(url: "https://github.com/apple/swift-apple-product-types", branch: "main"),
    ],
    products: [
        .iOSApplication(
            name: "MindfulGate",
            targets: ["AppModule"],
            bundleIdentifier: "com.mindfulgate.MindfulGate",
            displayVersion: "1.0",
            bundleVersion: "1",
            appIcon: .placeholder(icon: .leaf),
            accentColor: .presetColor(.teal),
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
        .executableTarget(
            name: "AppModule",
            dependencies: [.product(name: "AppleProductTypes", package: "swift-apple-product-types")]
        )
    ]
)
