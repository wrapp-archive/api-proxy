A simple golang app which intercepts all backend calls and can replace responses

How to use
=== 
1. Run app: "go run main.go"

2. Point your client to your own machine port 8080

- For Android: Choose endpoint to http://10.0.2.2:8080 (http://developer.android.com/tools/devices/emulator.html#networkaddresses)

3. All responses will be saved in a folder called 'output'. If you want to override a response, put it in the folder 'override' (same format as in the 'output' folder)
 
Installing Go
===
```bash
brew install go
```
