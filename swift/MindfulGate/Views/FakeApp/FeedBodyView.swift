import SwiftUI

/// "feed" style: Instagram / Facebook / X (Twitter) / Reddit. Ported from
/// fake_app_screen.py's _build_feed_body. Same 3 MOCK_FEED_POSTS shared
/// across every feed app, just re-skinned per app's accent color and
/// per-app action-button config (icons/labeled/vote).
struct FeedBodyView: View {
    let appName: String
    let accentColor: Color

    var body: some View {
        ScrollView {
            VStack(spacing: 16) {
                ForEach(Array(MockData.mockFeedPosts.enumerated()), id: \.offset) { index, post in
                    FeedPostCardView(
                        username: post.username,
                        caption: post.caption,
                        accentColor: accentColor,
                        imageIndex: MockData.mockImageIndex(for: appName, offset: index),
                        actionsConfig: MockData.feedActionsFor(appName)
                    )
                }
            }
            .padding(16)
        }
    }
}

/// Dispatches to Reddit's genuinely-different vote-cluster layout, or the
/// shared header/photo/caption/actions card used by the other three apps.
struct FeedPostCardView: View {
    let username: String
    let caption: String
    let accentColor: Color
    let imageIndex: Int
    let actionsConfig: MockData.FeedActionsConfig

    var body: some View {
        if case .vote(let voteCount, let commentCount, let upvoteFlash, let downvoteFlash) = actionsConfig.layout {
            RedditPostCardView(
                username: username, caption: caption, accentColor: accentColor,
                imageIndex: imageIndex, voteCount: voteCount, commentCount: commentCount,
                upvoteFlash: upvoteFlash, downvoteFlash: downvoteFlash
            )
        } else {
            StandardFeedPostCardView(
                username: username, caption: caption, accentColor: accentColor,
                imageIndex: imageIndex, actionsConfig: actionsConfig
            )
        }
    }
}

struct StandardFeedPostCardView: View {
    let username: String
    let caption: String
    let accentColor: Color
    let imageIndex: Int
    let actionsConfig: MockData.FeedActionsConfig

    var body: some View {
        VStack(spacing: 0) {
            FeedPostHeader(username: username, accentColor: accentColor)
            FeedPostPhoto(imageIndex: imageIndex)
            FeedPostCaption(username: username, caption: caption)
            actionsRow
        }
        .background(Color(hex: "#1c1c1e"))
        .clipShape(RoundedRectangle(cornerRadius: 10))
    }

    @ViewBuilder
    private var actionsRow: some View {
        switch actionsConfig.layout {
        case .icons(let small):
            HStack(spacing: 0) {
                Spacer()
                ForEach(actionsConfig.buttons, id: \.id) { btn in
                    FeedActionButton(
                        icon: btn.icon,
                        style: small ? .icon(size: 28, fontSize: 15) : .icon(size: 34, fontSize: 20),
                        flashColor: Color(hex: btn.flash)
                    )
                    Spacer()
                }
            }
            .padding(.horizontal, 10)
            .padding(.top, 4)
            .padding(.bottom, 8)
        case .labeled:
            HStack(spacing: 0) {
                ForEach(Array(actionsConfig.buttons.enumerated()), id: \.offset) { index, btn in
                    if index > 0 {
                        Rectangle().fill(Color(hex: "#2a2a2c")).frame(width: 1)
                    }
                    FeedActionButton(icon: btn.icon, label: btn.label, style: .labeled, flashColor: Color(hex: btn.flash))
                }
            }
            .padding(.vertical, 2)
            .overlay(alignment: .top) {
                Rectangle().fill(Color(hex: "#2a2a2c")).frame(height: 1)
            }
        case .vote:
            EmptyView()  // handled by RedditPostCardView instead
        }
    }
}

/// Reddit's post shape: a vertical vote cluster on the left instead of a
/// bottom action row, with comment count shown separately below the
/// caption -- matches how Reddit's real layout actually differs, not just
/// its colors/icons.
struct RedditPostCardView: View {
    let username: String
    let caption: String
    let accentColor: Color
    let imageIndex: Int
    let voteCount: String
    let commentCount: String
    let upvoteFlash: String
    let downvoteFlash: String

    var body: some View {
        HStack(spacing: 0) {
            VStack(spacing: 2) {
                FeedActionButton(icon: "▲", style: .vote, flashColor: Color(hex: upvoteFlash), colorOnlyFlash: true)
                Text(voteCount)
                    .font(.system(size: 11, weight: .bold))
                    .foregroundStyle(Color(hex: "#d7dadc"))
                FeedActionButton(icon: "▼", style: .vote, flashColor: Color(hex: downvoteFlash), colorOnlyFlash: true)
            }
            .padding(EdgeInsets(top: 10, leading: 8, bottom: 10, trailing: 8))
            .background(Color(hex: "#161617"))

            VStack(spacing: 0) {
                FeedPostHeader(username: username, accentColor: accentColor)
                FeedPostPhoto(imageIndex: imageIndex)
                FeedPostCaption(username: username, caption: caption)
                HStack {
                    Text("💬  \(commentCount)")
                        .font(.system(size: 11))
                        .foregroundStyle(Color(hex: "#818384"))
                    Spacer()
                }
                .padding(EdgeInsets(top: 0, leading: 10, bottom: 8, trailing: 10))
            }
        }
        .background(Color(hex: "#1c1c1e"))
        .clipShape(RoundedRectangle(cornerRadius: 10))
    }
}

// MARK: - Shared header/photo/caption (used by both card shapes)

struct FeedPostHeader: View {
    let username: String
    let accentColor: Color

    var body: some View {
        HStack(spacing: 8) {
            Text(String(username.prefix(1)).uppercased())
                .font(.system(size: 12, weight: .semibold))
                .foregroundStyle(.white)
                .frame(width: 28, height: 28)
                .background(Circle().fill(accentColor))
            Text(username)
                .font(.system(size: 13, weight: .semibold))
                .foregroundStyle(Color(hex: "#f2f2f2"))
            Spacer()
        }
        .padding(EdgeInsets(top: 10, leading: 10, bottom: 8, trailing: 10))
    }
}

struct FeedPostPhoto: View {
    let imageIndex: Int

    var body: some View {
        Group {
            if MockData.mockImages.indices.contains(imageIndex) {
                Image(MockData.mockImages[imageIndex])
                    .resizable()
                    .aspectRatio(contentMode: .fill)
                    .frame(maxWidth: .infinity)
                    .frame(height: 160)
                    .clipped()
            } else {
                Color(hex: "#0d0d0d").frame(height: 160)
            }
        }
    }
}

struct FeedPostCaption: View {
    let username: String
    let caption: String

    var body: some View {
        Text("\(username) \(caption)")
            .font(.system(size: 12))
            .foregroundStyle(Color(hex: "#cfcfcf"))
            .padding(EdgeInsets(top: 8, leading: 10, bottom: 10, trailing: 10))
    }
}
