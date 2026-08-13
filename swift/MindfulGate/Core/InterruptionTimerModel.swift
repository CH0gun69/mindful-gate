import Foundation

/// Owns the Interruption screen's level-driven gating logic: a delay timer
/// that keeps Continue Anyway disabled, a 1Hz countdown for its label text,
/// and (level 3 only) a reaffirm-tap requirement after the delay elapses.
/// Ported from prototype/ui/interruption.py's timer handling -- only
/// Continue Anyway is ever gated, Go Back is always immediately clickable.
final class InterruptionTimerModel: ObservableObject {
    @Published private(set) var secondsLeft: Int = 0
    @Published private(set) var isContinueEnabled = false
    @Published private(set) var showReaffirm = false
    @Published private(set) var isBreathing = false

    private var levelConfig = MockData.protectionLevels[1]!
    private var unlockTimer: Timer?
    private var countdownTimer: Timer?

    /// Full reset + (re)start for a given protection level, mirroring
    /// set_context()'s "this instance is reused across every trigger, so
    /// nothing from a previous app/level may survive" contract.
    func setContext(level: Int) {
        stopTimers()
        levelConfig = MockData.protectionLevels[level] ?? MockData.protectionLevels[1]!
        isContinueEnabled = false
        showReaffirm = false
        secondsLeft = levelConfig.delay
        isBreathing = levelConfig.breathing

        unlockTimer = Timer.scheduledTimer(withTimeInterval: Double(levelConfig.delay), repeats: false) { [weak self] _ in
            DispatchQueue.main.async { self?.onDelayElapsed() }
        }
        countdownTimer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { [weak self] _ in
            DispatchQueue.main.async { self?.tickCountdown() }
        }
    }

    private func tickCountdown() {
        secondsLeft = max(secondsLeft - 1, 0)
        if secondsLeft <= 0 {
            countdownTimer?.invalidate()
            countdownTimer = nil
        }
    }

    private func onDelayElapsed() {
        isBreathing = false
        countdownTimer?.invalidate()
        countdownTimer = nil
        if levelConfig.reaffirm {
            // Delay's over but still gated -- drop the stale "(0s)" suffix
            // rather than leave a countdown next to a button that isn't
            // actually about to unlock on its own.
            showReaffirm = true
        } else {
            isContinueEnabled = true
        }
    }

    func reaffirmTapped() {
        showReaffirm = false
        isContinueEnabled = true
    }

    /// Defensive stop for when the screen is navigated away from
    /// mid-countdown -- called from the view's onDisappear.
    func stopTimers() {
        unlockTimer?.invalidate()
        unlockTimer = nil
        countdownTimer?.invalidate()
        countdownTimer = nil
    }
}
