import './App.css'
import { useReactMediaRecorder } from "react-media-recorder";

function RecorderView(props){
  const { status, startRecording, stopRecording, mediaBlobUrl } =
    useReactMediaRecorder({ video: props.useVideo , audio: props.useAudio, onStop: props.onStop });
  return (
    <div className="recorderView">
      <div>
        <p>{props.name} : {status}</p>
        <button className="recordButton" onClick={startRecording}>Record</button>
        <button className="recordButton" onClick={stopRecording}>Stop</button>
        <video src={mediaBlobUrl} controls autoPlay loop />
        <h2>{status === "stopped" ? "Completed" : ""}</h2>
      </div>
    </div>
  );
}


export default RecorderView;