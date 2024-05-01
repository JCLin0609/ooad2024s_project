from app.models.fuzzStatus import FuzzStatus
import pytest


@pytest.fixture
def input_string():
    return '''
start_time        : 14183
last_update       : 14196
run_time          : 643
fuzzer_pid        : 834770
cycles_done       : 73
cycles_wo_finds   : 1
time_wo_finds     : 0
fuzz_time         : 633
calibration_time  : 0
sync_time         : 0
trim_time         : 10
execs_done        : 745429
execs_per_sec     : 1157.58
execs_ps_last_min : 51.51
corpus_count      : 77
corpus_favored    : 7
corpus_found      : 75
corpus_imported   : 0
corpus_variable   : 0
max_depth         : 5
cur_item          : 37
pending_favs      : 0
pending_total     : 57
stability         : 100.00%
bitmap_cvg        : 0.00%
saved_crashes     : 14
saved_hangs       : 0
last_find         : 0
last_crash        : 14190
last_hang         : 0
execs_since_crash : 7666
exec_timeout      : 20
slowest_exec_ms   : 0
peak_rss_mb       : 2
cpu_affinity      : 0
edges_found       : 54
total_edges       : 8388608
var_byte_count    : 0
havoc_expansion   : 1
auto_dict_entries : 0
testcache_size    : 7607
testcache_count   : 76
testcache_evict   : 0
afl_banner        : fuzz_targets/afl_test1/afl_test1
afl_version       : ++4.20c
target_mode       : shmem_testcase default
command_line      : AFLplusplus/afl-fuzz -i fuzz_targets/afl_test1/input -o fuzz_targets/afl_test1/output fuzz_targets/afl_test1/afl_test1    
'''


def test_create_fuzzStatus_from_string(input_string):
    fuzz_status = FuzzStatus.from_string(input_string)
    assert fuzz_status.start_time == 14183
    assert fuzz_status.last_update == 14196
    assert fuzz_status.execs_per_sec == 1157.58
    assert fuzz_status.stability == '100.00%'
    assert fuzz_status.bitmap_cvg == '0.00%'
    assert fuzz_status.afl_banner == 'fuzz_targets/afl_test1/afl_test1'
