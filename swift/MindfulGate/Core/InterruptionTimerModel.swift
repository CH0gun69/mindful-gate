import Foundation

final class InterruptionTimerModel: ObservableObject {
    @Published private(set) var secondsLeft: Int = 0
    @Published private(set) var isContinueEnabled = false
    @Published private(set) var showReaffirm = false
    @Published private(set) var isBreathing = false

    private var levelConfig = MockData.protectionLevels[1]!
    private var unlockTimer: Timer?
    private var countdownTimer: Timer?

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
            showReaffirm = true
        } else {
            isContinueEnabled = true
        }
    }

    func reaffirmTapped() {
        showReaffirm = false
        isContinueEnabled = true
    }

    func stopTimers() {
        unlockTimer?.invalidate()
        unlockTimer = nil
        countdownTimer?.invalidate()
        countdownTimer = nil
    }
}
