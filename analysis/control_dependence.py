from collections import defaultdict
import os


class ControlDependenceGraph:

    def __init__(self, cfg):
        self.cfg = cfg
        self.post_dom = {}
        self.ipdom = {}
        self.control_dependencies = defaultdict(set)

    # =====================================================
    # ENTRY POINT
    # =====================================================

    def compute(self):
        self._compute_post_dominators()
        self._compute_ipost_dominators()
        self._compute_control_dependence()
        return self.control_dependencies

    # =====================================================
    # POST-DOMINATORS
    # =====================================================

    def _compute_post_dominators(self):

        blocks = self.cfg.blocks
        exit_block = self.cfg.exit

        if exit_block is None:
            raise Exception("CFG must have an exit block for CDG.")

        post_dom = {b: set(blocks) for b in blocks}
        post_dom[exit_block] = {exit_block}

        changed = True
        while changed:
            changed = False

            for b in blocks:
                if b == exit_block:
                    continue

                succs = b.successors
                if not succs:
                    continue

                new_set = set(blocks)
                for s in succs:
                    new_set &= post_dom[s]

                new_set.add(b)

                if new_set != post_dom[b]:
                    post_dom[b] = new_set
                    changed = True

        self.post_dom = post_dom

    # =====================================================
    # IMMEDIATE POST-DOMINATOR
    # =====================================================

    def _compute_ipost_dominators(self):

        for b in self.cfg.blocks:

            if b == self.cfg.exit:
                self.ipdom[b] = None
                continue

            post_doms = self.post_dom[b] - {b}

            # choose closest post-dominator
            self.ipdom[b] = min(
                post_doms,
                key=lambda x: len(self.post_dom[x])
            )

    # =====================================================
    # CONTROL DEPENDENCE
    # =====================================================

    def _compute_control_dependence(self):

        for b in self.cfg.blocks:
            if os.getenv("SECURELANG_DEBUG_CFG", "0") == "1":
                print(b.name, "successors:", [s.name for s in b.successors])

            # Only true branching blocks
            if len(b.successors) < 2:
                continue

            for succ in b.successors:

                # Skip if successor post-dominates branch
                if succ in self.post_dom[b]:
                    continue

                runner = succ

                while runner is not None and runner != self.ipdom[b]:
                    self.control_dependencies[b].add(runner)
                    runner = self.ipdom[runner]
