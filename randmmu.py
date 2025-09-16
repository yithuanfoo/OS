from mmu import MMU
import random

class RandMMU(MMU):
    def __init__(self, frames):
        # TODO: Constructor logic for RandMMU
        self.num_frames = frames
        self.frames = [None] * frames
        self.page_to_frame = {}
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

    def read_memory(self, page_number):
        # TODO: Implement the method to read memory
        if page_number in self.page_to_frame:
            if self.debug:
                f = self.page_to_frame[page_number]
                print(f"[HIT] Read page {page_number} in frame {f} (dirty={self.frames[f]['dirty']})")
                return
            
        self.page_faults += 1
        if self.debug:
            print(f"[MISS] Read page {page_number} -> page fault")
            
        idx = None
        for i, slot in enumerate(self.frames):
            if slot is None:
                idx = i
                break

        if idx is None:
            idx = random.randrange(self.num_frames)
            victim = self.frames[idx]
            if victim is not None:
                if victim['dirty']:
                    self.disk_writes += 1
                    if self.debug:
                        print(f"Evict page {victim['page']} from frame {idx} (dirty -> write to disk)")
                else:
                    if self.debug:
                        print(f"Evict page {victim['page']} from frame {idx} (clean)")
                self.page_to_frame.pop(victim['page'], None)
        
        self.frames[idx] = {'page': page_number, 'dirty': False}
        self.page_to_frame[page_number] = idx
        self.disk_reads += 1
        if self.debug:
            print(f"Loaded page {page_number} into frame {idx} (dirty=0)")

    def write_memory(self, page_number):
        # TODO: Implement the method to write memory
        if page_number in self.page_to_frame:
            f = self.page_to_frame[page_number]
            self.frames[f]['dirty'] = True
            if self.debug:
                print(f"[HIT] Write page {page_number} in frame {f} (dirty=1)")
            return
        
        self.page_faults += 1
        if self.debug:
            print(f"[MISS] Write page {page_number} -> page fault")
        
        idx = None
        for i, slot in enumerate(self.frames):
            if slot is None:
                idx = i
                break

        if idx is None:
            idx = random.randrange(self.num_frames)
            victim = self.frames[idx]
            if victim is not None:
                if victim['dirty']:
                    self.disk_writes += 1
                    if self.debug:
                        print(f"Evict page {victim['page']} from frame {idx} (dirty -> write to disk)")
                else:
                    if self.debug:
                        print(f"Evict page {victim['page']} from frame {idx} (clean)")
                self.page_to_frame.pop(victim['page'], None)
                                           
        self.frames[idx] = {'page': page_number, 'dirty': True}
        self.page_to_frame[page_number] = idx
        self.disk_reads += 1
        if self.debug:
            print(f"Loaded page {page_number} into frame {idx} (dirty=1)")
    def get_total_disk_reads(self):
        # TODO: Implement the method to get total disk reads
        return self.disk_reads

    def get_total_disk_writes(self):
        # TODO: Implement the method to get total disk writes
        return self.disk_writes

    def get_total_page_faults(self):
        # TODO: Implement the method to get total page faults
        return self.page_faults
    
