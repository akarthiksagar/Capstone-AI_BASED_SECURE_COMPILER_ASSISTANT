from collections import defaultdict


class DominanceAnalysis:

    def __init__(self, cfg):
        self.cfg = cfg
        self.idom = {}
        self.dom_tree = defaultdict(list)
        self.dom_frontier = defaultdict(set)

    # ======================================================
    # Compute Dominators
    # ======================================================

    def compute(self):
        self._compute_dominators()
        self._compute_dominance_frontier()
        return self.idom, self.dom_tree, self.dom_frontier

    def _compute_dominators(self):
        blocks = self.cfg.blocks
        entry = self.cfg.entry

        dominators = {b: set(blocks) for b in blocks}
        dominators[entry] = {entry}

        changed = True
        while changed:
            changed = False

            for b in blocks:
                if b == entry:
                    continue

                preds = b.predecessors
                if not preds:
                    continue

                new_dom = set(blocks)
                for p in preds:
                    new_dom &= dominators[p]

                new_dom.add(b)

                if new_dom != dominators[b]:
                    dominators[b] = new_dom
                    changed = True
        
        # 🔥 DEBUG DOMINATOR SETS
        print("\n==== DOMINATOR SETS ====")
        for b in blocks:
            print(b.name, ":", [d.name for d in dominators[b]])


        # Immediate dominator
        for b in blocks:
            if b == entry:
                self.idom[b] = None
                continue

            doms = dominators[b] - {b}
            self.idom[b] = max(doms, key=lambda d: len(dominators[d]))

        for b, idom in self.idom.items():
            if idom:
                self.dom_tree[idom].append(b)

    # ======================================================
    # Dominance Frontier
    # ======================================================

    def _compute_dominance_frontier(self):
        blocks=self.cfg.blocks
        for b in self.cfg.blocks:
            if len(b.predecessors) >= 2:
                for p in b.predecessors:
                    runner = p
                    while runner != self.idom[b]:
                        self.dom_frontier[runner].add(b)
                        runner = self.idom[runner]

       # 🔥 DEBUG DOMINANCE FRONTIER
        print("\n==== DOMINANCE FRONTIER ====")
        for b in blocks:
            print(b.name, ":", [x.name for x in self.dom_frontier[b]])
