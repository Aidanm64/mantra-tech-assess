import logo from './logo.svg';
import './App.css';
import RecordView from './recordView.js';
import { useState, useEffect } from 'react';


const host = "http://localhost:8000"

function App() {

  const [connectedToBackend, setConnectedToBackend ] = useState(false)
  const [audioVideoFile, setAudioVideoFile ] = useState(null)
  const [audioOnlyFile, setAudioOnlyFile ] = useState(null)
  const [videoOnlyFile, setVideoOnlyFile] = useState(null)
  const [recordingUuid, setRecordingUuid] = useState(null)
  const [showVideo, setShowVideo] = useState(false)

  useEffect(() => {
    fetch(host.concat("/"))
      .then(response => setConnectedToBackend(true))
      .catch(error => {
        console.error(error);
        setConnectedToBackend(false);
      })
  });




  function handleSubmit(){
    console.log("hello")
    let data = new FormData();
    data.append("audio_video_file", audioVideoFile)
    data.append("audio_only_file", audioOnlyFile)
    data.append("video_only_file", videoOnlyFile)
    console.log(data)
    fetch(host.concat("/recordings"), {
      method: 'POST',
      body: data
    })
      .then(response => response.json())
      .then(json => {
        setRecordingUuid(json.uuid)
        setShowVideo(true)
      })
      .catch(error => console.error(error));
  }

  if ( !showVideo ) {
    return (
      <div className="App">
      <div>
        <h1>{connectedToBackend ? "connected" : "disconnected"}</h1>
      </div>
      <div className="rows">
        <div className="row">
          <RecordView useVideo={true} useAudio={true} onStop={(blobUrl, blob) => {
            console.log("hey")
            setAudioVideoFile(blob)}} />
        </div>
        <div className="row">
          <RecordView useVideo={false} useAudio={true} onStop={(blobUrl, blob) => {setAudioOnlyFile(blob)}} />
        </div>
        <div className="row">
          <RecordView useVideo={true} useAudio={false} onStop={(blobUrl, blob) => {setVideoOnlyFile(blob)}} />
        </div>
      </div>
      <div>
      <button onClick={handleSubmit}>Submit</button>
      </div>
      </div>
    );
  }
    return (
      <div>
      <video src={host.concat('/recordings/').concat(recordingUuid).concat('/output')} type="video/mp4" controls autoPlay loop/>
      </div>
    )
};

export default App;
