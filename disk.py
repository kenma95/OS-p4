import string


class Disk(object):
    available_id = list(string.uppercase)

    def __init__(self, n, s):
        self.n_blocks = n
        self.blocksize = s

        self.map = []
        for i in range(self.n_blocks):
            self.map.append('.')

        self.files = {}

    def __str__(self):
        rc = '=' * 32 + '\n'
        for i in range(self.n_blocks):
            rc += self.map[i]
            if i % 32 == 31:
                rc += '\n'
        rc += '=' * 32
        return rc

    def store(self, file_name, file_size):
        needed = file_size / self.blocksize
        if file_size % self.blocksize != 0:
            needed += 1
        empty_blocks = []
        for i in range(self.n_blocks):
            if self.map[i] == '.':
                empty_blocks.append(i)

        if len(empty_blocks) < needed:
            return None

        fid = self.available_id.pop(0)

        filled_blocks = [[]]
        for i in empty_blocks[0: needed]:
            if not filled_blocks[-1] or i == filled_blocks[-1][-1] + 1:
                filled_blocks[-1].append(i)
            else:
                filled_blocks.append([i])
        clusters = len(filled_blocks)
        for c in filled_blocks:
            for i in c:
                self.map[i] = fid

        self.files[file_name] = fid
        return fid, needed, clusters

    def delete(self, file_name):
        fid = self.files[file_name]
        deleted = 0
        for i in range(self.n_blocks):
            if self.map[i] == fid:
                self.map[i] = '.'
                deleted += 1
        return fid, deleted

    def read(self, file_name, offset, read_bytes):
        fid = self.files[file_name]
        read = 0
        offset_ = offset
        remaining_ = read_bytes
        for i in range(self.n_blocks):
            if self.map[i] == fid:
                if offset_ > 0:
                    offset_ -= self.blocksize
                    if offset_ < 0:
                        read += 1
                        remaining_ += offset_
                elif remaining_ > 0:
                    remaining_ -= self.blocksize
                    read += 1
                else:
                    break
        return fid, read

