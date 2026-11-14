// Host-only YM2612 synthesis boundary. No ROM, CPU or game policy lives here.
// The independently licensed core is in ../third_party/ymfm (BSD-3-Clause).
#include <algorithm>
#include <cstdint>
#include <limits>
#include <new>
#include "ymfm_opn.h"

#ifdef _WIN32
#define AUDIO_EXPORT extern "C" __declspec(dllexport)
#else
#define AUDIO_EXPORT extern "C" __attribute__((visibility("default")))
#endif

namespace {
constexpr uint64_t disabled = std::numeric_limits<uint64_t>::max();
constexpr uint64_t sample_clocks = 144; // YM2612: 24 operators * prescale 6.

class Chip final : public ymfm::ymfm_interface {
public:
    explicit Chip(uint32_t clock) : clock_hz(clock), engine(*this) { engine.reset(); }

    void ymfm_set_timer(uint32_t timer, int32_t duration) override {
        if (timer < 2)
            timers[timer] = duration < 0 ? disabled : now + uint32_t(duration);
    }
    void ymfm_set_busy_end(uint32_t clocks) override { busy_end = now + clocks; }
    bool ymfm_is_busy() override { return now < busy_end; }
    void ymfm_update_irq(bool asserted) override { irq = asserted; }

    // Writes and status reads occur at the already-advanced external clock.
    // The core's mode-write/IRQ synchronization callbacks are synchronous here.
    uint64_t advance(uint64_t target, int16_t *stereo, uint64_t capacity) {
        uint64_t written = 0;
        while (now < target) {
            uint64_t next = std::min(target, std::min(next_sample,
                                      std::min(timers[0], timers[1])));
            now = next;
            // Explicit ordering at coincident boundaries: timer A, B, then PCM.
            for (uint32_t timer = 0; timer < 2; ++timer) {
                if (timers[timer] == now) {
                    timers[timer] = disabled;
                    m_engine->engine_timer_expired(timer);
                }
            }
            if (next_sample == now) {
                ymfm::ym2612::output_data sample;
                engine.generate(&sample, 1);
                sample.clamp16();
                if (written < capacity) {
                    stereo[2 * written] = int16_t(sample.data[0]);
                    stereo[2 * written + 1] = int16_t(sample.data[1]);
                }
                ++written;
                next_sample += sample_clocks;
            }
        }
        return written;
    }

    const uint32_t clock_hz;
    uint64_t now = 0, busy_end = 0, next_sample = sample_clocks;
    uint64_t timers[2] = { disabled, disabled };
    bool irq = false;
    ymfm::ym2612 engine;
};
}

AUDIO_EXPORT uint32_t g5510_ymfm_abi() { return 1; }
AUDIO_EXPORT void *g5510_ymfm_create(uint32_t clock_hz) noexcept {
    if (clock_hz < sample_clocks) return nullptr;
    try { return new Chip(clock_hz); } catch (...) { return nullptr; }
}
AUDIO_EXPORT void g5510_ymfm_destroy(void *opaque) noexcept {
    delete static_cast<Chip *>(opaque);
}
AUDIO_EXPORT uint64_t g5510_ymfm_clock(void *opaque) noexcept {
    return static_cast<Chip *>(opaque)->now;
}
AUDIO_EXPORT uint64_t g5510_ymfm_busy_end(void *opaque) noexcept {
    return static_cast<Chip *>(opaque)->busy_end;
}
AUDIO_EXPORT uint32_t g5510_ymfm_native_rate(void *opaque) noexcept {
    auto &chip = *static_cast<Chip *>(opaque);
    return chip.engine.sample_rate(chip.clock_hz);
}
AUDIO_EXPORT uint32_t g5510_ymfm_status(void *opaque) noexcept {
    return static_cast<Chip *>(opaque)->engine.read_status();
}
AUDIO_EXPORT uint32_t g5510_ymfm_irq(void *opaque) noexcept {
    return static_cast<Chip *>(opaque)->irq ? 1 : 0;
}
AUDIO_EXPORT int32_t g5510_ymfm_write(void *opaque, uint32_t port, uint32_t value) noexcept {
    if (!opaque || port > 3 || value > 255) return -1;
    static_cast<Chip *>(opaque)->engine.write(port, uint8_t(value));
    return 0;
}
AUDIO_EXPORT int64_t g5510_ymfm_advance(void *opaque, uint64_t target,
        int16_t *stereo, uint64_t capacity_frames) noexcept {
    if (!opaque) return -1;
    auto &chip = *static_cast<Chip *>(opaque);
    if (target < chip.now || target > disabled - sample_clocks) return -1;
    const uint64_t needed = target / sample_clocks - chip.now / sample_clocks;
    if (needed > capacity_frames || (needed && !stereo)) return -1;
    return int64_t(chip.advance(target, stereo, capacity_frames));
}
