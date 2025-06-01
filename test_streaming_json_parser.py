from streaming_json_parser import StreamingJsonParser

def test_streaming_json_parser():
    parser = StreamingJsonParser()
    parser.consume('{"foo": "bar"}')
    assert parser.get() == {"foo": "bar"}

def test_chunked_streaming_json_parser():
    parser = StreamingJsonParser()
    parser.consume('{"foo":')
    parser.consume('"bar"}')
    assert parser.get() == {"foo": "bar"}

def test_partial_streaming_json_parser():
    parser = StreamingJsonParser()
    parser.consume('{"foo": "bar')
    assert parser.get() == {"foo": "bar"}

def test_partial_key():
    parser = StreamingJsonParser()
    parser.consume('{"foo": "bar", "worl')
    assert parser.get() == {"foo": "bar"}

def test_switzerl_example():
    parser = StreamingJsonParser()
    parser.consume('{"test": "hello", "country": "Switzerl')
    assert parser.get() == {"test": "hello", "country": "Switzerl"}

if __name__ == "__main__":
    test_streaming_json_parser()
    test_chunked_streaming_json_parser()
    test_partial_streaming_json_parser()
    test_partial_key()
    test_switzerl_example()
    print("All tests passed!")