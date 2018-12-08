from compression_lambda import strip_extension


def test_compression_lambda():
    input_path = "audio.mp3"
    output_name = strip_extension(input_path)

    assert output_name == "audio"
