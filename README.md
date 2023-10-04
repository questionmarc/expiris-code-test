Assumes that you have python3 installed
To run just use `python3 src/app.py`

The application will ask for each frame data shot by shot
If the first variable is an `x` for strike it'll go to the next frame (unless frame is 10)

Score is updated after each frame so strike frames and spare frame's score will change as the next 1 or 2 shots get made

Missing:
- Tests for the different functionality
- Better UI
- Regex for validating input
- Loop to improve re-inputing when data is invalid
- Breaking logic into it's own class to eliminate globals