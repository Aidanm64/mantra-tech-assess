import './App.css'
import { useReactMediaRecorder } from "react-media-recorder";
import { useEffect } from 'react';

function RecorderView(props){
  const { status, startRecording, stopRecording, mediaBlobUrl } =
    useReactMediaRecorder({ video: props.useVideo , audio: props.useAudio, onStop: props.onStop });
    useEffect(()=>{
      if (status === "recording"){
        setTimeout(() => stopRecording(), props.duration)
      }
    }, [status])
  return (
    <div className="recorderView">
      <div>
        <p>{props.name} : {status}</p>
        <button className="recordButton" onClick={startRecording}>Record</button>
        <video src={mediaBlobUrl} controls autoPlay loop />
        <h2>{status === "stopped" ? "Completed" : ""}</h2>
      </div>
    </div>
  );
}


export default RecorderView;