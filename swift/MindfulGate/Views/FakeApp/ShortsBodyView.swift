import SwiftUI

struct ShortsBodyView: View {
    let appName: String

    private static let imageOffsets: [String: Int] = ["TikTok": 0, "YouTube": 3]

    private var imageIndex: Int {
        MockData.mockImageIndex(for: appName, offset: Self.imageOffsets[appName] ?? 0)
    }

    private var handle: String {
        let cleaned = appName.lowercased()
            .replacingOccurrences(of: " ", with: "")
            .replacingOccurrences(of: "(", with: "")
            .replacingOccurrences(of: ")", with: "")
        return "@\(cleaned)_demo"
    }

    var body: some View {
        ZStack {
            GeometryReader { proxy in
                Group {
                    if MockData.mockImages.indices.contains(imageIndex) {
                        Image(MockData.mockImages[imageIndex])
                            .resizable()
                            .aspectRatio(contentMode: .fill)
                            .frame(width: proxy.size.width, height: proxy.size.height)
                            .clipped()
                    } else {
                        Color.black
                    }
                }
            }

            VStack(spacing: 0) {
                Spacer()
                ZStack(alignment: .bottomTrailing) {
                    VStack(alignment: .leading, spacing: 4) {
                        Text(handle)
                            .font(.system(size: 13, weight: .bold))
                            .foregroundStyle(.white)
                        Text(MockData.mockShortsCaption)
                            .font(.system(size: 12))
                            .foregroundStyle(Color(hex: "#e8e8e8"))
                    }
                    .padding(EdgeInsets(top: 10, leading: 16, bottom: 16, trailing: 60))
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .background(Color.black.opacity(0.55))

                    VStack(spacing: 14) {
                        engageIcon("♥", "24.5K")
                        engageIcon("💬", "312")
                        engageIcon("↗", "1.2K")
                    }
                    .padding(EdgeInsets(top: 8, leading: 8, bottom: 16, trailing: 12))
                }
            }
        }
        .background(Color.black)
    }

    private func engageIcon(_ glyph: String, _ count: String) -> some View {
        VStack(spacing: 2) {
            Text(glyph).font(.system(size: 22)).foregroundStyle(.white)
            Text(count).font(.system(size: 10, weight: .semibold)).foregroundStyle(Color(hex: "#d8d8d8"))
        }
    }
}
