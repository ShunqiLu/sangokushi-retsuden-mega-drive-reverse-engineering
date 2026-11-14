"""Finite explicit application tick over actual original audio source points.

This coordinates the existing semantic owners; it interprets no opcodes and
supplies no RAM, command, R value, timer flag, successful ACK or hidden time.
"""
from dataclasses import dataclass

from tools.high_level_audio_engine.domain import AudioBoundary
from tools.high_level_audio_engine.driver_startup import DriverStartupPoint,Im1ClockGrant
from .audio import OwnedGameAudio,AudioChipAdvance


SOURCE_POINTS={0x006F:'main-loop-boundary',0x0073:'mailbox-return',
    0x009B:'timerB-SFX-return',0x00A8:'timerA-update-return'}


@dataclass(frozen=True)
class AudioTickSpec:
    """All four caller supplies are required; None explicitly means no IM1."""
    fm_ticks: int
    psg_input_clocks: int
    im1_grant: Im1ClockGrant | None
    max_software_steps: int

    def validate(self):
        for name,maximum in (('fm_ticks',(1<<64)-145),('psg_input_clocks',(1<<63)-1)):
            value=getattr(self,name)
            if type(value)is not int or not 0<=value<=maximum:
                raise ValueError('explicit finite nonnegative '+name+' required')
        if type(self.max_software_steps)is not int or not 1<=self.max_software_steps<=65536:
            raise ValueError('explicit finite software-action limit1..65536 required')
        if self.im1_grant is not None and type(self.im1_grant)is not Im1ClockGrant:
            raise ValueError('exact explicit Im1ClockGrant or explicit None required')
        return self


@dataclass(frozen=True)
class AudioTickResult:
    """Small actual progress receipt, not copied sound RAM or a playback claim."""
    start_point: int
    end_point: int
    end_kind: str
    software_steps: int
    im1_delivered: bool
    reached_next_main_boundary: bool
    visited_points: tuple
    chips: AudioChipAdvance


class AudioTickBoundary(AudioBoundary):
    def __init__(self,message,receipt):
        self.receipt=receipt
        super().__init__(message)


def _source_point(audio):
    point=audio.waiting
    if (type(point)is not DriverStartupPoint or point.session is not audio.startup
            or point.generation!=audio.generation or point.reset_epoch!=audio.reset_epoch
            or point.pc not in SOURCE_POINTS or SOURCE_POINTS[point.pc]!=point.kind):
        raise AudioBoundary('actual same-invocation source-derived audio boundary required')
    return point


def execute_audio_tick(audio: OwnedGameAudio,spec: AudioTickSpec) -> AudioTickResult:
    """Grant explicit clocks, optional one real IM1, then reach the next006F.

    Main/IRQ caller order is external. If an original main operation retains
    the sound bus or resets it, existing ownership guards stop this operation.
    Every advance and IM1 delivery consumes one declared software-action slot.
    Unknown/failed child execution propagates; exhaustion is not completion.
    """
    if type(audio)is not OwnedGameAudio or type(spec)is not AudioTickSpec:
        raise ValueError('exact application audio owner and explicit tick specification required')
    spec.validate();audio._require_owned()
    start=_source_point(audio)
    grant=spec.im1_grant
    # Reject a stale/mismatched explicit IRQ before consuming either chip's
    # clocks. The adjacent application owner holds this actual loop object.
    if grant is not None and (grant.clock_hz!=audio._loop.irq_clock_hz
            or grant.timestamp<=audio._loop.irq_clock):
        raise AudioBoundary('tick IM1 clock must match the actual live driver and advance its timestamp')
    chips=audio.advance_chips(fm_ticks=spec.fm_ticks,psg_input_clocks=spec.psg_input_clocks)
    visited=[(start.pc,start.kind)];steps=0;delivered=False
    while True:
        point=_source_point(audio)
        if steps and point.pc==0x006F and (grant is None or delivered):
            return AudioTickResult(start.pc,point.pc,point.kind,steps,delivered,True,tuple(visited),chips)
        if steps==spec.max_software_steps:
            receipt=AudioTickResult(start.pc,point.pc,point.kind,steps,delivered,False,tuple(visited),chips)
            raise AudioTickBoundary('explicit audio tick software-action budget exhausted at actual '+hex(point.pc),receipt)
        if point.pc==0x0073 and grant is not None and not delivered:
            returned=audio.deliver_im1(grant)
            delivered=True
        else:
            returned=audio.advance()
        steps+=1
        if returned is not audio.waiting:
            raise AudioBoundary('actual audio operation must return its same retained source point')
        point=_source_point(audio)
        visited.append((point.pc,point.kind))
