import './App.css';
import RecorderView from './recorderView.js';
import LoadingSpinner from './loadingSpinner.js'
import { useState, useEffect } from 'react';


const host = "http://localhost:8000"

function App() {

  const [connectedToBackend, setConnectedToBackend ] = useState(false)
  const [audioVideoFile, setAudioVideoFile ] = useState(null)
  const [audioOnlyFile, setAudioOnlyFile ] = useState(null)
  const [videoOnlyFile, setVideoOnlyFile] = useState(null)
  const [recordingUuid, setRecordingUuid] = useState(null)
  const [showView, setShowView] = useState("recording")

  useEffect(() => {
    fetch(host.concat("/"))
      .then(response => setConnectedToBackend(true))
      .catch(error => {
        console.error(error);
        setConnectedToBackend(false);
      })
  }, []);

  function reloadWindow(){
    window.location.reload(false)
  }

  function handleSubmit(){
    let data = new FormData();
    data.append("audio_video_file", new File([audioVideoFile], "audio_video.mp4"))
    data.append("audio_only_file", new File([audioOnlyFile], "audio_only.wav"))
    data.append("video_only_file", new File([videoOnlyFile], "video_only.mp4"))
    setShowView("processing")
    fetch(host.concat("/recordings"), {
      method: 'POST',
      body: data
    })
      .then(response => response.json())
      .then(json => {
        setRecordingUuid(json.uuid)
        setShowView("playback")
      })
      .catch(error => console.error(error));
  }

  var page = null;
  switch (showView){
    case "processing":
      page = (
        <div style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          height: "100%"
        }}>
          <h2>combining video...</h2>
          <LoadingSpinner />
        </div>)
      break;
    case "playback":
        page = (
          <div>
            <div>
              <video src={host.concat('/recordings/').concat(recordingUuid).concat('/output')} type="video/mp4" controls autoPlay loop/>
            </div>
            <div>
              <span><button className="submitButton" onClick={reloadWindow}>Restart</button></span>
            </div>
          </div>
        );
        break;
    default:
        page = (
        <div>
        <p> Record each sample and press submit</p>
          <div className="rows">
            <RecorderView name="Audio & Video" useVideo={true} useAudio={true} onStop={(blobUrl, blob) => {setAudioVideoFile(blob)}} />
            <RecorderView name="Audio Only" useVideo={false} useAudio={true} onStop={(blobUrl, blob) => {setAudioOnlyFile(blob)}} />
            <RecorderView name="Video Only" useVideo={true} useAudio={false} onStop={(blobUrl, blob) => {setVideoOnlyFile(blob)}} />
          </div>
          <div>
            <button className="submitButton" onClick={handleSubmit}>Submit</button>
          </div>
        </div>
      );
        break;
  }

  return (
    <div>
      <h2>Server: {connectedToBackend ? "connected" : "disconnected"}</h2>
      <div className="App">
        {page}
      </div>
    </div>
  )
};

export default App;
