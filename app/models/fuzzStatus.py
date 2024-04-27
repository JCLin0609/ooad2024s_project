import re


class FuzzStatus:
    def __init__(self, start_time: int, last_update: int, run_time: int, fuzzer_pid: int, cycles_done: int,
                 cycles_wo_finds: int, time_wo_finds: int, fuzz_time: int, calibration_time: int, sync_time: int,
                 trim_time: int, execs_done: int, execs_per_sec: float, execs_ps_last_min: float, corpus_count: int,
                 corpus_favored: int, corpus_found: int, corpus_imported: int, corpus_variable: int, max_depth: int,
                 cur_item: int, pending_favs: int, pending_total: int, stability: float, bitmap_cvg: float,
                 saved_crashes: int, saved_hangs: int, last_find: int, last_crash: int, last_hang: int,
                 execs_since_crash: int, exec_timeout: int, slowest_exec_ms: int, peak_rss_mb: int,
                 cpu_affinity: int, edges_found: int, total_edges: int, var_byte_count: int, havoc_expansion: int,
                 auto_dict_entries: int, testcache_size: int, testcache_count: int, testcache_evict: int,
                 afl_banner: str, afl_version: str, target_mode: str, command_line: str):
        self.start_time = start_time
        self.last_update = last_update
        self.run_time = run_time
        self.fuzzer_pid = fuzzer_pid
        self.cycles_done = cycles_done
        self.cycles_wo_finds = cycles_wo_finds
        self.time_wo_finds = time_wo_finds
        self.fuzz_time = fuzz_time
        self.calibration_time = calibration_time
        self.sync_time = sync_time
        self.trim_time = trim_time
        self.execs_done = execs_done
        self.execs_per_sec = execs_per_sec
        self.execs_ps_last_min = execs_ps_last_min
        self.corpus_count = corpus_count
        self.corpus_favored = corpus_favored
        self.corpus_found = corpus_found
        self.corpus_imported = corpus_imported
        self.corpus_variable = corpus_variable
        self.max_depth = max_depth
        self.cur_item = cur_item
        self.pending_favs = pending_favs
        self.pending_total = pending_total
        self.stability = stability
        self.bitmap_cvg = bitmap_cvg
        self.saved_crashes = saved_crashes
        self.saved_hangs = saved_hangs
        self.last_find = last_find
        self.last_crash = last_crash
        self.last_hang = last_hang
        self.execs_since_crash = execs_since_crash
        self.exec_timeout = exec_timeout
        self.slowest_exec_ms = slowest_exec_ms
        self.peak_rss_mb = peak_rss_mb
        self.cpu_affinity = cpu_affinity
        self.edges_found = edges_found
        self.total_edges = total_edges
        self.var_byte_count = var_byte_count
        self.havoc_expansion = havoc_expansion
        self.auto_dict_entries = auto_dict_entries
        self.testcache_size = testcache_size
        self.testcache_count = testcache_count
        self.testcache_evict = testcache_evict
        self.afl_banner = afl_banner
        self.afl_version = afl_version
        self.target_mode = target_mode
        self.command_line = command_line

    @classmethod
    def from_string(cls, status_string: str):
        lines = status_string.strip().split('\n')
        params = {}
        for line in lines:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            if value.isdigit():
                value = int(value)
            elif re.match(r"^\d+\.\d+$", value):
                value = float(value)
            params[key] = value

        return cls(**params)
