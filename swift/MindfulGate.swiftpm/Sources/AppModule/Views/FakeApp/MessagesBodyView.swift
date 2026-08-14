import SwiftUI

struct MessagesBodyView: View {
    var body: some View {
        HStack(spacing: 0) {
            contactsSidebar
            chatView
        }
    }

    private var contactsSidebar: some View {
        VStack(spacing: 4) {
            ForEach(Array(MockData.mockContacts.enumerated()), id: \.offset) { index, contact in
                VStack(alignment: .leading, spacing: 2) {
                    Text(contact.name)
                        .font(.system(size: 12, weight: .semibold))
                        .foregroundStyle(Theme.textPrimary)
                    Text(contact.preview)
                        .font(.system(size: 11))
                        .foregroundStyle(Color(hex: "#8a8f98"))
                }
                .padding(EdgeInsets(top: 6, leading: 8, bottom: 6, trailing: 8))
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(
                    RoundedRectangle(cornerRadius: 8)
                        .fill(index == 0 ? Color(hex: "#23272f") : Color.clear)
                )
            }
            Spacer()
        }
        .padding(EdgeInsets(top: 10, leading: 6, bottom: 10, trailing: 6))
        .frame(width: 128)
        .background(Color(hex: "#17181a"))
        .overlay(alignment: .trailing) {
            Rectangle().fill(Color(hex: "#26282c")).frame(width: 1)
        }
    }

    private var chatView: some View {
        ScrollView {
            VStack(spacing: 8) {
                ForEach(Array(MockData.mockChat.enumerated()), id: \.offset) { _, message in
                    ChatBubbleRow(sender: message.sender, text: message.text)
                }
            }
            .padding(12)
        }
        .background(Theme.background)
    }
}

struct ChatBubbleRow: View {
    let sender: String
    let text: String

    private var isMe: Bool { sender == "me" }

    var body: some View {
        HStack {
            if isMe { Spacer(minLength: 40) }
            Text(text)
                .font(.system(size: 13))
                .foregroundStyle(isMe ? Theme.tealOnColorText : Theme.textPrimary)
                .padding(EdgeInsets(top: 8, leading: 12, bottom: 8, trailing: 12))
                .background(RoundedRectangle(cornerRadius: 14).fill(isMe ? Theme.teal : Color(hex: "#2a2d33")))
                .frame(maxWidth: 170, alignment: isMe ? .trailing : .leading)
            if !isMe { Spacer(minLength: 40) }
        }
    }
}
