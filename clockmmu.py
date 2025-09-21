from mmu import MMU


class ClockMMU(MMU):
    def __init__(self, frames):
        # TODO: Constructor logic for EscMMU
        if frames < 0:
            raise ValueError("frames must be >= 0")
        self.num_frames = frames
        # List of Frames
        self.frames = [None] * frames
        # Helps track page to frame index
        self.page_to_frame = {}
        # Stack of free frame ids
        self.free = list(range(frames))[::-1]
        # Clock hand
        self.hand = 0

        # Counters
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0

        self.debug = False

    def set_debug(self):
        # TODO: Implement the method to set debug mode
        self.debug = True

    def reset_debug(self):
        # TODO: Implement the method to reset debug mode
        self.debug = False

    def _alloc_frame(self):
        # if self.num_frames == 0:
        #     return 0
        if self.free:
            return self.free.pop()
        return self._clock_pick_victim()

    def _clock_pick_victim(self):
        """
        Helper function to pick a victim using an enhanced Second-Chance (Clock) victim selection:
        - clear ref-> 0 and give a second chance to ref=1 pages
        """
        N = self.num_frames
        assert N > 0
        scanned = 0
        dirty_candidate = None

        # Loop until a victim is found
        while True:
            f = self.hand
            meta = self.frames[f]

            if meta is None:
                idx = f
                self.hand = (f + 1) % N
                return idx

            if meta['ref'] == 1:
                # Second chance: clear and move on
                meta['ref'] = 0
            else:
                # ref == 0 -> candidate
                if not meta['dirty']:
                    # clean victim
                    idx = f
                    self.hand = (f + 1) % N
                    return self._evict_and_return(idx)
                # keep first dirty candidate in this sweep
                if dirty_candidate is None:
                    dirty_candidate = f

            # advance hand
            self.hand = (self.hand + 1) % N
            scanned += 1

            if scanned >= N:
                if dirty_candidate is not None:
                    # Evict the first dirty zero-ref
                    idx = dirty_candidate
                    self.hand = (idx + 1) % N
                    return self._evict_and_return(idx)

    # Helper function to evict and return the frame index
    def _evict_and_return(self, idx):
        self._evict(idx)
        return idx

    # Helper function to evict the frame
    def _evict(self, idx):
        # Get the victim frame
        victim = self.frames[idx]
        # If victim frame is empty, return
        if victim is None:
            return
        
        # Get the page number of the victim
        vpage = victim['page']
        if victim['dirty']:
            self.disk_writes += 1
            if self.debug:
                print(f"Evict page {vpage} from frame {idx} (dirty -> write to disk)")
        else:
            if self.debug:
                print(f"Evict page {vpage} from frame {idx} (clean)")
        self.page_to_frame.pop(vpage, None)
        self.frames[idx] = None

    def _load(self, idx, page_number, dirty):
        """Place the page into frame idx, mark ref=1 on access, and count disk read."""
        if self.num_frames == 0:
            self.disk_reads += 1
            if self.debug:
                print(f"Loaded page {page_number} into frame 0 (simulated, dirty={int(dirty)})")
            return

        # Load the page into the frame
        self.frames[idx] = {'page': page_number, 'dirty': dirty, 'ref': 1}
        self.page_to_frame[page_number] = idx
        self.disk_reads += 1
        if self.debug:
            print(f"Loaded page {page_number} into frame {idx} (dirty={int(dirty)})")

    def read_memory(self, page_number):
        # TODO: Implement the method to read memory
        # HIT: set ref=1, leave dirty as-is
        if page_number in self.page_to_frame:
            f = self.page_to_frame[page_number]
            self.frames[f]['ref'] = 1
            if self.debug:
                print(f"[HIT]  Read  page {page_number} in frame {f} (dirty={int(self.frames[f]['dirty'])})")
            return

        # MISS path
        self.page_faults += 1
        if self.debug:
            print(f"[MISS] Read  page {page_number} -> page fault")

        idx = self._alloc_frame()
        self._load(idx, page_number, dirty=False)

    def _load(self, idx, page_number, dirty):
        """Place the page into frame idx, mark ref=1 on access, and count disk read."""
        if self.num_frames == 0:
            # No storage possible; just count the disk read for the simulation.
            self.disk_reads += 1
            if self.debug:
                print(f"Loaded page {page_number} into frame 0 (simulated, dirty={int(dirty)})")
            return

        # Load the page into the frame
        self.frames[idx] = {'page': page_number, 'dirty': dirty, 'ref': 1}
        self.page_to_frame[page_number] = idx
        self.disk_reads += 1
        if self.debug:
            print(f"Loaded page {page_number} into frame {idx} (dirty={int(dirty)})")
    
    def write_memory(self, page_number):
        # TODO: Implement the method to write memory
        if page_number in self.page_to_frame:
            f = self.page_to_frame[page_number]
            self.frames[f]['ref'] = 1
            self.frames[f]['dirty'] = True
            if self.debug:
                print(f"[HIT]  Write page {page_number} in frame {f} (dirty=1)")
            return

        # Miss path
        self.page_faults += 1
        if self.debug:
            print(f"[MISS] Write page {page_number} -> page fault")

        idx = self._alloc_frame()
        self._load(idx, page_number, dirty=True)

    def get_total_disk_reads(self):
        # TODO: Implement the method to get total disk reads
        return self.disk_reads

    def get_total_disk_writes(self):
        # TODO: Implement the method to get total disk writes
        return self.disk_writes

    def get_total_page_faults(self):
        # TODO: Implement the method to get total page faults
        return self.page_faults
