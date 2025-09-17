from mmu import MMU

class LruMMU(MMU):
    def __init__(self, frames):
        # TODO: Constructor logic for LruMMU
        self.num_frames = frames
        self.frames = [None] * frames
        self.page_to_frame = {}
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0
        self.debug = False
        self.LRU_list = []

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
                frame = self.page_to_frame[page_number]
                print(f"Hit      Read page {page_number} in frame {frame} (dirty={self.frames[frame]['dirty']})")
            self.update_LRU(page_number)
            return
        
        self.page_faults += 1
        if self.debug:
            print(f"Miss     Read page {page_number}: page fault")
        
        idx = None
        for i, slot in enumerate(self.frames):
            if slot is None:
                idx = i
                break

        if idx is None:
            #helper function which determines the least recently used page
            idx = self.select_LRU()
            victim = self.frames[idx]
            if victim is not None:
                if victim['dirty']:
                    self.disk_writes += 1
                    if self.debug:
                        print(f"Evict page {victim['page']} from frame {idx}: dirty -> write to disk")
                else: 
                    if self.debug:
                        print(f"Evict page {victim['page']} from frame {idx}: clean ")

        self.frames[idx] = {'page' : page_number, 'dirty' : False}
        self.page_to_frame[page_number] = idx
        self.disk_reads += 1
        self.update_LRU(page_number)
        
        if self.debug:
            print(f"Loaded page {page_number} into frame {idx}: dirty = 0")
    
    def select_LRU(self):
        #list of LRU values (LRU_list) is maintained where its already ordered from least to most recently used
        #pop(0) returns the first element which is the least recently used
        LRU_page = self.LRU_list.pop(0)
        #gives the frame index where this page is sitting in memory 
        LRU_idx = self.page_to_frame[LRU_page]
        #since page will get removed, safe to delete it 
        del self.page_to_frame[LRU_page]
        #returns the current least recently used page
        return LRU_idx
    
    def update_LRU(self, page_number):
        #if the page is already in the list, we've used it before
        if page_number in self.LRU_list:
            #since accessing it again we initally remove it
            self.LRU_list.remove(page_number)
        #then add it to the end of the list again, correctly updating in order of least recently used
        self.LRU_list.append(page_number)


    def write_memory(self, page_number):
        # TODO: Implement the method to write memory
        if page_number in self.page_to_frame:
            frame = self.page_to_frame[page_number]
            self.frames[frame]['dirty'] = True
            if self.debug:
                print(f"HIT      Write page {page_number} in frame {frame}: dirty = 1")
            self.update_LRU(page_number)
            return
        
        self.page_faults += 1

        if self.debug:
            print(f"Miss     Write page {page_number}: page fault")

        idx = None
        for i, slot in enumerate(self.frames):
            if slot is None:
                idx = i
                break

        if idx is None:
            idx = self.select_LRU()
            victim = self.frames[idx]
            if victim is not None:
                if victim['dirty']:
                    self.disk_writes += 1
                    if self.debug:
                        print(f"Evict page {victim['page']} from frame {idx}: dirty -> write to disk")
                else:
                    if self.debug:
                        print(f"Evict page {victim['page']} from frame {idx}: clean ")
        
        self.frames[idx] = {'page': page_number, 'dirty' : True}
        self.page_to_frame[page_number] = idx
        self.disk_reads += 1
        self.update_LRU(page_number)

        if self.debug:
            print(f"Loaded page {page_number} into frame {idx}: dirty = 1")


    def get_total_disk_reads(self):
        # TODO: Implement the method to get total disk reads
        return self.disk_reads

    def get_total_disk_writes(self):
        # TODO: Implement the method to get total disk writes
        return self.disk_writes

    def get_total_page_faults(self):
        # TODO: Implement the method to get total page faults
        return self.page_faults
