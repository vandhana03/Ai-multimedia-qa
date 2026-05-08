import whisper

model = whisper.load_model("base")

def transcribe_file(path):

    result = model.transcribe(path)

    return result