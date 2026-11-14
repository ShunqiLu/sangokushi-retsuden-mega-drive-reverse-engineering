"""Candidate typed observations for the existing deployment/terrain kernels.

None carrier values remain unobserved; a WORD result is not evidence of a
complete LONG register. The retained frame is the same first-deployment ABI.
"""
from dataclasses import dataclass
from tools.high_level_battle_ai.domain import uint
from tools.high_level_battle_ai.contexts_first_deployment import FirstDeploymentFrame
from tools.high_level_battle_ai.contexts_policy_memory import checked_policy_table


@dataclass(frozen=True)
class DeploymentTerrainFields:
    carrier: int | None
    word: int
    category: int
    lookup: object
    extend: bool

    def validate(self, state):
        if self.carrier is not None:
            uint(self.carrier, 32)
        uint(self.word, 16)
        uint(self.category, 8)
        checked_policy_table(self.lookup, state)
        if type(self.extend) is not bool:
            raise ValueError('real final offset shift X required')
        return self


@dataclass(frozen=True)
class DeploymentProbeFields:
    frame: FirstDeploymentFrame
    placed: bool

    def validate(self, state):
        if type(self.frame) is not FirstDeploymentFrame:
            raise ValueError('sole retained deployment frame required')
        self.frame.validate(state)
        if type(self.placed) is not bool:
            raise ValueError('real placement carry required')
        return self


@dataclass(frozen=True)
class DeploymentEdgeFields:
    frame: FirstDeploymentFrame
    offset: int
    source: object
    found: bool

    def validate(self, state):
        if type(self.frame) is not FirstDeploymentFrame:
            raise ValueError('sole retained deployment frame required')
        self.frame.validate(state)
        uint(self.offset, 16)
        checked_policy_table(self.source, state)
        if type(self.found) is not bool:
            raise ValueError('real vacancy carry required')
        return self
