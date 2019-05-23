from log_analyzer.streamer import Streamer


def test_streamer_read_chunk(access_log_file):
    streamer = Streamer(access_log_file)
    assert len(streamer.read_chunk(1)) == 1
    assert len(streamer.read_chunk(2)) == 2


def test_streamer_read_huge_chunk(access_log_file):
    streamer = Streamer(access_log_file)
    # assert streamer.read_chunk return a value equal of less than chunk
    # in case of empty file, no data available in the file or few lines left
    assert len(streamer.read_chunk(50000)) <= 50000


def test_streamer_read_from_stdin():
    streamer = Streamer()
    # assert streamer.read_chunk return a value equal of less than chunk
    # in case of empty file, no data available in the file or few lines left
    assert len(streamer.read_chunk(50000)) <= 50000
