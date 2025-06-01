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

def test_nested_object():
    parser = StreamingJsonParser()
    parser.consume('{"foo": {"nested": "value"}}')
    assert parser.get() == {"foo": {"nested": "value"}}

def test_partial_nested_object():
    parser = StreamingJsonParser()
    parser.consume('{"foo": {"nested": "val')
    assert parser.get() == {"foo": {"nested": "val"}}

def test_multiple_keys():
    parser = StreamingJsonParser()
    parser.consume('{"foo": "bar", "baz": "qux"}')
    assert parser.get() == {"foo": "bar", "baz": "qux"}

def test_chunked_multiple_keys():
    parser = StreamingJsonParser()
    parser.consume('{"foo": "bar", ')
    parser.consume('"baz": "qux"}')
    assert parser.get() == {"foo": "bar", "baz": "qux"}

def test_partial_key():
    parser = StreamingJsonParser()
    parser.consume('{"foo": "bar", "worl')
    assert parser.get() == {"foo": "bar"}

if __name__ == "__main__":
    test_streaming_json_parser()
    test_chunked_streaming_json_parser()
    test_partial_streaming_json_parser()
    test_nested_object()
    test_partial_nested_object()
    test_multiple_keys()
    test_chunked_multiple_keys()
    test_partial_key()
    print("All tests passed!")