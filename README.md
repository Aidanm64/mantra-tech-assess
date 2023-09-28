# Mantra Technical Assessment

## Requirements
- docker
- docker-compose v2 (docker compose commands)
- nvidia gpu
- ~10GB of free space (backend container is pretty big)

## How to run
### Full application
1. navigate to the main application folder
`cd app`

2. build and deploy the app locally:
`make start`
Note: this will open up a browser window pointed at the frontend page when it is complete. If this doesnt work for some reason, go to http://localhost:3000

3. interact with the app from your browser. Note that the processing times are inconsistent and generally pretty lengthy.

4. shut everything down
`make stop`


### Tests
`make test_backend`

### Run individually
if you want to see the console output of each service, they can be run separately as follows:
`make backend`
then, in a separate shell
`make frontend`
then you can navigate to 



## Notes
- I struggled to get consitent results for wav2lib processing time and quility. Occasionally it takes a relatively short period of time to process the files and return a desirable output. The more common experience is that the processing time will be long and the output will consist of the audio overlaid onto a truncated, looping portion of the input video. I've determined that wait time and quality are related to the value "Length of mel chunks" thats shown in wav2lib output.

- I use [this](https://www.cosmicpython.com/) approach to building web applications as it provides excellent flexibility in design and ease of testing. It can be a lot to take in at first so let me know if you have any questions.


## Next steps
### Wav2Lip progress
Extracting the wav2lip progress information poses a challenge with a synchronous service. My approach to solving this would include having the wav2lib algorithm be deployed separately so it can be run asynchronously with progress updates being communicated either through the backend REST interface or over a message bus. The frontend could then poll the "GET /recording/{uuid}" endpoint and report the "combination_percentage" property to the UI. This would also allow more options for optmization of the execution of the wav2lib algotrithm as we could allocate resources separately.

### Wav2Lip training
There is a way to pretrain the ESRGAN model outlined [here](https://github.com/Markfryazino/wav2lip-hq#the-algorithm) using the Audio+Video sample we are collecting. Ive left a placeholer in the code where this step would occur. Unfortunately, the [linked article](https://drive.google.com/file/d/1ptTFVNc1v9kzr-V3OK8DJEywziVMKh68/view) that outlines this process is in russian, and I cant read russian. Kinda stumped on that one for now.

### Recording session persistence
Currently theres no way to revisit previous recording sessions. I've set the backend up with mongodb to keep a record of the recording sessions so this functionality could be added simply by adding a query endpoint for all recording sessions and a corresponding feature in the ui.


