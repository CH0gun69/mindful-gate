import SwiftUI

/// A simple donut/ring chart: each segment gets an arc proportional to its
/// share of the total. Not pixel-perfect -- a handful of solid-color arced
/// segments is enough for this prototype. Ported from
/// prototype/ui/widgets/usage_ring_chart.py.
///
/// Segments are drawn starting from 12 o'clock, clockwise, in the order
/// given. Individual segment fill colors always come from `segments` and are
/// never touched by `borderColor` -- that only affects the shared
/// outline/overall tone (Dashboard overrides it for its ambient tint).
struct UsageRingChart: View {
    struct Segment {
        let name: String
        let minutes: Int
        let color: String
    }

    var segments: [Segment]
    var diameter: CGFloat = 112
    var borderColor: String = "#3a3f47"

    private static let ringThickness: CGFloat = 16
    private static let gapDegrees: Double = 3

    private var total: Int { segments.reduce(0) { $0 + $1.minutes } }

    var body: some View {
        Canvas { context, size in
            guard total > 0 else { return }
            let thickness = Self.ringThickness
            let radius = min(size.width, size.height) / 2 - thickness / 2 - 1
            let center = CGPoint(x: size.width / 2, y: size.height / 2)

            // Qt's convention: 0deg = 3 o'clock, positive = counter-clockwise.
            // Start at 12 o'clock (90deg) and step clockwise (subtracting) --
            // reproduced here using SwiftUI's clockwise Angle(degrees:) from
            // the same 12-o'clock reference (-90deg in standard screen coords,
            // since y grows downward).
            var startDegrees = -90.0
            for segment in segments {
                let span = (Double(segment.minutes) / Double(total)) * 360
                let drawnSpan = max(span - Self.gapDegrees, 0)

                var path = Path()
                path.addArc(
                    center: center,
                    radius: radius,
                    startAngle: .degrees(startDegrees),
                    endAngle: .degrees(startDegrees + drawnSpan),
                    clockwise: false
                )
                context.stroke(
                    path,
                    with: .color(Color(hex: segment.color)),
                    style: StrokeStyle(lineWidth: thickness, lineCap: .butt)
                )
                context.stroke(
                    path,
                    with: .color(Color(hex: borderColor)),
                    style: StrokeStyle(lineWidth: 1)
                )

                startDegrees += span
            }
        }
        .frame(width: diameter, height: diameter)
    }
}
