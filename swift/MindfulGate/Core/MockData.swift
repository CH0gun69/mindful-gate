import Foundation

/// Hardcoded mock data for the mindful-gate app. No real usage tracking --
/// purely for demo purposes. Ported 1:1 from prototype/core/mock_data.py.
enum MockData {

    // MARK: - Top-level scalars

    static let screenTimeToday = "4h 32m"
    static let unlocksToday = 87
    static let notificationsToday = 143

    struct TopApp {
        let name: String
        let time: String
        let protected: Bool
    }

    static let topApps: [TopApp] = [
        TopApp(name: "Instagram", time: "1h 48m", protected: true),
        TopApp(name: "YouTube", time: "1h 05m", protected: false),
        TopApp(name: "TikTok", time: "52m", protected: true),
        TopApp(name: "Messages", time: "31m", protected: false),
        TopApp(name: "X (Twitter)", time: "16m", protected: true),
    ]

    static let protectableApps = ["Instagram", "TikTok", "X (Twitter)", "YouTube", "Facebook", "Reddit"]

    /// Which of protectableApps start out checked/protected before the user has
    /// ever visited Set Your Intention -- single source of truth shared by that
    /// screen's toggle defaults and PhoneHome's initial interrupt behavior.
    static let defaultProtectedApps: Set<String> = ["Instagram", "TikTok", "X (Twitter)"]

    /// Per-app protection level (1/2/3) before the user has ever visited Set
    /// Your Intention -- level 1 (mildest) for every protectable app.
    static let defaultAppProtectionLevels: [String: Int] =
        Dictionary(uniqueKeysWithValues: protectableApps.map { ($0, 1) })

    /// Behavior per interruption level. "delay" is seconds Continue Anyway stays
    /// disabled before it can unlock, "breathing" shows the BreathingCircle,
    /// "reaffirm" means the delay elapsing does NOT auto-unlock Continue Anyway
    /// -- the user must additionally tap the "Still on purpose?" chip.
    struct ProtectionLevel {
        let delay: Int
        let breathing: Bool
        let reaffirm: Bool
    }

    static let protectionLevels: [Int: ProtectionLevel] = [
        1: ProtectionLevel(delay: 3, breathing: false, reaffirm: false),
        2: ProtectionLevel(delay: 7, breathing: true, reaffirm: false),
        3: ProtectionLevel(delay: 12, breathing: true, reaffirm: true),
    ]

    /// Full breathe-in+breathe-out cycle duration (ms) for the pulsing circle
    /// shown during levels 2/3 (see Widgets/BreathingCircle.swift).
    static let breathingCycleMs = 2500

    static let defaultIntention = "Only reply to messages"

    /// Decorative glyph + accent color per app. Purely presentational -- apps
    /// not listed here fall back to an initial-letter avatar.
    static let appGlyphs: [String: (glyph: String, color: String)] = [
        "Instagram": ("📸", "#c44d75"),
        "TikTok": ("🎵", "#111214"),
        "X (Twitter)": ("𝕏", "#1f2024"),
        "YouTube": ("▶", "#d62929"),
        "Messages": ("💬", "#4caf65"),
        "Facebook": ("📘", "#3b7ccf"),
        "Reddit": ("👽", "#d65829"),
    ]

    static func glyph(for name: String) -> (glyph: String, color: String) {
        appGlyphs[name] ?? (String(name.prefix(1)).uppercased(), "#3a3f47")
    }

    /// Real brand-logo asset names (Assets.xcassets/Brand/) for apps that have
    /// one. "Messages" is a fictional stand-in app with no real-world brand, so
    /// it's intentionally absent and keeps falling back to its emoji avatar.
    static let appIconAssetNames: [String: String] = [
        "Instagram": "instagram",
        "TikTok": "tiktok",
        "X (Twitter)": "x",
        "YouTube": "youtube",
        "Facebook": "facebook",
        "Reddit": "reddit",
    ]

    static func iconAssetName(for name: String) -> String? {
        appIconAssetNames[name]
    }

    // MARK: - Time helpers

    /// Parses a mock "Xh Ym" / "Ym" time string (as used in topApps) into total minutes.
    static func parseMinutes(_ timeStr: String) -> Int {
        var hours = 0
        var minutes = 0
        for part in timeStr.split(separator: " ") {
            if part.hasSuffix("h") {
                hours = Int(part.dropLast()) ?? 0
            } else if part.hasSuffix("m") {
                minutes = Int(part.dropLast()) ?? 0
            }
        }
        return hours * 60 + minutes
    }

    /// Inverse of parseMinutes -- total minutes back into the same "Xh Ym" / "Ym" format.
    static func formatMinutes(_ totalMinutes: Int) -> String {
        let hours = totalMinutes / 60
        let minutes = totalMinutes % 60
        if hours > 0 && minutes > 0 {
            return String(format: "%dh %02dm", hours, minutes)
        }
        if hours > 0 {
            return "\(hours)h"
        }
        return "\(minutes)m"
    }

    // MARK: - Shuffle mechanism (session-only, in-memory, never mutates topApps)

    static let shuffleRangeMinutes = 5...180

    private static var shuffledTimes: [String: String]?

    /// Randomizes every topApps app's mock "time spent today" in memory only.
    /// Never touches topApps -- callers just re-render usageBreakdown()/
    /// timeSpentTodayFor()/currentScreenTimeToday() afterward.
    static func shuffleTopApps() {
        var result: [String: String] = [:]
        for app in topApps {
            result[app.name] = formatMinutes(Int.random(in: shuffleRangeMinutes))
        }
        shuffledTimes = result
    }

    /// Back to the real topApps values -- explicit inverse of shuffleTopApps().
    static func resetTopAppsShuffle() {
        shuffledTimes = nil
    }

    private static func timeFor(_ app: TopApp) -> String {
        if let shuffled = shuffledTimes, let overridden = shuffled[app.name] {
            return overridden
        }
        return app.time
    }

    /// This app's current "Xh Ym" time (shuffled if active, else its real topApps
    /// entry), or nil if it has no mock usage entry at all.
    static func timeSpentTodayFor(_ name: String) -> String? {
        guard let app = topApps.first(where: { $0.name == name }) else { return nil }
        return timeFor(app)
    }

    struct UsageEntry {
        let name: String
        let minutes: Int
        let timeString: String
        let color: String
    }

    /// Derived live from topApps for the screen-time ring chart + legend --
    /// deliberately not a separate hardcoded dataset, so it can't drift out of sync.
    static func usageBreakdown() -> [UsageEntry] {
        topApps.map { app in
            let timeString = timeFor(app)
            return UsageEntry(
                name: app.name,
                minutes: parseMinutes(timeString),
                timeString: timeString,
                color: glyph(for: app.name).color
            )
        }
    }

    /// The big screen-time total shown on Phone Home/Dashboard.
    static func currentScreenTimeToday() -> String {
        guard shuffledTimes != nil else { return screenTimeToday }
        let total = topApps.reduce(0) { $0 + parseMinutes(timeFor($1)) }
        return formatMinutes(total)
    }

    // MARK: - Ambient usage tint (2-state; no numeric score, never red)

    static let ambientThresholdMinutes = 240
    static let ambientColorNormal = "#93cfc4"
    static let ambientColorHigh = "#d9a974"

    static func isHighUsage() -> Bool {
        parseMinutes(currentScreenTimeToday()) >= ambientThresholdMinutes
    }

    static func usageColor(isHigh: Bool) -> String {
        isHigh ? ambientColorHigh : ambientColorNormal
    }

    // MARK: - Fake App mock content

    /// Local CC0 placeholder photo asset names (Assets.xcassets/MockPhotos/).
    static let mockImages = [
        "lake_forest", "waterfall", "flower_field", "cat_closeup",
        "yellow_flower", "foggy_road", "hay_bales", "foggy_trees",
        "sunset_field", "bare_tree",
    ]

    /// Deterministic pseudo-random index into mockImages, seeded by an app/screen
    /// name -- same app always shows the same picture across a run. offset lets
    /// one screen request several different images off the same name.
    static func mockImageIndex(for name: String, offset: Int = 0) -> Int {
        let weighted = name.enumerated().reduce(0) { total, pair in
            let (i, c) = pair
            let codePoint = Int(c.unicodeScalars.first?.value ?? 0)
            return total + (i + 1) * codePoint
        }
        let count = mockImages.count
        return ((weighted + offset) % count + count) % count
    }

    /// (username, caption) pairs shared by every "feed"-style app.
    static let mockFeedPosts: [(username: String, caption: String)] = [
        ("wanderlust.jane", "chasing golden hour again 🌅"),
        ("dev.marcus", "small wins today, one commit at a time"),
        ("plant.mama", "she's finally blooming 🌸"),
    ]

    static let mockShortsCaption = "wait for it... 😅"

    struct FeedActionButton {
        let id: String
        let icon: String
        let label: String?
        let flash: String
    }

    enum FeedLayout {
        case icons(small: Bool)
        case labeled
        case vote(voteCount: String, commentCount: String, upvoteFlash: String, downvoteFlash: String)
    }

    struct FeedActionsConfig {
        let layout: FeedLayout
        let buttons: [FeedActionButton]
    }

    /// Per-app action-button config for the "feed" style, so each app is
    /// recognizable by its button personality, not just its accent color.
    static let feedActions: [String: FeedActionsConfig] = [
        "Instagram": FeedActionsConfig(layout: .icons(small: false), buttons: [
            FeedActionButton(id: "like", icon: "♡", label: nil, flash: "#ff3b5c"),
            FeedActionButton(id: "comment", icon: "💬", label: nil, flash: "#8fd3c7"),
            FeedActionButton(id: "share", icon: "➤", label: nil, flash: "#8fd3c7"),
            FeedActionButton(id: "save", icon: "🔖", label: nil, flash: "#8fd3c7"),
        ]),
        "Facebook": FeedActionsConfig(layout: .labeled, buttons: [
            FeedActionButton(id: "like", icon: "👍", label: "Like", flash: "#1877f2"),
            FeedActionButton(id: "comment", icon: "💬", label: "Comment", flash: "#1877f2"),
            FeedActionButton(id: "share", icon: "↗", label: "Share", flash: "#1877f2"),
        ]),
        "X (Twitter)": FeedActionsConfig(layout: .icons(small: true), buttons: [
            FeedActionButton(id: "reply", icon: "💬", label: nil, flash: "#1d9bf0"),
            FeedActionButton(id: "retweet", icon: "↻", label: nil, flash: "#00ba7c"),
            FeedActionButton(id: "like", icon: "♡", label: nil, flash: "#f91880"),
            FeedActionButton(id: "share", icon: "↗", label: nil, flash: "#1d9bf0"),
        ]),
        "Reddit": FeedActionsConfig(
            layout: .vote(voteCount: "1.2K", commentCount: "84 comments", upvoteFlash: "#ff4500", downvoteFlash: "#7193ff"),
            buttons: []
        ),
    ]

    /// Falls back to Instagram's icon row for any app that isn't explicitly configured.
    static func feedActionsFor(_ name: String) -> FeedActionsConfig {
        feedActions[name] ?? feedActions["Instagram"]!
    }

    /// Fictional contacts for the "messages" style -- invented generic names.
    static let mockContacts: [(name: String, preview: String)] = [
        ("Jamie Chen", "Good to hear 🙂"),
        ("Jordan Lee", "See you at 6?"),
        ("Sam Park", "Sent the files 📎"),
        ("Taylor Kim", "Haha exactly 😂"),
    ]

    /// (sender, text) pairs for the messages style's chat view, with Jamie Chen.
    /// sender is "me" (the app's user) or "them" (Jamie).
    static let mockChat: [(sender: String, text: String)] = [
        ("them", "Hey Alex! How's it going?"),
        ("me", "It's going well, thanks!"),
        ("them", "Good to hear 🙂"),
    ]

    /// Which visual style each real app uses on the Fake App screen.
    static let appStyle: [String: String] = [
        "Instagram": "feed",
        "Facebook": "feed",
        "X (Twitter)": "feed",
        "Reddit": "feed",
        "TikTok": "shorts",
        "YouTube": "shorts",
        "Messages": "messages",
    ]

    /// Defaults to "feed" for anything unlisted, since that's the most generic/reusable of the three.
    static func styleFor(_ name: String) -> String {
        appStyle[name] ?? "feed"
    }
}
