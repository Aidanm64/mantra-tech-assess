import './App.css'
import { useReactMediaRecorder } from "react-media-recorder";


function RecorderView(props){
  const { status, startRecording, stopRecording, mediaBlobUrl, onStop} =
    useReactMediaRecorder({ video: props.useVideo , audio: props.useAudio, onStop: props.onStop });
  return (
    <div className="recorderView">
      <p>{props.name} : {status}</p>
      <button className="recordButton" onClick={startRecording}>Start</button>
      <button className="recordButton" onClick={stopRecording}>Stop</button>
      <video src={mediaBlobUrl} controls autoPlay loop />
    </div>
  );
}


export default RecorderView;