import SwiftUI

/// Small value+label stat block (QFrame#statCard). Ported from
/// prototype/ui/widgets/stat_card.py. Used in a row of two on Dashboard
/// (Unlocks / Notifications).
struct StatCard: View {
    let label: String
    let value: String

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(value)
                .font(.system(size: 20, weight: .bold))
                .foregroundStyle(Theme.textPrimary)
            Text(label)
                .font(.system(size: 12))
                .foregroundStyle(Theme.textMuted)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(12)
        .background(RoundedRectangle(cornerRadius: 10).fill(Theme.surface))
    }
}
